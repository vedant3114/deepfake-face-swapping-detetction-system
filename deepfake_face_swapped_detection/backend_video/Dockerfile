# Use Python 3.10 (Full image to avoid DNS/SSL issues with slim)
FROM python:3.10

# Set working directory
WORKDIR /app

# Install system dependencies (ffmpeg, libsndfile1, and network diagnostics)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    ca-certificates \
    dnsutils \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .

# Install Python dependencies
# Use --no-cache-dir to keep image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a directory for the model to ensure permissions
RUN mkdir -p models && chmod 777 models

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Define environment variables
ENV MODEL_PATH=best_model.pth

# Run the application
# HF Spaces expects the app to run on port 7860 by default
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
