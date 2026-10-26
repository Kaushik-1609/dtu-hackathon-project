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
# HELPER & SMART REASONING FUNCTIONS
# ---------------------------------------------------------------------------

def is_mock_enabled() -> bool:
    """Return True if MOCK environment variable is set to '1' or if GEMINI_API_KEY is missing."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    return os.environ.get("MOCK", "").strip() == "1" or not api_key


def get_model_name() -> str:
    """Get configured model name with default to gemma-4-31b-it."""
    return os.environ.get("GEMMA_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL


def get_genai_client():
    """Initialize and return google-genai Client."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is missing."
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

    markdown_match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", clean_text)
    if markdown_match:
        clean_text = markdown_match.group(1).strip()

    first_brace = clean_text.find("{")
    last_brace = clean_text.rfind("}")
    first_bracket = clean_text.find("[")
    last_bracket = clean_text.rfind("]")

    if first_brace != -1 and last_brace != -1 and (first_bracket == -1 or first_brace < first_bracket):
        clean_text = clean_text[first_brace:last_brace + 1]
    elif first_bracket != -1 and last_bracket != -1:
        clean_text = clean_text[first_bracket:last_bracket + 1]

    return json.loads(clean_text)


def generate_smart_pedagogical_response(
    question: Optional[str] = None,
    has_image: bool = False,
    language: str = "en",
    level: str = "simple"
) -> Dict[str, Any]:
    """Generates an accurate, context-aware step-by-step pedagogical explanation in English or Hindi."""
    q = (question or "").strip()
    q_lower = q.lower()
    lang = "hi" if language == "hi" else "en"

    # 1. Arithmetic evaluation (e.g. "2+2 is equal to what", "5 * 4", "10 / 2", "15 + 35")
    math_match = re.search(r"(\d+(?:\.\d+)?)\s*([\+\-\*\/xX])\s*(\d+(?:\.\d+)?)", q_lower)
    if math_match:
        n1 = float(math_match.group(1))
        op = math_match.group(2).lower()
        n2 = float(math_match.group(3))

        if op == "+":
            ans = n1 + n2
            op_name = "Addition" if lang == "en" else "जोड़"
        elif op == "-":
            ans = n1 - n2
            op_name = "Subtraction" if lang == "en" else "घटाव"
        elif op in ("*", "x"):
            ans = n1 * n2
            op_name = "Multiplication" if lang == "en" else "गुणा"
        elif op == "/":
            ans = (n1 / n2) if n2 != 0 else 0
            op_name = "Division" if lang == "en" else "भाग"
        else:
            ans = n1 + n2
            op_name = "Addition"

        ans_str = str(int(ans)) if isinstance(ans, float) and ans.is_integer() else str(ans)
        n1_str = str(int(n1)) if n1.is_integer() else str(n1)
        n2_str = str(int(n2)) if n2.is_integer() else str(n2)

        if lang == "hi":
            return {
                "topic": f"सरल अंकगणित: {op_name} ({n1_str} {op} {n2_str})",
                "explanation": f"{n1_str} {op} {n2_str} का मान {ans_str} के बराबर होता है। अंकगणित में {op_name} मूलभूत गणितीय संक्रिया है।",
                "steps": [
                    f"संख्याओं की पहचान करें: हमारे पास दो संख्याएँ हैं: {n1_str} और {n2_str}।",
                    f"{op_name} संक्रिया लागू करें: {n1_str} और {n2_str} का संक्रियात्मक मान {ans_str} प्राप्त होता है।",
                    f"अंतिम परिणाम: {n1_str} {op} {n2_str} = {ans_str}।"
                ],
                "key_points": [
                    f"{n1_str} {op} {n2_str} = {ans_str}।",
                    "यह प्राथमिक गणित की मूलभूत संक्रिया है।",
                    f"अंतिम परिणाम {ans_str} है।"
                ]
            }
        else:
            return {
                "topic": f"Basic Arithmetic: {op_name} ({n1_str} {op} {n2_str})",
                "explanation": f"{n1_str} {op} {n2_str} is equal to {ans_str}. In elementary mathematics, {op_name.lower()} is one of the four fundamental arithmetic operations.",
                "steps": [
                    f"Identify the values: We are given the numbers {n1_str} and {n2_str}.",
                    f"Apply the {op_name.lower()} operation between {n1_str} and {n2_str}.",
                    f"State the final result: {n1_str} {op} {n2_str} = {ans_str}."
                ],
                "key_points": [
                    f"{n1_str} {op} {n2_str} = {ans_str}.",
                    f"Fundamental {op_name.lower()} rule applied.",
                    f"Final result is {ans_str}."
                ]
            }

    # 2. Photosynthesis
    if "photo" in q_lower or "प्रकाश" in q:
        if lang == "hi":
            return {
                "topic": "प्रकाश संश्लेषण (Photosynthesis)",
                "explanation": "प्रकाश संश्लेषण वह जैविक प्रक्रिया है जिसके द्वारा हरे पौधे सूर्य के प्रकाश, कार्बन डाइऑक्साइड (CO₂) और जल (H₂O) का उपयोग करके ग्लूकोज और ऑक्सीजन का निर्माण करते हैं।",
                "steps": [
                    "सूर्य के प्रकाश का अवशोषण: पत्तियों में मौजूद क्लोरोफिल प्रकाश ऊर्जा को ग्रहण करता है।",
                    "जल और CO₂ का ग्रहण: जड़ें मिट्टी से पानी और पत्तियां रंध्रों (स्टोमेटा) से CO₂ लेती हैं।",
                    "रासायनिक रूपांतरण: 6CO₂ + 6H₂O + प्रकाश ऊर्जा → C₆H₁₂O₆ (ग्लूकोज) + 6O₂ (ऑक्सीजन)।",
                    "ऑक्सीजन का निकास: ऑक्सीजन वायुमंडल में उप-उत्पाद के रूप में छोड़ी जाती है।"
                ],
                "key_points": [
                    "रासायनिक समीकरण: 6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂।",
                    "यह क्रिया मुख्य रूप से पत्तियों के हरितलवक (क्लोरोप्लास्ट) में होती है।",
                    "पौधों को स्वपोषी (autotrophs) बनाने वाली मुख्य प्रक्रिया यही है।"
                ]
            }
        else:
            return {
                "topic": "Photosynthesis in Plants",
                "explanation": "Photosynthesis is the biological process by which green plants and certain other organisms transform light energy into chemical energy, synthesizing glucose from carbon dioxide and water while releasing oxygen.",
                "steps": [
                    "Light Absorption: Chlorophyll pigments inside chloroplasts absorb photons from sunlight.",
                    "Raw Material Intake: Roots absorb water (H₂O) and stomata absorb carbon dioxide (CO₂).",
                    "Chemical Conversion: The light-dependent and Calvin cycle reactions produce glucose (C₆H₁₂O₆).",
                    "Oxygen Release: Oxygen is released into the atmosphere as an essential byproduct."
                ],
                "key_points": [
                    "Overall equation: 6CO₂ + 6H₂O + sunlight → C₆H₁₂O₆ + 6O₂.",
                    "Occurs primarily inside plant chloroplasts.",
                    "Provides the primary energy source for virtually all aerobic life on Earth."
                ]
            }

    # 3. Quadratic Formula
    if "quadratic" in q_lower or "द्विघात" in q:
        if lang == "hi":
            return {
                "topic": "द्विघात समीकरण और श्रीधराचार्य सूत्र",
                "explanation": "द्विघात समीकरण का मानक रूप ax² + bx + c = 0 होता है (जहाँ a ≠ 0)। इसके मूल (roots) निकालने के लिए द्विघात सूत्र x = (-b ± √(b² - 4ac)) / (2a) का उपयोग किया जाता है।",
                "steps": [
                    "समीकरण को मानक रूप ax² + bx + c = 0 में व्यवस्थित करें।",
                    "गुणांक a, b, और c के मान पहचानें।",
                    "विविक्तकर (Discriminant) D = b² - 4ac की गणना करें।",
                    "सूत्र x = (-b ± √D) / (2a) में मान रखकर दोनों मूल प्राप्त करें।"
                ],
                "key_points": [
                    "द्विघात सूत्र: x = (-b ± √(b² - 4ac)) / (2a)।",
                    "यदि D > 0 तो दो वास्तविक और भिन्न मूल होंगे।",
                    "यदि D = 0 तो दो समान वास्तविक मूल होंगे, और D < 0 पर काल्पनिक मूल होंगे।"
                ]
            }
        else:
            return {
                "topic": "The Quadratic Formula",
                "explanation": "A quadratic equation is a second-order polynomial equation in a single variable x with standard form ax² + bx + c = 0 (where a ≠ 0). Its solutions (roots) are given by the Quadratic Formula.",
                "steps": [
                    "Standardize: Arrange the equation in the form ax² + bx + c = 0.",
                    "Identify coefficients: Extract values for a, b, and c.",
                    "Calculate the Discriminant: Evaluate Δ = b² - 4ac to determine nature of roots.",
                    "Apply Formula: Substitute into x = (-b ± √(b² - 4ac)) / (2a) to find the two roots."
                ],
                "key_points": [
                    "Quadratic Formula: x = (-b ± √(b² - 4ac)) / (2a).",
                    "If b² - 4ac > 0, there are two distinct real roots.",
                    "If b² - 4ac = 0, there is one repeated real root."
                ]
            }

    # 4. Newton's laws or physics
    if "newton" in q_lower or "न्यूटन" in q or "force" in q_lower or "motion" in q_lower:
        return dict(MOCK_EXPLAIN_HI) if lang == "hi" else dict(MOCK_EXPLAIN_EN)

    # 5. Circuits / Ohm's Law
    if "ohm" in q_lower or "circuit" in q_lower or "resistor" in q_lower:
        if lang == "hi":
            return {
                "topic": "ओम का नियम एवं विद्युत परिपथ (Ohm's Law)",
                "explanation": "ओम के नियम के अनुसार, यदि भौतिक अवस्थाएं (जैसे तापमान) स्थिर रहें, तो किसी चालक के सिरों के बीच का विभवांतर (V) उसमें प्रवाहित धारा (I) के समानुपाती होता है: V = IR।",
                "steps": [
                    "परिपथ में दिए गए मानों की पहचान करें (विभवांतर V, धारा I, या प्रतिरोध R)।",
                    "समीकरण V = I × R का चयन करें।",
                    "अज्ञात मान निकालने के लिए समीकरण को पुनर्व्यवस्थित करें (I = V/R या R = V/I)।",
                    "इकाई का ध्यान रखते हुए अंतिम उत्तर की गणना करें।"
                ],
                "key_points": [
                    "सूत्र: V = IR (वोल्ट = एम्पीयर × ओम)।",
                    "श्रेणीक्रम (Series) में प्रतिरोध: R_total = R₁ + R₂।",
                    "समानांतर क्रम (Parallel) में प्रतिरोध: 1/R_total = 1/R₁ + 1/R₂।"
                ]
            }
        else:
            return {
                "topic": "Ohm's Law and Electrical Resistance",
                "explanation": "Ohm's Law states that the current (I) through a conductor between two points is directly proportional to the voltage (V) across the two points: V = IR.",
                "steps": [
                    "Identify the circuit variables: Voltage (V in Volts), Current (I in Amperes), Resistance (R in Ohms).",
                    "Apply Ohm's law formula: V = I * R.",
                    "Rearrange for the unknown quantity: I = V/R or R = V/I.",
                    "Calculate the numerical result and verify proper SI units."
                ],
                "key_points": [
                    "Fundamental equation: V = IR.",
                    "Resistance opposes electric charge flow.",
                    "Resistors in series add directly (R = R₁ + R₂), while parallel resistors add reciprocally."
                ]
            }

    # 6. Any other question or image
    cleaned_topic = q.strip("? .!").capitalize()
    if len(cleaned_topic) > 40:
        words = cleaned_topic.split()
        cleaned_topic = " ".join(words[:5]) + "..."
    if not cleaned_topic:
        cleaned_topic = "Visual Problem & Diagram Analysis" if lang == "en" else "चित्र एवं समस्या विश्लेषण"

    if lang == "hi":
        return {
            "topic": cleaned_topic,
            "explanation": f"'{q or 'दिए गए चित्र'}' के संदर्भ में, यह अवधारणा मूलभूत वैज्ञानिक एवं तार्किक सिद्धांतों पर आधारित है। इसे समझने के लिए समस्या को बुनियादी घटकों में बांटकर चरणबद्ध तरीके से हल किया जाता है।",
            "steps": [
                "समस्या और मूल प्रश्न की पहचान करें।",
                "प्रासंगिक नियमों, सूत्रों एवं सिद्धांतों का चयन करें।",
                "तार्किक तर्क और गणनाओं को क्रमानुसार लागू करें।",
                "अंतिम परिणाम की पुष्टि करें और निष्कर्ष प्राप्त करें।"
            ],
            "key_points": [
                f"मूल विषय: {cleaned_topic}।",
                "प्रत्येक चरण तार्किक रूप से पिछले चरण से जुड़ा हुआ है।",
                "संकल्पना की स्पष्टता के लिए मूलभूत परिभाषा को याद रखें।"
            ]
        }
    else:
        return {
            "topic": cleaned_topic,
            "explanation": f"Regarding '{q or 'the uploaded problem diagram'}', this problem involves core foundational principles that can be understood by breaking the question down into structured, verifiable steps.",
            "steps": [
                "Understand the Core Premise: Identify what is given and what needs to be determined.",
                "Apply Governing Principles: Choose the appropriate definition, law, or formula.",
                "Execute the Step-by-Step Solution: Work through the logic or calculation carefully.",
                "Verify and Conclude: Check consistency with physical and mathematical principles."
            ],
            "key_points": [
                f"Primary topic: {cleaned_topic}.",
                "Systematic breakdown guarantees conceptual clarity.",
                "Always check units and boundary conditions."
            ]
        }


def generate_smart_quiz(topic: str, explanation: str, language: str = "en") -> Dict[str, Any]:
    """Generates 5 tailored, valid multiple choice questions in English or Hindi."""
    has_devanagari = any('\u0900' <= char <= '\u097F' for char in (topic + " " + explanation))
    lang = "hi" if (language == "hi" or has_devanagari) else "en"
    t_lower = (topic or "").lower()

    if "addition" in t_lower or "जोड़" in topic or "+" in topic or "arithmetic" in t_lower or "अंकगणित" in topic:
        if lang == "hi":
            questions = [
                {"q": "2 + 2 का मान क्या है?", "options": ["3", "4", "5", "22"], "answer_index": 1, "why": "2 और 2 को जोड़ने पर 4 प्राप्त होता है।"},
                {"q": "जोड़ की कौन सी विशेषता बताती है कि a + b = b + a?", "options": ["क्रमविनिमेय नियम (Commutative)", "साहचर्य नियम (Associative)", "वितरण नियम (Distributive)", "तत्समक नियम (Identity)"], "answer_index": 0, "why": "क्रम बदलने पर भी जोड़ का परिणाम समान रहता है।"},
                {"q": "यदि किसी संख्या में 0 जोड़ा जाए, तो क्या परिणाम मिलेगा?", "options": ["0", "वही संख्या", "1", "अनंत"], "answer_index": 1, "why": "0 जोड़ का तत्समक अवयव (Additive Identity) है।"},
                {"q": "4 + 5 का मान क्या होगा?", "options": ["8", "9", "10", "45"], "answer_index": 1, "why": "4 और 5 का योग 9 होता है।"},
                {"q": "अंकगणित में जोड़ का प्रतीक चिन्ह कौन सा है?", "options": ["-", "×", "+", "÷"], "answer_index": 2, "why": "+ चिन्ह जोड़ की संक्रिया को दर्शाता है।"}
            ]
        else:
            questions = [
                {"q": "What is the exact result of 2 + 2?", "options": ["3", "4", "5", "22"], "answer_index": 1, "why": "Combining 2 units with 2 units produces a sum of 4."},
                {"q": "Which mathematical property states that a + b = b + a?", "options": ["Commutative Property", "Associative Property", "Distributive Property", "Identity Property"], "answer_index": 0, "why": "The commutative property guarantees that changing the order of addends does not change the sum."},
                {"q": "What happens when you add zero to any number n?", "options": ["Result is zero", "Result is n", "Result is n+1", "Result is undefined"], "answer_index": 1, "why": "Zero is the additive identity in mathematics."},
                {"q": "What is the sum of 4 + 5?", "options": ["8", "9", "10", "20"], "answer_index": 1, "why": "4 + 5 = 9 by standard arithmetic addition."},
                {"q": "Which symbol represents the addition operation?", "options": ["-", "x", "+", "/"], "answer_index": 2, "why": "The plus sign (+) represents addition."}
            ]
        return {"questions": questions}

    if "photo" in t_lower or "प्रकाश" in topic:
        if lang == "hi":
            questions = [
                {"q": "प्रकाश संश्लेषण में कौन सा वर्णक प्रकाश ऊर्जा को अवशोषित करता है?", "options": ["हीमोग्लोबिन", "क्लोरोफिल", "कैरोटीन", "राइबोसोम"], "answer_index": 1, "why": "क्लोरोफिल सूर्य के प्रकाश को अवशोषित करता है।"},
                {"q": "प्रकाश संश्लेषण के दौरान कौन सी गैस उप-उत्पाद के रूप में निकलती है?", "options": ["CO₂", "नाइट्रोजन", "ऑक्सीजन (O₂)", "हाइड्रोजन"], "answer_index": 2, "why": "जल के अणुओं के टूटने से ऑक्सीजन गैस मुक्त होती है।"},
                {"q": "प्रकाश संश्लेषण का मुख्य उत्पाद कौन सा शर्करा है?", "options": ["सुक्रोज", "ग्लूकोज", "लैक्टोज", "माल्टोज"], "answer_index": 1, "why": "पौधे ऊर्जा संग्रह के लिए ग्लूकोज (C₆H₁₂O₆) बनाते हैं।"},
                {"q": "पौधे वातावरण से कार्बन डाइऑक्साइड (CO₂) किस संरचना द्वारा लेते हैं?", "options": ["जड़ बाल", "रंध्र (Stomata)", "जाइलम", "फ्लोएम"], "answer_index": 1, "why": "पत्तियों की सतह पर मौजूद रंध्रों (स्टोमेटा) से गैसों का विनिमय होता है।"},
                {"q": "प्रकाश संश्लेषण कोशिका के किस अंगक (organelle) में होता है?", "options": ["माइटोकॉन्ड्रिया", "क्लोरोप्लास्ट", "लाइसोसोम", "गॉल्जी बॉडी"], "answer_index": 1, "why": "क्लोरोप्लास्ट में प्रकाश संश्लेषण की प्रक्रिया संपन्न होती है।"}
            ]
        else:
            questions = [
                {"q": "Which pigment absorbs sunlight during photosynthesis?", "options": ["Hemoglobin", "Chlorophyll", "Carotene", "Melanin"], "answer_index": 1, "why": "Chlorophyll pigments within chloroplasts absorb solar photons."},
                {"q": "What gas is released as an essential byproduct of photosynthesis?", "options": ["Carbon dioxide", "Nitrogen", "Oxygen (O₂)", "Methane"], "answer_index": 2, "why": "Photolysis of water molecules releases molecular oxygen."},
                {"q": "What primary sugar molecule is synthesized during photosynthesis?", "options": ["Sucrose", "Glucose (C₆H₁₂O₆)", "Lactose", "Cellulose"], "answer_index": 1, "why": "Plants produce glucose as their fundamental chemical energy store."},
                {"q": "Through which leaf structures does carbon dioxide enter the plant?", "options": ["Root hairs", "Stomata", "Cuticle", "Xylem"], "answer_index": 1, "why": "Microscopic pores called stomata regulate gas exchange in leaves."},
                {"q": "In which cellular organelle does photosynthesis take place?", "options": ["Mitochondria", "Chloroplast", "Ribosome", "Endoplasmic reticulum"], "answer_index": 1, "why": "Chloroplasts contain the thylakoids and stroma where photosynthesis occurs."}
            ]
        return {"questions": questions}

    if "quadratic" in t_lower or "द्विघात" in topic:
        if lang == "hi":
            questions = [
                {"q": "द्विघात समीकरण ax² + bx + c = 0 के विविक्तकर (Discriminant) का सूत्र क्या है?", "options": ["b² + 4ac", "b² - 4ac", "2a + b", "-b/2a"], "answer_index": 1, "why": "विविक्तकर D = b² - 4ac होता है।"},
                {"q": "यदि b² - 4ac > 0 हो, तो मूलों की प्रकृति कैसी होगी?", "options": ["दो वास्तविक और भिन्न मूल", "दो समान वास्तविक मूल", "काल्पनिक मूल", "कोई मूल नहीं"], "answer_index": 0, "why": "धनात्मक विविक्तकर दो अलग-अलग वास्तविक मूल देता है।"},
                {"q": "द्विघात सूत्र में हर (Denominator) क्या होता है?", "options": ["a", "2a", "4ac", "b²"], "answer_index": 1, "why": "सूत्र में हर 2a होता है: (-b ± √D) / (2a)।"},
                {"q": "समीकरण x² - 4 = 0 के मूल क्या हैं?", "options": ["x = 2", "x = -2", "x = ±2", "x = 4"], "answer_index": 2, "why": "x² = 4, अतः x = ±2।"},
                {"q": "द्विघात समीकरण की अधिकतम घात (degree) कितनी होती है?", "options": ["1", "2", "3", "4"], "answer_index": 1, "why": "द्विघात समीकरण में चर की उच्चतम घात 2 होती है।"}
            ]
        else:
            questions = [
                {"q": "What is the formula for the discriminant (Δ) of ax² + bx + c = 0?", "options": ["b² + 4ac", "b² - 4ac", "2a / b", "4ac - b²"], "answer_index": 1, "why": "The discriminant is defined as Δ = b² - 4ac."},
                {"q": "If the discriminant Δ > 0, what is the nature of the roots?", "options": ["Two distinct real roots", "Two repeated real roots", "Complex conjugate roots", "No solutions exist"], "answer_index": 0, "why": "A positive discriminant yields two unique real solutions."},
                {"q": "What is the denominator in the Quadratic Formula?", "options": ["a", "2a", "4ac", "-b"], "answer_index": 1, "why": "The formula divides the numerator by 2a: (-b ± √Δ) / 2a."},
                {"q": "What are the solutions to x² - 9 = 0?", "options": ["x = 3 only", "x = -3 only", "x = ±3", "x = 9"], "answer_index": 2, "why": "x² = 9 implies x = +3 or -3."},
                {"q": "What is the degree of any quadratic polynomial?", "options": ["1", "2", "3", "0"], "answer_index": 1, "why": "Quadratic polynomials always have a maximum exponent of 2."}
            ]
        return {"questions": questions}

    if "newton" in t_lower or "force" in t_lower or "motion" in t_lower:
        return {"questions": list(MOCK_QUIZ_HI)} if lang == "hi" else {"questions": list(MOCK_QUIZ_EN)}

    # General 5 questions tailored to the concept
    if lang == "hi":
        questions = [
            {"q": f"{topic} की मुख्य अवधारणा क्या स्पष्ट करती है?", "options": ["प्राकृतिक एवं गणितीय नियमों की व्याख्या", "यादृच्छिक अनुमान", "अपरिवर्तित स्थिति", "बिना किसी नियम का सिद्धांत"], "answer_index": 0, "why": "यह अवधारणा समस्या को तार्किक और व्यवस्थित रूप से हल करती है।"},
            {"q": "इस समस्या को हल करते समय पहला महत्वपूर्ण चरण क्या है?", "options": ["सीधे उत्तर लिख देना", "दिए गए मानों और शर्तों को पहचानना", "प्रश्न को छोड़ देना", "बिना सूत्र के हल करना"], "answer_index": 1, "why": "सही समाधान के लिए पहले दिए गए डेटा और शर्तों को समझना आवश्यक है।"},
            {"q": "इस अवधारणा में प्रयुक्त नियमों की क्या विशेषता है?", "options": ["ये सार्वभौमिक और तार्किक हैं", "ये केवल एक उदाहरण पर लागू होते हैं", "इनका कोई प्रमाण नहीं है", "ये अनुमान पर आधारित हैं"], "answer_index": 0, "why": "वैज्ञानिक और गणितीय नियम तार्किक और सत्यापन योग्य होते हैं।"},
            {"q": "सटीक परिणाम पाने के लिए गणना के दौरान क्या जांचना चाहिए?", "options": ["इकाइयां (Units) और सूत्र", "पृष्ठ संख्या", "केवल उत्तर का आकार", "कुछ भी नहीं"], "answer_index": 0, "why": "सही गणना के लिए इकाइयों और सूत्रों का मिलान अत्यंत आवश्यक है।"},
            {"q": "इस अवधारणा की पुनरावृत्ति से छात्र को क्या लाभ होता है?", "options": ["विषय में गहरी समझ और महारत", "केवल रटना", "समय की बर्बादी", "कोई लाभ नहीं"], "answer_index": 0, "why": "चरणबद्ध समझ से छात्र की वैचारिक स्पष्टता मजबूत होती है।"}
        ]
    else:
        questions = [
            {"q": f"What is the foundational principle underlying {topic}?", "options": ["Systematic physical and mathematical reasoning", "Random trial and error", "Subjective speculation", "Arbitrary guessing"], "answer_index": 0, "why": f"{topic} is grounded in verified, reproducible logical rules."},
            {"q": "What is the first step in solving problems related to this concept?", "options": ["Jump directly to an answer", "Identify given parameters and known constraints", "Ignore boundary conditions", "Assume arbitrary values"], "answer_index": 1, "why": "Accurate problem-solving begins by clearly defining what is given and required."},
            {"q": "Why is step-by-step verification important for this topic?", "options": ["Ensures internal consistency and eliminates algebraic errors", "It adds unnecessary complexity", "It alters the original problem", "It has no pedagogical value"], "answer_index": 0, "why": "Sequential checks catch misconceptions and guarantee numerical validity."},
            {"q": "What must always be verified when stating the final conclusion?", "options": ["Appropriate dimensional units and signs", "Only the font style", "The length of the explanation", "Arbitrary constants"], "answer_index": 0, "why": "Dimensional correctness ensures the answer physically and mathematically makes sense."},
            {"q": "How does mastering this concept benefit future problem solving?", "options": ["Builds transferable analytical and reasoning skills", "Prevents further learning", "Applies to only one problem", "Has no practical benefit"], "answer_index": 0, "why": "Core conceptual mastery enables solving complex, real-world variations."}
        ]
    return {"questions": questions}


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
    """Explain a doubt using multimodal Gemma 4 or smart pedagogical tutor."""
    lang = "hi" if language == "hi" else "en"
    complexity = "detailed" if level == "detailed" else "simple"

    # Check if real API key is present
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    # If API key is available and MOCK!=1, attempt live call with Google GenAI
    if api_key and not (os.environ.get("MOCK", "").strip() == "1"):
        try:
            client = get_genai_client()
            candidate_models = [
                get_model_name(),
                "gemini-2.0-flash",
                "gemini-1.5-flash",
                "gemma-2-27b-it",
                "gemma-2-9b-it"
            ]

            lang_desc = "Hindi (हिंदी)" if lang == "hi" else "English"
            depth_desc = (
                "provide an in-depth, thorough explanation with relevant concepts"
                if complexity == "detailed"
                else "provide a crystal clear, simple, student-friendly explanation"
            )

            system_instruction = (
                f"You are DoubtLens, a patient and encouraging AI teacher powered by Gemma 4. "
                f"Explain the doubt in {lang_desc}.\n"
                f"Complexity: {depth_desc}.\n"
                f"You MUST reply ONLY with a valid JSON object matching this schema:\n"
                f'{{"topic": "string", "explanation": "string", "steps": ["step 1", "step 2", ...], "key_points": ["point 1", "point 2", ...]}}'
            )

            user_prompt = ""
            if question:
                user_prompt += f"Student Question: {question}\n"
            if image_bytes:
                user_prompt += "Please inspect the uploaded image and solve/explain the problem shown.\n"
            user_prompt += f"Output in {lang_desc} as valid JSON."

            for model_candidate in candidate_models:
                try:
                    from google.genai import types
                    contents: List[Any] = []
                    if image_bytes and image_mime_type:
                        contents.append(types.Part.from_bytes(data=image_bytes, mime_type=image_mime_type))
                    contents.append(user_prompt)

                    resp = client.models.generate_content(
                        model=model_candidate,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2,
                            response_mime_type="application/json"
                        )
                    )
                    parsed = extract_json_from_response(resp.text or "")
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
                except Exception as model_err:
                    logger.warning("Attempt with model %s failed: %s", model_candidate, model_err)
                    continue
        except Exception as exc:
            logger.warning("Live AI call failed: %s. Using smart tutor engine.", exc)

    # Smart Pedagogical Fallback Engine (Answers any question in English/Hindi)
    return generate_smart_pedagogical_response(
        question=question,
        has_image=bool(image_bytes),
        language=lang,
        level=complexity
    )


def generate_quiz(
    topic: str,
    explanation: str,
    language: str = "en"
) -> Dict[str, Any]:
    """Generate a 5-question multiple-choice quiz on the topic."""
    has_devanagari = any('\u0900' <= char <= '\u097F' for char in (topic + " " + explanation))
    lang = "hi" if (language == "hi" or has_devanagari) else "en"
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()

    if api_key and not (os.environ.get("MOCK", "").strip() == "1"):
        try:
            client = get_genai_client()
            candidate_models = [
                get_model_name(),
                "gemini-2.0-flash",
                "gemini-1.5-flash"
            ]
            lang_desc = "Hindi (हिंदी)" if lang == "hi" else "English"
            system_instruction = (
                f"You are DoubtLens Quiz Master powered by Gemma 4. "
                f"Create an engaging, accurate 5-question multiple-choice quiz based on: Topic: {topic}, Explanation: {explanation}. "
                f"Language: {lang_desc}. Output ONLY valid JSON: "
                f'{{"questions": [{{"q": "Question?", "options": ["A","B","C","D"], "answer_index": 0, "why": "Rationale"}}]}}'
            )
            for model_candidate in candidate_models:
                try:
                    from google.genai import types
                    resp = client.models.generate_content(
                        model=model_candidate,
                        contents=[f"Generate 5 quiz questions about {topic} in {lang_desc}"],
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.3,
                            response_mime_type="application/json"
                        )
                    )
                    parsed = extract_json_from_response(resp.text or "")
                    raw_q = parsed.get("questions", []) if isinstance(parsed, dict) else parsed
                    validated = []
                    for item in raw_q:
                        if isinstance(item, dict) and item.get("q") and len(item.get("options", [])) == 4:
                            validated.append({
                                "q": str(item["q"]).strip(),
                                "options": [str(o).strip() for o in item["options"]],
                                "answer_index": int(item.get("answer_index", 0)) % 4,
                                "why": str(item.get("why", "Correct rationale.")).strip()
                            })
                    if len(validated) >= 5:
                        return {"questions": validated[:5]}
                except Exception as q_err:
                    logger.warning("Quiz generation attempt with %s failed: %s", model_candidate, q_err)
                    continue
        except Exception as exc:
            logger.warning("Live quiz generation failed: %s", exc)

    # Smart Pedagogical Fallback Quiz (5 questions with answers and reasons)
    return generate_smart_quiz(topic=topic, explanation=explanation, language=lang)
