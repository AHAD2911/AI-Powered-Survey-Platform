# 🤖 VIVA: AI-Powered Survey Platform

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%202.0%20Flash-purple?logo=google-gemini&logoColor=white)](https://aistudio.google.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**VIVA** is a next-generation survey platform that replaces static forms with intelligent, autonomous AI agents. Built with Google's Gemini AI, VIVA conducts deep, adaptive interviews that probe for nuances, ensuring you get the most insightful data possible.

---

## 🌟 Key Features

- **🧠 Autonomous Interviewers**: AI agents that understand context and ask relevant follow-up questions based on respondent answers.
- **🎙️ Multi-Modal input**: Seamlessly switch between **Text** and **Voice** responses with integrated speech-to-text transcription.
- **📊 Real-time Dashboard**: Track active surveys, view completion stats, and manage research topics from a centralized interface.
- **🌍 Global Support**: Conduct interviews in multiple languages (English, Spanish, French, German, Hindi, Chinese).
- **✨ Premium Dark UI**: A sleek, modern interface built with Streamlit, featuring custom CSS, Lottie animations, and glassmorphism elements.
- **💾 Robust Storage**: Local SQLite database integration with Write-Ahead Logging (WAL) for high performance and reliability.

---

## 🛠️ Technology Stack

| Component | Technology |
| :--- | :--- |
| **Frontend** | Streamlit, Custom CSS, Lottie Animations |
| **AI Engine** | Google Gemini 2.0 Flash (`google-generativeai`) |
| **Audio Processing** | SpeechRecognition, PyAudio, Pydub |
| **Database** | SQLite3 (Persistent storage with WAL) |
| **Language** | Python 3.8+ |

---

## 📂 Project Structure

```text
AI Survey/
├── app.py              # Main Streamlit application (Frontend)
├── backend.py          # AI Logic, Database Operations & Audio Processing
├── Requirement.txt     # Project dependencies
├── Readme.md           # Project documentation
├── viva.db             # SQLite Database (Auto-generated)
└── viva.db-wal         # SQLite Write-Ahead Log
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.8 or higher.
- A Google Gemini API Key. [Get one here](https://aistudio.google.com/app/apikey).

### 2. Installation

Clone the repository:
```bash
git clone https://github.com/your-username/viva-ai-survey.git
cd viva-ai-survey
```

Install dependencies:
```bash
pip install -r Requirement.txt
```

### 3. Environment Setup
Create an environment variable for your Google API Key:

**On Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your_api_key_here"
```

**On Linux/macOS:**
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

### 4. Running the App
```bash
streamlit run app.py
```

---

## 📖 Usage Guide

1.  **Dashboard**: View existing surveys or click **"Create New Survey"**.
2.  **Creation**: Define your research topic, set the number of follow-up "probes", and choose the language.
3.  **Interview**: The AI will start asking questions. You can type your response or use the microphone to speak.
4.  **Completion**: Once the probe limit is reached, the AI will thank the participant and mark the survey as complete.
5.  **Analytics**: Review survey results and metrics in the dashboard.

---

## 🛡️ License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  
</div>
