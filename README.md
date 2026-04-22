# 🎥 DeepDrishti - Deepfake & Face-Swapped Detection System

> **A comprehensive AI-powered detection system to identify deepfakes and face-swapped content in images and videos**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-deepdrishti.vercel.app-blue?style=flat-square)](https://deepdrishti.vercel.app/)
[![Published Paper](https://img.shields.io/badge/Published-IJNRD-green?style=flat-square)](https://ijnrd.org/papers/IJNRD2603579.pdf)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Model Architecture](#model-architecture)
- [Deployment](#deployment)
- [Publications](#publications)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

**DeepDrishti** is an advanced machine learning system designed to detect and identify deepfakes and face-swapped content. It combines:

- **Video Analysis**: Multi-modal detection using visual frames and audio analysis
- **Image Analysis**: ResNet50-based CNN for detecting face-swapped images
- **URL Support**: Direct detection from YouTube, Instagram, TikTok, and other platforms
- **Real-time Processing**: Fast inference with GPU acceleration support

The system employs cutting-edge deep learning models to analyze both visual and audio characteristics, providing high-accuracy detection results with explainability features.

### 🎓 Academic Foundation

This project is backed by peer-reviewed research and has been published in the **International Journal of Novel Research and Development (IJNRD)**. See the [Publications](#publications) section for more details.

---

## ✨ Features

### Core Detection Capabilities
- ✅ **Video Deepfake Detection**: Multi-frame analysis with temporal consistency checking
- ✅ **Image Face-Swap Detection**: CNN-based classification using pre-trained ResNet50
- ✅ **Audio-Visual Synchronization**: Detects lip-sync inconsistencies
- ✅ **Multi-Platform Support**: YouTube, Instagram, TikTok, Twitter/X direct URL analysis
- ✅ **Explainability Reports**: Detailed analysis reports with confidence scores

### Detection Modes
1. **Direct Upload**: Upload video/image files directly from your device
2. **URL Analysis**: Provide direct links to social media content
3. **Platform Download**: Automatic download and analysis from supported platforms

### Analysis Features
- 📊 **Confidence Scoring**: Get probability scores for authenticity assessment
- 📈 **Detailed Reports**: Frame-by-frame analysis with visualization
- 🎨 **Real-time Visualization**: Live processing feedback with glow effects
- 💾 **Report Export**: Download analysis results as PDF

---

## 🛠️ Technology Stack

### Frontend
```
Vue 3 (Composition API)
├── TypeScript
├── Vite (Build Tool)
├── Tailwind CSS
├── Chart.js (Data Visualization)
├── html2canvas (Screenshot Generation)
└── jsPDF (PDF Export)
```

### Backend - Video Analysis
```
FastAPI (Python Web Framework)
├── PyTorch (Deep Learning Framework)
├── TorchAudio (Audio Processing)
├── TorchVision (Computer Vision)
├── OpenCV (Video Processing)
├── yt-dlp (Video Downloading)
└── CUDA Support (GPU Acceleration)
```

### Backend - Image Analysis
```
FastAPI (Python Web Framework)
├── TensorFlow/Keras
├── ResNet50 (Pre-trained Model)
├── OpenCV
├── PIL (Image Processing)
├── yt-dlp (Image Downloading)
├── Selenium (Browser Automation)
├── Instaloader (Instagram API)
└── WebDriver Manager
```

---

## 📁 Project Structure

```
deepfake_face_swapped_detection/
├── 📂 src/                              # Vue 3 Frontend
│   ├── App.vue                          # Main application component
│   ├── components/
│   │   └── DeepfakeExplainability.vue  # Analysis visualization component
│   ├── main.ts                          # Vue application entry point
│   └── shims-vue.d.ts                   # TypeScript Vue declarations
│
├── 📂 backend_video/                    # Video Deepfake Detection API
│   ├── main.py                          # FastAPI application server
│   ├── model_arch.py                    # PyTorch model architecture
│   ├── downloader.py                    # Video download utility
│   ├── url_handler.py                   # Platform detection & URL parsing
│   ├── setup_ffmpeg.py                  # FFmpeg configuration
│   ├── requirements.txt                 # Python dependencies
│   └── .env                             # Environment variables
│
├── 📂 backend-image/                    # Image Face-Swap Detection API
│   ├── main.py                          # FastAPI application server
│   ├── downloader.py                    # Image download utility
│   ├── url_handler.py                   # Platform detection
│   ├── requirements.txt                 # Python dependencies
│   └── .env                             # Environment variables
│
├── 📂 models/                           # Pre-trained & Training Notebooks
│   ├── notebook*.ipynb                  # Jupyter notebooks for model training
│   └── best_model.pth                   # Trained PyTorch video model
│
├── 📂 public/                           # Static assets
├── package.json                         # Node.js dependencies
├── tsconfig.json                        # TypeScript configuration
├── vite.config.ts                       # Vite build configuration
└── README.md                            # Project documentation
```

---

## 💻 Installation

### Prerequisites
- **Node.js** >= 18.x (for frontend)
- **Python** >= 3.10 (for backends)
- **FFmpeg** (for video processing)
- **GPU** (NVIDIA with CUDA 11.8+ recommended, but CPU mode also supported)

### Step 1: Clone the Repository

```bash
git clone https://github.com/vdant3114/deepfake-detection.git
cd deepfake_face_swapped_detection
```

### Step 2: Frontend Setup

```bash
# Install dependencies
npm install

# Build frontend
npm run build

# Or for development with hot reload
npm run dev
```

### Step 3: Backend Setup - Video Detection

```bash
cd backend_video

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download pre-trained model (automatic on first run)
# Or manually download from Hugging Face:
# https://huggingface.co/vedant3114/best_model_video

# Start API server
python main.py
# API will be available at http://localhost:8000
```

### Step 4: Backend Setup - Image Detection

```bash
cd backend-image

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Create .env file
cat > .env << EOF
API_URL=your_nvidia_hive_api_url
API_KEY=your_nvidia_hive_api_key
EOF

# Install dependencies
pip install -r requirements.txt

# Start API server (on different port)
python main.py --port 8001
# API will be available at http://localhost:8001
```

### Step 5: Environment Variables

Create `.env` files in both backend directories:

**backend_video/.env:**
```
DEVICE=cuda  # or 'cpu' for CPU-only mode
MODEL_PATH=best_model.pth
HF_MODEL_URL=https://huggingface.co/vedant3114/best_model_video/resolve/main/best_model.pth
```

**backend-image/.env:**
```
API_URL=https://api.nvidia.com/v1/...  # Optional: Nvidia Hive API
API_KEY=your_api_key                    # Optional: Nvidia Hive API Key
USE_API_FALLBACK=True
```

---

## 🚀 Quick Start

### Development Mode

**Terminal 1 - Frontend:**
```bash
npm run dev
# Frontend available at http://localhost:5173
```

**Terminal 2 - Video Backend:**
```bash
cd backend_video
source venv/bin/activate
python main.py
# API at http://localhost:8000
```

**Terminal 3 - Image Backend:**
```bash
cd backend-image
source venv/bin/activate
python main.py --port 8001
# API at http://localhost:8001
```

### Production Build

```bash
# Build frontend
npm run build

# Frontend will be in 'dist/' directory
# Deploy to Vercel, Netlify, or any static hosting

# For backends, deploy FastAPI apps to:
# - Render.com (free tier available)
# - AWS, GCP, Azure
# - Railway.app
```

---

## 🔌 API Documentation

### Video Detection API

**Endpoint:** `POST /api/detect-video`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/detect-video" \
  -F "file=@sample_video.mp4"
```

**Response:**
```json
{
  "is_deepfake": false,
  "confidence": 0.95,
  "frame_analysis": [
    {
      "frame_id": 0,
      "confidence": 0.92
    }
  ],
  "audio_analysis": {
    "lip_sync_score": 0.88,
    "audio_quality": "good"
  },
  "processing_time": 24.5
}
```

---

**Endpoint:** `POST /api/detect-video-url`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/detect-video-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  }'
```

**Response:** Same as direct upload

---

### Image Detection API

**Endpoint:** `POST /api/detect-image`

**Request:**
```bash
curl -X POST "http://localhost:8001/api/detect-image" \
  -F "file=@sample_image.jpg"
```

**Response:**
```json
{
  "is_face_swapped": false,
  "confidence": 0.87,
  "model_used": "resnet50",
  "processing_time": 1.2
}
```

---

**Endpoint:** `POST /api/detect-image-url`

**Request:**
```bash
curl -X POST "http://localhost:8001/api/detect-image-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://instagram.com/..."
  }'
```

**Response:** Same as direct upload

---

## 📊 Usage Examples

### JavaScript/Frontend

```typescript
// Video detection
const formData = new FormData();
formData.append('file', videoFile);

const response = await fetch('http://localhost:8000/api/detect-video', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(`Deepfake confidence: ${result.confidence}`);
```

### Python/Backend

```python
import requests

# Video detection
video_url = "https://example.com/video.mp4"
response = requests.post(
    "http://localhost:8000/api/detect-video-url",
    json={"url": video_url}
)
result = response.json()
print(f"Is Deepfake: {result['is_deepfake']}")
```

---

## 🧠 Model Architecture

### Video Detection Model: MultiModalDeepfakeDetector

**Key Components:**

1. **Visual Feature Extractor** (ResNet-based)
   - Extracts spatial features from video frames
   - Uses residual connections for better gradient flow
   - Output: 128-dim feature vector per frame

2. **Audio Feature Extractor**
   - Converts audio to Mel-spectrograms
   - Processes with CNN (Conv2D layers)
   - Temporal attention with Transformer encoder
   - Output: 128-dim feature vector per sequence

3. **Fusion Layer**
   - Concatenates visual and audio features
   - Multi-head attention mechanism
   - Temporal sequence modeling with LSTM

4. **Classification Head**
   - Dense layers with dropout
   - Sigmoid activation for binary classification
   - Output: [0, 1] confidence score

**Configuration:**
```python
HIDDEN_DIM = 128
SEQUENCE_LENGTH = 32
IMG_SIZE = 112
AUDIO_SAMPLE_RATE = 16000
AUDIO_N_MELS = 64
AUDIO_N_FFT = 1024
DROPOUT_RATE = 0.5
```

---

### Image Detection Model

**Architecture:**
- Base: ResNet50 (pre-trained on ImageNet)
- Input: 180x180 RGB images
- Additional Layers:
  - Global Average Pooling
  - Dense layer (512 units) + Dropout(0.5)
  - ReLU activation
  - Output layer (1 unit) + Sigmoid

**Features:**
- Fine-tuned on face-swap dataset
- Handles various face manipulation techniques
- Transfer learning from large-scale dataset

---

## 🌐 Deployment

### Option 1: Vercel (Frontend)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Option 2: Netlify (Frontend)

```bash
# Deploy built files
netlify deploy --prod --dir=dist
```

### Option 3: Render (Backend APIs)

**For backend_video:**

1. Create new Web Service on Render
2. Connect GitHub repository
3. Set environment:
   - Runtime: Python 3.11
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port 8000`

**For backend-image:**

1. Repeat same process
2. Change start command to use port 8001

### Option 4: Docker Deployment

**Dockerfile for Video Backend:**
```dockerfile
FROM pytorch/pytorch:2.0-cuda11.8-runtime-ubuntu22.04

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📰 Publications

This project is based on peer-reviewed research:

**Paper:** *"DeepDrishti: A Multi-Modal Deep Learning Approach for Detecting Face-Swapped and Deepfake Content"*

- 📄 **Published:** International Journal of Novel Research and Development (IJNRD)
- 🔗 **DOI:** [IJNRD2603579](https://ijnrd.org/papers/IJNRD2603579.pdf)
- 📊 **Methodology:** Multi-modal approach combining visual and audio cues
- 🎯 **Accuracy:** 94.2% on test dataset
- 💡 **Innovation:** Transformer-based audio-visual fusion

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use Vue 3 Script Setup for components
- Add tests for new features
- Update documentation accordingly

---

## 📋 System Requirements

### Minimum (CPU Mode)
- 8GB RAM
- 10GB free disk space
- Python 3.10+
- Node.js 18+

### Recommended (GPU Mode)
- NVIDIA GPU with 4GB+ VRAM
- CUDA 11.8+
- cuDNN 8.x
- 16GB+ RAM
- 20GB+ SSD space

---

## 🔒 Security Note

This tool is designed for legitimate use cases:
- ✅ Educational purposes
- ✅ Content verification
- ✅ Research
- ✅ Media authenticity checking

Please use responsibly and ethically. Creating and distributing deepfakes of others without consent is illegal in many jurisdictions.

---

## 📞 Support & Contact

- 📧 **Email:** vedant3114@gmail.com
- 🐙 **GitHub Issues:** [Report an Issue](https://github.com/yourusername/deepfake-detection/issues)
- 💬 **Discussions:** [Join Community](https://github.com/yourusername/deepfake-detection/discussions)

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Special thanks to the open-source community (PyTorch, TensorFlow, FastAPI, Vue.js)
- The academic community for peer-review and validation
- Contributors and users who have provided feedback

---

## 📈 Performance Metrics

| Metric | Score |
|--------|-------|
| **Video Deepfake Detection Accuracy** | 94.2% |
| **Image Face-Swap Detection Accuracy** | 91.8% |
| **Average Processing Time (Video)** | ~30s (for 1 min video) |
| **Average Processing Time (Image)** | ~1.2s |
| **GPU Memory Usage** | ~2.5GB |
| **Multi-Platform Support** | 5+ platforms |



---

**Made with ❤️ by the DeepDrishti Team**

[⬆ back to top](#-deepdrishti---deepfake--face-swapped-detection-system)
