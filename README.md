🚨 Kinetic Guard: Real-Time AI Gesture Safety System
An enterprise-grade, multi-platform personal safety application that allows users to trigger silent SOS alerts using discreet hand gestures detected via real-time computer vision.

Python FastAPI
Frontend React & Redux
Mobile Kotlin & Compose
Tasks Celery & Redis

🎯 Overview
Kinetic Guard solves a critical problem: what happens when someone is in danger but cannot speak or type? By leveraging Google MediaPipe on a mobile device, the system detects specific finger combinations (e.g., Thumb Down, 2 Fingers) and instantly triggers a multi-channel emergency response pipeline.

This repository is structured as a Monorepo, containing the backend API, React dashboard, Android client, machine learning tuning scripts, and infrastructure configurations.

🏗️ System Architecture
The system follows an event-driven, asynchronous architecture to ensure zero-latency alerts:

Android Client captures frames → MediaPipe detects hand landmarks → Maps geometry to specific gestures.
FastAPI Backend receives the POST request → Fetches real-time street address via OpenStreetMap (Nominatim).
WebSocket Server simultaneously pushes the alert to the React Dashboard the exact millisecond it is saved.
Celery Worker picks up the alert asynchronously → Sends a formatted HTML email with a 1-click WhatsApp deep-link, ensuring the API response time remains sub-second.

✨ Key Features
Discreet Triggers: 10+ distinct gesture mappings (Thumb Down, 2 Fingers, 5 Fingers, etc.).
Anti-Flicker CV Logic: Implemented strict 0.10f hysteresis margins and a 3-second cooldown to prevent micro-movement false positives.
Zero-Latency UI: Replaced HTTP polling with persistent WebSockets for true real-time dashboard updates.
Smart Geocoding: Automatically converts raw GPS coordinates into highly accurate street addresses.
Multi-Channel Notifications: HTML emails featuring a WhatsApp deep-link button for instant forwarding.
Dark Mode Operations Center: Sleek, glassmorphism-inspired React UI designed for high-stress monitoring environments.

📁 Project Structure
KineticGuard/├── backend/          # FastAPI application, Pydantic schemas, SQLAlchemy models├── infra/            # Docker Compose, Redis, Celery configurations├── ml/               # MediaPipe/ONNX model tuning, feature extraction scripts├── web/              # React application, Redux state, WebSocket hooks├── android/          # Kotlin app, CameraX pipeline, Gesture mapping logic├── .gitignore        # Secures .env files and large ML models├── .env.example      # Template for environment variables└── README.md         # You are here

⚙️ Quick Start
Prerequisites
Docker & Docker Compose
Node.js 18+ & NPM
Android Studio
Python 3.12+

**1. Infrastructure & Database**
Start PostgreSQL and Redis using the provided Docker configurations:

bash

cd infra
docker-compose up -d

**2. Backend Setup**
bash

cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# (Fill in your Postgres, Redis, and SMTP credentials in .env)

alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

**3. Background Worker (Mailroom)**
In a new terminal, start the Celery worker to handle email dispatch:

bash

cd backend
celery -A app.tasks.celery_app worker --loglevel=info --pool=solo

**4. Frontend Dashboard**
bash

cd web
npm install
npm run dev
Access the dashboard at http://localhost:5173

**5. Android Application**
Open the android/ folder in Android Studio.
Update the BASE_URL in ApiClient.kt to match your local machine's LAN IP (e.g., http://192.168.x.x:8000/).
Build and run on a physical device (CameraX requires real hardware).

🧠 Computer Vision Details
To prevent the camera from triggering hundreds of false alerts per second, the Android client implements specific logic:

Hysteresis Margins: A finger is only considered "up" if its tip is at least 0.10 normalized units above its PIP joint, filtering out natural hand tremors.
State Debouncing: A strict 3-second cooldown is enforced globally, regardless of whether the gesture changes, preventing API spam.

🛡️ Security
This repository utilizes .gitignore rules to strictly prevent the uploading of:

.env files containing database passwords and SMTP credentials.
Large .onnx / .pth machine learning model weights.
Android build outputs and local IDE configurations.
