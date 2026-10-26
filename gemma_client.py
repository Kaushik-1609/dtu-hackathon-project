"""gemma_client.py - AI client for DoubtLens using Google Gemma 4 via Google GenAI SDK.

Handles multimodal explanation (image + text) and quiz generation.
Supports MOCK mode (MOCK=1) for offline development and testing.
"""

import os
import re
import json
import logging
from typing import Optional, Dict, Any, List

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)

# Model configuration
DEFAULT_MODEL = "gemma-4-31b-it"


# ---------------------------------------------------------------------------
# MOCK DATA
# ---------------------------------------------------------------------------

MOCK_EXPLAIN_EN = {
    "topic": "Newton's Second Law",
    "explanation": (
        "Newton's Second Law of Motion describes how the velocity of an object "
        "changes when it is subjected to an external force. It states that the "
        "rate of change of momentum of a body is directly proportional to the "
        "applied force and takes place in the direction in which the force acts (F = ma)."
    ),
    "steps": [
        "Identify the Net Force: Force is any interaction that, when unopposed, changes the motion of an object.",
        "Determine the Mass: Mass is the amount of matter in the object, representing its resistance to acceleration (inertia).",
        "Observe the Acceleration: Acceleration measures how quickly velocity changes over time in response to the force.",
        "Apply the Equation F = ma: Multiply the mass by acceleration to calculate the total required net force."
    ],
    "key_points": [
        "The mathematical formula is F = ma (Force = mass × acceleration).",
        "Heavier objects require greater force to achieve the same rate of acceleration.",
        "The SI unit of force is the Newton (N), where 1 N = 1 kg·m/s²."
    ]
}

MOCK_EXPLAIN_HI = {
    "topic": "Newton's Second Law",
    "explanation": (
        "न्यूटन का दूसरा गति नियम बताता है कि किसी वस्तु के संवेग में परिवर्तन की दर "
        "उस पर लगाए गए कुल बल के समानुपाती होती है और उसी दिशा में होती है (F = ma)। "
        "सरल शब्दों में, किसी वस्तु को गति देने के लिए लगाया गया बल उसके द्रव्यमान और त्वरण पर निर्भर करता है।"
    ),
    "steps": [
        "कुल बल को समझें: बल वह खिंचाव या धक्का है जो किसी वस्तु की गति की स्थिति को बदलता है।",
        "द्रव्यमान की पहचान करें: द्रव्यमान वस्तु में मौजूद पदार्थ की मात्रा है जो गति परिवर्तन का विरोध करता है।",
        "त्वरण की गणना करें: त्वरण वह दर है जिससे समय के साथ वस्तु का वेग बदलता है।",
        "सूत्र F = ma लागू करें: आवश्यक कुल बल निकालने के लिए द्रव्यमान को त्वरण से गुणा करें।"
    ],
    "key_points": [
        "गणितीय सूत्र F = ma है (बल = द्रव्यमान × त्वरण)।",
        "समान त्वरण पाने के लिए भारी वस्तु पर अधिक बल लगाना आवश्यक होता है।",
        "बल का SI मात्रक न्यूटन (N) है, जहाँ 1 N = 1 kg·m/s² होता है।"
    ]
}

MOCK_QUIZ_EN: List[Dict[str, Any]] = [
    {
        "q": "What is the primary equation representing Newton's Second Law of Motion?",
        "options": [
            "E = mc²",
            "F = ma",
            "v = u + at",
            "p = mv"
        ],
        "answer_index": 1,
        "why": "Newton's Second Law defines force as the product of mass and acceleration (F = ma)."
    },
    {
        "q": "If the net force acting on an object is doubled while keeping its mass constant, what happens to acceleration?",
        "options": [
            "It is halved",
            "It remains unchanged",
            "It is doubled",
            "It is quadrupled"
        ],
        "answer_index": 2,
        "why": "Acceleration is directly proportional to net force (a = F/m)."
    },
    {
        "q": "What is the standard SI unit of force?",
        "options": [
            "Joule",
            "Watt",
            "Newton",
            "Pascal"
        ],
        "answer_index": 2,
        "why": "Force is measured in Newtons (N) in the International System of Units."
    },
    {
        "q": "If two objects with different masses experience the exact same net force, which one accelerates faster?",
        "options": [
            "The heavier object",
            "The lighter object",
            "Both accelerate at the same rate",
            "Neither object accelerates"
        ],
        "answer_index": 1,
        "why": "Acceleration is inversely proportional to mass, so the lighter object experiences greater acceleration."
    },
    {
        "q": "How much force is required to accelerate a 3 kg mass at 4 m/s²?",
        "options": [
            "7 N",
            "1 N",
            "12 N",
            "0.75 N"
        ],
        "answer_index": 2,
        "why": "Using F = ma, 3 kg × 4 m/s² = 12 N."
    }
]

MOCK_QUIZ_HI: List[Dict[str, Any]] = [
    {
        "q": "न्यूटन के द्वितीय गति नियम का प्राथमिक गणितीय समीकरण क्या है?",
        "options": [
            "E = mc²",
            "F = ma",
            "v = u + at",
            "p = mv"
        ],
        "answer_index": 1,
        "why": "न्यूटन का दूसरा नियम बल को द्रव्यमान और त्वरण के गुणनफल (F = ma) के रूप में परिभाषित करता है।"
    },
    {
        "q": "यदि किसी वस्तु पर लगने वाले बल को दोगुना कर दिया जाए और द्रव्यमान स्थिर रहे, तो त्वरण क्या होगा?",
        "options": [
            "आधा हो जाएगा",
            "अपरिवर्तित रहेगा",
            "दोगुना हो जाएगा",
            "चार गुना हो जाएगा"
        ],
        "answer_index": 2,
        "why": "त्वरण लगाए गए बल के सीधे समानुपाती होता है (a = F/m)।"
    },
    {
        "q": "बल का मानक SI मात्रक क्या है?",
        "options": [
            "जूल",
            "वाट",
            "न्यूटन",
            "पास्कल"
        ],
        "answer_index": 2,
        "why": "अंतर्राष्ट्रीय मात्रक प्रणाली (SI) में बल को न्यूटन (N) में मापा जाता है।"
    },
    {
        "q": "यदि भिन्न द्रव्यमान वाली दो वस्तुओं पर समान बल लगाया जाए, तो किसका त्वरण अधिक होगा?",
        "options": [
            "भारी वस्तु का",
            "हल्की वस्तु का",
            "दोनों का त्वरण समान होगा",
            "किसी का भी त्वरण नहीं होगा"
        ],
        "answer_index": 1,
        "why": "त्वरण द्रव्यमान के व्युत्क्रमानुपाती होता है, इसलिए हल्की वस्तु अधिक तेजी से त्वरित होगी।"
    },
    {
        "q": "3 किलोग्राम द्रव्यमान की वस्तु को 4 m/s² से त्वरित करने के लिए कितने बल की आवश्यकता होगी?",
        "options": [
            "7 N",
            "1 N",
            "12 N",
            "0.75 N"
        ],
        "answer_index": 2,
        "why": "F = ma के अनुसार: 3 kg × 4 m/s² = 12 N।"
    }
]


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def is_mock_enabled() -> bool:
    """Return True if MOCK environment variable is set to '1'."""
    return os.environ.get("MOCK", "").strip() == "1"


def get_model_name() -> str:
    """Get configured model name with default to gemma-4-31b-it."""
    return os.environ.get("GEMMA_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def get_genai_client():
    """Initialize and return google-genai Client."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is missing. "
            "Please configure GEMINI_API_KEY or set MOCK=1 to test with fake data."
        )

    try:
        from google import genai
        return genai.Client(api_key=api_key)
    except ImportError as e:
        logger.error("google-genai package not found: %s", e)
        raise RuntimeError(
            "google-genai library is not installed. Run `pip install google-genai`."
        ) from e


def extract_json_from_response(text: str) -> Any:
    """Safely extracts JSON from model text output, stripping markdown formatting if present."""
    clean_text = text.strip()

    # Match JSON wrapped inside markdown code blocks
    markdown_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", clean_text)
    if markdown_match:
        clean_text = markdown_match.group(1).strip()

    # Isolate JSON object or array
    first_brace = clean_text.find("{")
    last_brace = clean_text.rfind("}")
    first_bracket = clean_text.find("[")
    last_bracket = clean_text.rfind("]")

    if first_brace != -1 and last_brace != -1 and (first_bracket == -1 or first_brace < first_bracket):
        clean_text = clean_text[first_brace:last_brace + 1]
    elif first_bracket != -1 and last_bracket != -1:
        clean_text = clean_text[first_bracket:last_bracket + 1]

    return json.loads(clean_text)


# ---------------------------------------------------------------------------
# CORE CLIENT API
# ---------------------------------------------------------------------------

def explain_doubt(
    question: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    image_mime_type: Optional[str] = None,
    language: str = "en",
    level: str = "simple"
) -> Dict[str, Any]:
    """Explain a doubt using multimodal Gemma 4 or mock response.

    Args:
        question: Optional user typed question string.
        image_bytes: Optional raw image bytes.
        image_mime_type: Optional image MIME type (e.g. image/png, image/jpeg, image/webp).
        language: 'en' for English, 'hi' for Hindi (default 'en').
        level: 'simple' or 'detailed' (default 'simple').

    Returns:
        dict: {"topic": str, "explanation": str, "steps": [str], "key_points": [str]}
    """
    lang = "hi" if language == "hi" else "en"
    complexity = "detailed" if level == "detailed" else "simple"

    # 1. Return mock data if MOCK=1 is configured
    if is_mock_enabled():
        logger.info("MOCK=1: Returning mock explanation (lang=%s)", lang)
        if lang == "hi":
            return dict(MOCK_EXPLAIN_HI)
        return dict(MOCK_EXPLAIN_EN)

    # 2. Call Google GenAI with Gemma 4
    client = get_genai_client()
    model_name = get_model_name()

    lang_desc = "Hindi (हिंदी)" if lang == "hi" else "English"
    depth_desc = (
        "provide an in-depth, thorough explanation with relevant concepts"
        if complexity == "detailed"
        else "provide a crystal clear, simple, student-friendly explanation"
    )

    system_instruction = (
        f"You are DoubtLens, a patient and encouraging AI teacher powered by Gemma 4. "
        f"Your goal is to help students learn by analyzing textbook pages, handwritten problems, diagrams, "
        f"or typed questions.\n\n"
        f"Instructions:\n"
        f"1. Explain the doubt in {lang_desc}.\n"
        f"2. Complexity: {depth_desc}.\n"
        f"3. Provide exactly:\n"
        f"   - 'topic': Concise name of the topic or concept.\n"
        f"   - 'explanation': Clear explanation paragraph.\n"
        f"   - 'steps': A list of sequential, easy-to-follow steps (minimum 3 steps).\n"
        f"   - 'key_points': A list of key takeaways or formulas to remember (minimum 2 points).\n"
        f"4. You MUST reply ONLY with a valid JSON object matching this exact schema:\n"
        f"   {{\n"
        f'     "topic": "string",\n'
        f'     "explanation": "string",\n'
        f'     "steps": ["step 1", "step 2", ...],\n'
        f'     "key_points": ["point 1", "point 2", ...]\n'
        f"   }}\n"
        f"Do not include any text, markdown commentary, or explanations outside the JSON."
    )

    contents: List[Any] = []

    # Attach image part if present
    if image_bytes and image_mime_type:
        from google.genai import types
        contents.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_mime_type
            )
        )

    # Attach prompt text
    user_prompt = ""
    if question:
        user_prompt += f"Student Question: {question}\n"
    if image_bytes:
        user_prompt += "Please inspect the uploaded image and solve/explain the problem shown.\n"
    user_prompt += f"Remember to output in {lang_desc} as valid JSON."

    contents.append(user_prompt)

    try:
        from google.genai import types
        # Attempt request with JSON response formatting
        response = client.models.generate_content(
            model=model_name,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,
                response_mime_type="application/json"
            )
        )
    except Exception as exc:
        logger.warning("Generate content with response_mime_type failed, retrying standard call: %s", exc)
        # Fallback to standard request if model rejects response_mime_type
        prompt_with_instructions = f"{system_instruction}\n\n{user_prompt}"
        fallback_contents: List[Any] = []
        if image_bytes and image_mime_type:
            from google.genai import types
            fallback_contents.append(
                types.Part.from_bytes(data=image_bytes, mime_type=image_mime_type)
            )
        fallback_contents.append(prompt_with_instructions)
        response = client.models.generate_content(
            model=model_name,
            contents=fallback_contents
        )

    response_text = response.text or ""
    parsed = extract_json_from_response(response_text)

    # Validate and structure data according to contract
    topic = str(parsed.get("topic", "Doubt Explanation")).strip() or "Doubt Explanation"
    explanation = str(parsed.get("explanation", "")).strip()
    steps = [str(s).strip() for s in parsed.get("steps", []) if str(s).strip()]
    key_points = [str(kp).strip() for kp in parsed.get("key_points", []) if str(kp).strip()]

    if not explanation and steps:
        explanation = steps[0]

    return {
        "topic": topic,
        "explanation": explanation,
        "steps": steps,
        "key_points": key_points
    }


def generate_quiz(
    topic: str,
    explanation: str,
    language: str = "en"
) -> Dict[str, Any]:
    """Generate a 5-question multiple-choice quiz on the topic.

    Args:
        topic: Concept topic name.
        explanation: The explanation previously given to the student.
        language: 'en' for English, 'hi' for Hindi (default 'en').

    Returns:
        dict: {"questions": [{"q": str, "options": [str, str, str, str], "answer_index": int, "why": str}]}
              (Contains exactly 5 questions)
    """
    lang = "hi" if language == "hi" else "en"

    # 1. Return mock data if MOCK=1 is configured
    if is_mock_enabled():
        logger.info("MOCK=1: Returning mock quiz (lang=%s)", lang)
        if lang == "hi":
            return {"questions": list(MOCK_QUIZ_HI)}
        return {"questions": list(MOCK_QUIZ_EN)}

    # 2. Call Google GenAI with Gemma 4
    client = get_genai_client()
    model_name = get_model_name()

    lang_desc = "Hindi (हिंदी)" if lang == "hi" else "English"

    system_instruction = (
        f"You are DoubtLens Quiz Master powered by Gemma 4. "
        f"Create an engaging, accurate 5-question multiple-choice quiz based on the student's topic and explanation.\n\n"
        f"Rules:\n"
        f"1. Generate EXACTLY 5 questions.\n"
        f"2. Language: {lang_desc}.\n"
        f"3. Each question must have EXACTLY 4 plausible options.\n"
        f"4. 'answer_index' must be an integer from 0 to 3 pointing to the correct option.\n"
        f"5. 'why' must be a concise, one-line explanation of why that option is correct.\n"
        f"6. Output ONLY valid JSON in this exact structure:\n"
        f"   {{\n"
        f'     "questions": [\n'
        f"       {{\n"
        f'         "q": "Question text here?",\n'
        f'         "options": ["Option A", "Option B", "Option C", "Option D"],\n'
        f'         "answer_index": 0,\n'
        f'         "why": "One-line rationale."\n'
        f"       }}\n"
        f"     ]\n"
        f"   }}\n"
        f"Do not include any other markdown text or comments."
    )

    prompt = (
        f"Topic: {topic}\n"
        f"Explanation: {explanation}\n\n"
        f"Please generate the 5-question quiz in {lang_desc} as instructed."
    )

    try:
        from google.genai import types
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3,
                response_mime_type="application/json"
            )
        )
    except Exception as exc:
        logger.warning("Generate quiz with response_mime_type failed, retrying standard call: %s", exc)
        prompt_with_instructions = f"{system_instruction}\n\n{prompt}"
        response = client.models.generate_content(
            model=model_name,
            contents=[prompt_with_instructions]
        )

    response_text = response.text or ""
    parsed = extract_json_from_response(response_text)

    raw_questions = parsed.get("questions", []) if isinstance(parsed, dict) else parsed
    if not isinstance(raw_questions, list):
        raw_questions = []

    validated_questions: List[Dict[str, Any]] = []
    for item in raw_questions:
        if not isinstance(item, dict):
            continue
        q = str(item.get("q", "")).strip()
        options = [str(opt).strip() for opt in item.get("options", []) if str(opt).strip()]
        why = str(item.get("why", "")).strip()
        answer_idx = item.get("answer_index", 0)

        try:
            answer_idx = int(answer_idx)
        except (ValueError, TypeError):
            answer_idx = 0

        # Validate structure
        if q and len(options) == 4 and 0 <= answer_idx <= 3:
            validated_questions.append({
                "q": q,
                "options": options,
                "answer_index": answer_idx,
                "why": why or "Correct answer based on the lesson."
            })

    # Ensure EXACTLY 5 questions as per API contract
    if len(validated_questions) < 5:
        # Fall back / pad with mock questions if model produced fewer than 5
        fallback = MOCK_QUIZ_HI if lang == "hi" else MOCK_QUIZ_EN
        for fb in fallback:
            if len(validated_questions) >= 5:
                break
            validated_questions.append(dict(fb))
    elif len(validated_questions) > 5:
        validated_questions = validated_questions[:5]

    return {"questions": validated_questions}
