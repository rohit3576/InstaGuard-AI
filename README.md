🛡 InstaGuard AI

Deepfake Detection & Toxic Comment Analysis for Instagram

InstaGuard AI is a frontend-first AI web application that detects deepfake videos and analyzes toxic comments related to Instagram content.
It is designed as a demo-ready, production-style project with a strong focus on AI, computer vision, and modern web architecture.

🚀 Features
🔹 Mode A — Instagram URL Analysis

(Platform-safe, text-only)

✅ Instagram URL validation

✅ Toxic comment analysis using BERT-based NLP

✅ Risk-level fusion (Low / Medium / High)

❌ No video processing (platform restriction)

🔹 Mode B — Uploaded Video Analysis (Full AI Pipeline)

(Best demo mode)

✅ Upload MP4 video

✅ Video preview in browser

✅ Canvas overlay with face scanning visualization

✅ CNN-based deepfake detection (frame-level)

✅ Aggregated deepfake risk score

✅ Real-time processing UI with loading animation

🧠 Tech Stack
Frontend

HTML5, CSS3

Vanilla JavaScript

<video> + <canvas> for face scanning overlay

Frontend-only UI (no Swagger / docs)

Backend

FastAPI

Python 3.10+

OpenCV (video frame extraction)

CNN-based deepfake model (ResNet-style)

BERT / DistilBERT for toxicity detection

AI / ML

Computer Vision (video frames)

CNN for deepfake classification

NLP toxicity detection

Risk fusion engine

🏗 Project Architecture
InstaGuard-AI/
│
├── backend/
│   ├── app.py
│   ├── api/
│   │   └── routes.py
│   ├── services/
│   │   ├── deepfake_service.py
│   │   ├── toxicity_service.py
│   │   ├── video_utils.py
│   │   └── fusion_engine.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── venv/
├── requirements.txt
└── README.md

▶️ How to Run Locally
1️⃣ Clone the Repository
git clone https://github.com/rohit3576/InstaGuard-AI.git
cd InstaGuard-AI

2️⃣ Create & Activate Virtual Environment
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Run the App
uvicorn backend.app:app --reload

5️⃣ Open in Browser
http://127.0.0.1:8000/


✅ The frontend UI is the product
❌ Swagger / docs are intentionally disabled

🎥 Demo Workflow
Uploaded Video

Upload an .mp4 file

Watch video preview

Red face scanning boxes appear

Deepfake score & risk level shown

Instagram URL

Paste Instagram post / reel URL

Toxicity analysis runs

Risk level displayed

⚠️ Platform Limitations (Important)

Instagram does not allow video scraping or frame extraction

Real video analysis is only supported via user-uploaded videos

This is a non-negotiable platform restriction

The project architecture reflects this reality correctly.

🧪 Current Status
✅ Implemented

Frontend-only UI

Video deepfake detection pipeline

Canvas-based face scanning visualization

Toxic comment NLP

Risk fusion logic

🔜 Planned Enhancements

Real face detection (MediaPipe / OpenCV)

Frame-by-frame confidence visualization

Model fine-tuning

Browser extension support

Cloud deployment

👨‍💻 Author

Rohit Pawar
Computer Engineering Student
AI • Full Stack • Computer Vision

GitHub: rohit3576

⭐ If you like this project

Give it a ⭐ on GitHub — it really helps!
