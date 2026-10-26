#!/usr/bin/env python3
"""
DoubtLens Contract Verification Test Runner
Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)

Validates DoubtLens Flask API endpoints against the frozen API contract:
1. GET  /api/health   -> 200 {"status": "ok"}
2. POST /api/explain  -> 200 {"topic": str, "explanation": str, "steps": list, "key_points": list}
3. POST /api/quiz     -> 200 {"questions": [{"q": str, "options": [str x 4], "answer_index": 0-3, "why": str}] x 5}
4. POST /api/explain  (empty) -> 400 {"error": str}

Uses only Python 3 standard library (no pip packages required).
"""

import sys
import os
import json
import urllib.request
import urllib.error
import mimetypes

PORT = os.environ.get("PORT", "5000")
BASE_URL = f"http://127.0.0.1:{PORT}"
SAMPLES_DIR = os.path.dirname(os.path.abspath(__file__))


def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def test_health() -> bool:
    url = f"{BASE_URL}/api/health"
    print(f"\n[1/5] Testing GET {url} ...")
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            body = json.loads(resp.read().decode("utf-8"))
            print(f"  Status: {status}, Body: {body}")
            assert status == 200, f"Expected 200, got {status}"
            assert body.get("status") == "ok", f"Expected 'status': 'ok', got {body}"
            print("  ✓ PASS")
            return True
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        return False


def test_explain_text() -> bool:
    url = f"{BASE_URL}/api/explain"
    print(f"\n[2/5] Testing POST {url} (Text-only Question) ...")
    boundary = "----WebKitFormBoundaryDoubtLensTest"
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="question"\r\n\r\n'
        "A 5kg block is pulled with 20N force on a surface with 5N friction. What is acceleration?\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="language"\r\n\r\n'
        "en\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="level"\r\n\r\n'
        "simple\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    try:
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            data = json.loads(resp.read().decode("utf-8"))
            print(f"  Status: {status}")
            print(f"  Topic: {data.get('topic')}")
            assert status == 200, f"Expected 200, got {status}"
            assert "topic" in data and isinstance(data["topic"], str), "Missing or invalid 'topic'"
            assert "explanation" in data and isinstance(data["explanation"], str), "Missing or invalid 'explanation'"
            assert "steps" in data and isinstance(data["steps"], list), "Missing or invalid 'steps'"
            assert "key_points" in data and isinstance(data["key_points"], list), "Missing or invalid 'key_points'"
            assert len(data["steps"]) > 0, "'steps' list cannot be empty"
            assert len(data["key_points"]) > 0, "'key_points' list cannot be empty"
            print("  ✓ PASS - Explanation structure valid")
            return True
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        return False


def test_explain_image() -> bool:
    url = f"{BASE_URL}/api/explain"
    img_path = os.path.join(SAMPLES_DIR, "physics_newton_law.jpg")
    print(f"\n[3/5] Testing POST {url} (Multimodal Image Upload) ...")
    if not os.path.isfile(img_path):
        print(f"  - SKIP: Image file {img_path} not found")
        return True

    with open(img_path, "rb") as f:
        img_bytes = f.read()

    boundary = "----WebKitFormBoundaryDoubtLensImageTest"
    header = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="image"; filename="physics_newton_law.jpg"\r\n'
        "Content-Type: image/jpeg\r\n\r\n"
    ).encode("utf-8")
    middle = (
        f"\r\n--{boundary}\r\n"
        'Content-Disposition: form-data; name="question"\r\n\r\n'
        "Explain step by step how to solve this textbook problem\r\n"
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="language"\r\n\r\n'
        "en\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    body = header + img_bytes + middle

    try:
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = resp.status
            data = json.loads(resp.read().decode("utf-8"))
            print(f"  Status: {status}, Topic: {data.get('topic')}")
            assert status == 200, f"Expected 200, got {status}"
            assert "steps" in data and len(data["steps"]) >= 1
            print("  ✓ PASS - Multimodal image processing successful")
            return True
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        return False


def test_quiz() -> bool:
    url = f"{BASE_URL}/api/quiz"
    print(f"\n[4/5] Testing POST {url} (5-Question Multiple Choice Quiz) ...")
    payload = json.dumps({
        "topic": "Newton's Second Law",
        "explanation": "Net force equals mass times acceleration (F=ma). Friction opposes motion.",
        "language": "en"
    }).encode("utf-8")

    try:
        req = urllib.request.Request(
            url,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            status = resp.status
            data = json.loads(resp.read().decode("utf-8"))
            print(f"  Status: {status}")
            assert status == 200, f"Expected 200, got {status}"
            assert "questions" in data and isinstance(data["questions"], list), "Missing 'questions' list"
            questions = data["questions"]
            assert len(questions) == 5, f"Contract requires EXACTLY 5 questions, got {len(questions)}"

            for i, q in enumerate(questions):
                assert "q" in q and isinstance(q["q"], str), f"Q{i+1}: Missing 'q'"
                assert "options" in q and isinstance(q["options"], list), f"Q{i+1}: Missing 'options'"
                assert len(q["options"]) == 4, f"Q{i+1}: Expected exactly 4 options, got {len(q['options'])}"
                assert "answer_index" in q and isinstance(q["answer_index"], int), f"Q{i+1}: Missing 'answer_index'"
                assert 0 <= q["answer_index"] <= 3, f"Q{i+1}: answer_index must be 0-3, got {q['answer_index']}"
                assert "why" in q and isinstance(q["why"], str), f"Q{i+1}: Missing 'why'"

            print(f"  ✓ PASS - All 5 questions strictly conform to API contract")
            return True
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        return False


def test_error_empty() -> bool:
    url = f"{BASE_URL}/api/explain"
    print(f"\n[5/5] Testing POST {url} (Validation: Empty Input -> 400) ...")
    boundary = "----WebKitFormBoundaryDoubtLensEmptyTest"
    body = (
        f"--{boundary}\r\n"
        'Content-Disposition: form-data; name="language"\r\n\r\n'
        "en\r\n"
        f"--{boundary}--\r\n"
    ).encode("utf-8")

    try:
        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
            method="POST",
        )
        urllib.request.urlopen(req, timeout=5)
        print("  ✗ FAIL: Expected HTTP 400 error, but request succeeded!")
        return False
    except urllib.error.HTTPError as err:
        print(f"  Received HTTP Status: {err.code} (Expected: 400)")
        if err.code == 400:
            err_data = json.loads(err.read().decode("utf-8"))
            assert "error" in err_data, "Error response must contain 'error' field"
            print(f"  ✓ PASS - Properly returned 400 Bad Request with message: '{err_data['error']}'")
            return True
        else:
            print(f"  ✗ FAIL - Unexpected status code: {err.code}")
            return False
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        return False


def main():
    print_header("DoubtLens API Contract Test Runner")
    print(f"Targeting server: {BASE_URL}")
    print("Checking if server is reachable...")

    tests = [
        ("Health Check", test_health),
        ("Explain Doubt (Text)", test_explain_text),
        ("Explain Doubt (Image)", test_explain_image),
        ("Quiz Generation", test_quiz),
        ("Empty Input Validation", test_error_empty),
    ]

    results = []
    for name, test_func in tests:
        success = test_func()
        results.append((name, success))

    print_header("Test Execution Summary")
    all_passed = True
    for name, success in results:
        status_str = "PASS ✓" if success else "FAIL ✗"
        print(f"  {name.ljust(35)}: {status_str}")
        if not success:
            all_passed = False

    print("\n" + "-" * 60)
    if all_passed:
        print("🎉 All API Contract Tests Passed Successfully!")
        sys.exit(0)
    else:
        print("⚠️ One or more tests failed. Check DoubtLens server logs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
