"""app.py - DoubtLens Flask Backend.

A student uploads a photo of a textbook page / handwritten problem / diagram (or types a question).
Gemma 4 explains it step by step in simple English or Hindi.
Then a "Test me" button generates a 5-question multiple-choice quiz on that topic.

API Endpoints:
1) GET  /api/health   -> {"status": "ok"}
2) POST /api/explain  -> {"topic": str, "explanation": str, "steps": [str], "key_points": [str]}
3) POST /api/quiz     -> {"questions": [{"q": str, "options": [str,str,str,str], "answer_index": int, "why": str}]}
"""

import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from gemma_client import explain_doubt, generate_quiz

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("doubtlens")

# Initialize Flask application
app = Flask(__name__, template_folder="templates", static_folder="static")

# Enable CORS for all routes (frontend and backend can communicate cleanly)
CORS(app)

# Limit maximum upload payload to 6 MB to safely accommodate 5 MB files + multipart headers
app.config["MAX_CONTENT_LENGTH"] = 6 * 1024 * 1024

# 5 MB in bytes for strict file size check
MAX_IMAGE_SIZE_BYTES = 5 * 1024 * 1024

# Allowed image extensions and mime types
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}
ALLOWED_MIME_TYPES = {"image/png", "image/jpeg", "image/pjpeg", "image/webp"}


# ---------------------------------------------------------------------------
# ERROR HANDLERS (Returning consistent JSON contract)
# ---------------------------------------------------------------------------

@app.errorhandler(413)
def handle_file_too_large(error):
    """Handle uploads exceeding file size limit."""
    logger.warning("Upload rejected: file size exceeds limit")
    return jsonify({"error": "File size exceeds 5 MB limit"}), 413


@app.errorhandler(400)
def handle_bad_request(error):
    """Handle bad requests with JSON error response."""
    description = getattr(error, "description", "Bad Request")
    return jsonify({"error": str(description)}), 400


@app.errorhandler(404)
def handle_not_found(error):
    """Handle not found routes."""
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(500)
def handle_server_error(error):
    """Handle unexpected server errors."""
    logger.error("Internal Server Error: %s", error)
    return jsonify({"error": "Internal server error"}), 500


# ---------------------------------------------------------------------------
# FRONTEND ROUTE
# ---------------------------------------------------------------------------

@app.route("/", methods=["GET"])
def index():
    """Serve the frontend index.html template if available."""
    index_file = os.path.join(app.template_folder or "templates", "index.html")
    if os.path.exists(index_file):
        return render_template("index.html")
    return jsonify({
        "project": "DoubtLens",
        "description": "Visual STEM doubt-solving and quiz tutor powered by Gemma 4",
        "status": "online",
        "health_check": "/api/health"
    }), 200


# ---------------------------------------------------------------------------
# API ENDPOINTS
# ---------------------------------------------------------------------------

@app.route("/api/health", methods=["GET"])
def health_check():
    """1) Health Check Endpoint.

    Returns:
        JSON: {"status": "ok"} with HTTP 200
    """
    return jsonify({"status": "ok"}), 200


@app.route("/api/explain", methods=["POST"])
def explain_endpoint():
    """2) Explain Doubt Endpoint.

    Accepts multipart/form-data:
      - image: File upload (optional; png/jpg/webp; max 5 MB)
      - question: Text prompt (optional)
      - language: "en" | "hi" (default "en")
      - level: "simple" | "detailed" (default "simple")

    Constraint:
      At least one of image or question must be provided.

    Returns:
        JSON: {"topic": str, "explanation": str, "steps": [str], "key_points": [str]}
    """
    try:
        # Extract form parameters
        question = request.form.get("question", "").strip()
        language = request.form.get("language", "en").strip().lower()
        level = request.form.get("level", "simple").strip().lower()

        # Sanitize language and level to contract defaults
        if language not in ("en", "hi"):
            language = "en"
        if level not in ("simple", "detailed"):
            level = "simple"

        # Extract file upload
        image_file = request.files.get("image")
        image_bytes = None
        image_mime_type = None

        if image_file and image_file.filename:
            filename = image_file.filename.lower()
            _, ext = os.path.splitext(filename)

            # Validate file extension
            if ext not in ALLOWED_EXTENSIONS:
                return jsonify({
                    "error": "Invalid image format. Allowed formats: PNG, JPG, JPEG, WEBP."
                }), 400

            # Read image content
            image_bytes = image_file.read()

            # Enforce 5 MB limit
            if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
                return jsonify({"error": "Image file too large (max 5 MB)"}), 413

            # Determine mime type
            content_type = image_file.content_type
            if content_type in ALLOWED_MIME_TYPES:
                image_mime_type = content_type
            elif ext == ".png":
                image_mime_type = "image/png"
            elif ext in (".jpg", ".jpeg"):
                image_mime_type = "image/jpeg"
            elif ext == ".webp":
                image_mime_type = "image/webp"
            else:
                image_mime_type = "application/octet-stream"

        # Validate that at least one of image or question is provided
        if not image_bytes and not question:
            return jsonify({
                "error": "At least one of 'image' or 'question' is required."
            }), 400

        # Invoke Gemma 4 via client
        result = explain_doubt(
            question=question if question else None,
            image_bytes=image_bytes,
            image_mime_type=image_mime_type,
            language=language,
            level=level
        )

        return jsonify(result), 200

    except Exception as exc:
        logger.exception("Error during /api/explain: %s", exc)
        return jsonify({"error": f"Failed to generate explanation: {str(exc)}"}), 500


@app.route("/api/quiz", methods=["POST"])
def quiz_endpoint():
    """3) Quiz Generation Endpoint.

    Accepts application/json:
      - topic: str (required)
      - explanation: str (required)
      - language: "en" | "hi" (default "en")

    Returns:
        JSON: {
          "questions": [
            {"q": str, "options": [str, str, str, str], "answer_index": int (0-3), "why": str}
          ]
        } (exactly 5 questions)
    """
    try:
        # Validate JSON content type and payload
        if not request.is_json:
            return jsonify({"error": "Request body must be application/json"}), 400

        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON body provided"}), 400

        topic = str(data.get("topic", "")).strip()
        explanation = str(data.get("explanation", "")).strip()
        language = str(data.get("language", "en")).strip().lower()

        if language not in ("en", "hi"):
            language = "en"

        # Required field validations
        if not topic:
            return jsonify({"error": "Field 'topic' is required."}), 400
        if not explanation:
            return jsonify({"error": "Field 'explanation' is required."}), 400

        # Invoke quiz generator
        quiz_data = generate_quiz(
            topic=topic,
            explanation=explanation,
            language=language
        )

        return jsonify(quiz_data), 200

    except Exception as exc:
        logger.exception("Error during /api/quiz: %s", exc)
        return jsonify({"error": f"Failed to generate quiz: {str(exc)}"}), 500


# ---------------------------------------------------------------------------
# APPLICATION ENTRYPOINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"
    logger.info("Starting DoubtLens backend server on port %s (debug=%s)", port, debug_mode)
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
