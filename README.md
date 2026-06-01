# Sinhala Handwritten OCR Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📝 About
Web application for recognizing handwritten Sinhala text from images using TrOCR (Transformer OCR) fine-tuned on SinOCR dataset.

## 🚀 Features
- Upload handwritten Sinhala images
- Automatic text recognition
- Copy results to clipboard
- Download results as text file

## 📊 Model
- Base Model: microsoft/trocr-base-handwritten
- Fine-tuned on: SinOCR dataset (771 training samples)
- Characters: 106 unique Sinhala characters

## 🛠️ Tech Stack
- Streamlit
- PyTorch
- Hugging Face Transformers
- OpenCV

## 📁 Project Structure
├── app.py # Streamlit application
├── requirements.txt # Python dependencies
├── packages.txt # System dependencies
└── README.md # Documentation

text

## 🎯 Usage
1. Upload a clear image of handwritten Sinhala text
2. Click "Recognize Text"
3. View, copy, or download the recognized text

## 📧 Contact
For questions or collaborations, please open an issue.

## 📄 License
MIT
