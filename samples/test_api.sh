#!/usr/bin/env bash
# ==============================================================================
# DoubtLens API Verification Script
# Hacktoberfest Hack Day Delhi x SKILLOP DTU (MLH)
#
# Validates the frozen API contract for DoubtLens:
#   1. GET /api/health
#   2. POST /api/explain (text only, image only, image+text, Hindi)
#   3. POST /api/quiz (5 questions schema)
#   4. Error handling (missing input -> 400)
# ==============================================================================

PORT="${PORT:-5000}"
BASE_URL="http://127.0.0.1:${PORT}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SAMPLE_IMG="${SCRIPT_DIR}/physics_newton_law.jpg"

GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================================${NC}"
echo -e "${BLUE}        🔍 DoubtLens API Test Suite                   ${NC}"
echo -e "${BLUE}        Target Server: ${BASE_URL}                   ${NC}"
echo -e "${BLUE}======================================================${NC}"

TOTAL_TESTS=0
PASSED_TESTS=0

run_test() {
  local name="$1"
  local cmd="$2"
  local expected_status="$3"
  local check_string="$4"

  TOTAL_TESTS=$((TOTAL_TESTS + 1))
  echo -e "\n${YELLOW}Test #${TOTAL_TESTS}: ${name}${NC}"

  # Execute command and capture response + HTTP status
  local response_file
  response_file=$(mktemp)
  local http_code
  http_code=$(eval "${cmd}" -s -w "%{http_code}" -o "${response_file}")

  local body
  body=$(cat "${response_file}")
  rm -f "${response_file}"

  echo "  HTTP Status: ${http_code} (Expected: ${expected_status})"

  if [ "${http_code}" -ne "${expected_status}" ]; then
    echo -e "  ${RED}FAILED: Status code mismatch!${NC}"
    echo "  Response body: ${body}"
    return 1
  fi

  if [ -n "${check_string}" ]; then
    if echo "${body}" | grep -q "${check_string}"; then
      echo -e "  Content Check: Contains '${check_string}' ${GREEN}✓${NC}"
    else
      echo -e "  ${RED}FAILED: Missing expected content '${check_string}'${NC}"
      echo "  Response body: ${body}"
      return 1
    fi
  fi

  echo -e "  ${GREEN}PASSED ✓${NC}"
  PASSED_TESTS=$((PASSED_TESTS + 1))
  return 0
}

# 1. Health check
run_test "GET /api/health" \
  "curl -X GET '${BASE_URL}/api/health'" \
  200 \
  '"status":"ok"'

# 2. Text-only explain (English)
run_test "POST /api/explain (Text-only, English)" \
  "curl -X POST '${BASE_URL}/api/explain' -F 'question=What is Newton Second Law?' -F 'language=en' -F 'level=simple'" \
  200 \
  '"topic"'

# 3. Multimodal explain with image
if [ -f "${SAMPLE_IMG}" ]; then
  run_test "POST /api/explain (Image upload, Newton's Law)" \
    "curl -X POST '${BASE_URL}/api/explain' -F 'image=@${SAMPLE_IMG}' -F 'question=Solve problem 4.2' -F 'language=en'" \
    200 \
    '"steps"'
else
  echo -e "${YELLOW}Skipping image test: ${SAMPLE_IMG} not found${NC}"
fi

# 4. Multimodal explain in Hindi
run_test "POST /api/explain (Language: Hindi)" \
  "curl -X POST '${BASE_URL}/api/explain' -F 'question=न्यूटन का दूसरा नियम क्या है?' -F 'language=hi'" \
  200 \
  '"key_points"'

# 5. Quiz Generation
QUIZ_PAYLOAD='{"topic":"Newton Second Law","explanation":"F=ma governs acceleration.","language":"en"}'
run_test "POST /api/quiz (Generate 5-question multiple choice quiz)" \
  "curl -X POST '${BASE_URL}/api/quiz' -H 'Content-Type: application/json' -d '${QUIZ_PAYLOAD}'" \
  200 \
  '"questions"'

# 6. Error handling: Empty request (neither image nor question provided)
run_test "POST /api/explain (Error handling: 400 Bad Request on empty input)" \
  "curl -X POST '${BASE_URL}/api/explain' -F 'language=en'" \
  400 \
  '"error"'

echo -e "\n${BLUE}======================================================${NC}"
echo -e "Test Summary: ${GREEN}${PASSED_TESTS}/${TOTAL_TESTS} tests passed.${NC}"
if [ "${PASSED_TESTS}" -eq "${TOTAL_TESTS}" ]; then
  echo -e "${GREEN}🎉 All API contract verification tests passed!${NC}"
  exit 0
else
  echo -e "${RED}⚠️ Some tests failed. Ensure DoubtLens server is running at ${BASE_URL}.${NC}"
  exit 1
fi
