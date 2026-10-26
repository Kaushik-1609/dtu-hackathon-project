# ==============================================================================
# DoubtLens - Dockerfile
# Python 3.11 containerized runtime for DoubtLens
# Built for Hacktoberfest Hack Day Delhi x SKILLOP DTU Hackathon
# ==============================================================================

FROM python:3.11-slim

# Set environment variables for clean container execution
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

WORKDIR /app

# Install dependencies using cached layer
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files into container
COPY . /app

# Create non-root user for security best practices
RUN useradd -m -u 1000 doubtlens && chown -R doubtlens:doubtlens /app
USER doubtlens

# Expose the default application port
EXPOSE 5000

# Container healthcheck using standard Python library (no extra package needed)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python3 -c "import urllib.request, os; port=os.environ.get('PORT', '5000'); urllib.request.urlopen(f'http://127.0.0.1:{port}/api/health')" || exit 1

# Launch application via Gunicorn with dynamic PORT support
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} --workers 2 --threads 4 --timeout 60 app:app"]
