# ============================================
# SINHALA HANDWRITTEN OCR WEB APP
# Streamlit Application for Sinhala Text Recognition
# ============================================

import streamlit as st
import torch
from PIL import Image
import io
import os
import numpy as np
import cv2
from datetime import datetime
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Page configuration
st.set_page_config(
    page_title="Sinhala Handwritten OCR",
    page_icon="📝",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 1rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .stButton button {
        background-color: #2E86AB;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">📝 Sinhala Handwritten OCR</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center">Upload a handwritten Sinhala document image and get digital text</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## About")
    st.info("""
    This application recognizes **handwritten Sinhala text** from images.
    
    **Features:**
    - Upload image (PNG, JPG, JPEG)
    - Automatic text recognition
    - Copy results to clipboard
    - Download results as TXT file
    """)
    
    st.markdown("## Instructions")
    st.markdown("1. 📤 Upload a clear image\n2. 🔍 Click Recognize Text\n3. 📋 Copy or download result")

# Model loading
@st.cache_resource
def load_model():
    """Load the trained model"""
    try:
        # Try to load fine-tuned model if exists
        model_path = "./trocr_sinhala_best"
        
        if os.path.exists(model_path):
            processor = TrOCRProcessor.from_pretrained(model_path)
            model = VisionEncoderDecoderModel.from_pretrained(model_path)
            st.sidebar.success("✅ Fine-tuned model loaded!")
        else:
            # Fallback to base model
            processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
            model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
            st.sidebar.info("📌 Using base model (fine-tuned model will be added after training)")
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        return processor, model, device
        
    except Exception as e:
        st.sidebar.error(f"Error: {str(e)}")
        return None, None, None

def preprocess_image(image):
    """Preprocess image for better OCR"""
    img = np.array(image)
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    img = 255 - img
    return Image.fromarray(img)

def predict_text(image, processor, model, device):
    """Predict Sinhala text from image"""
    try:
        processed_img = preprocess_image(image)
        pixel_values = processor(images=processed_img, return_tensors="pt").pixel_values.to(device)
        
        generated_ids = model.generate(
            pixel_values,
            max_length=128,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2,
        )
        
        predicted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return predicted_text, None
    except Exception as e:
        return None, str(e)

# Main UI
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📤 Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        
        if st.button("🔍 Recognize Text", type="primary", use_container_width=True):
            with st.spinner("Recognizing text..."):
                processor, model, device = load_model()
                if processor and model:
                    predicted_text, error = predict_text(image, processor, model, device)
                    if predicted_text:
                        st.session_state['predicted_text'] = predicted_text
                        st.session_state['prediction_time'] = datetime.now()
                        st.success("✅ Recognition completed!")
                    else:
                        st.error(f"Error: {error}")
                else:
                    st.error("Failed to load model")

with col2:
    st.markdown("### 📝 Recognition Result")
    
    if 'predicted_text' in st.session_state:
        result_text = st.session_state['predicted_text']
        st.markdown(f'<div class="result-box"><strong>📄 Recognized Text:</strong><br><br><span style="font-size: 1.1rem;">{result_text}</span></div>', unsafe_allow_html=True)
        
        col_copy, col_download = st.columns(2)
        with col_copy:
            st.code(result_text)
        with col_download:
            txt_file = io.BytesIO(result_text.encode('utf-8'))
            st.download_button("💾 Download TXT", data=txt_file, file_name=f"ocr_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", use_container_width=True)
    else:
        st.info("👈 Upload an image and click 'Recognize Text'")

st.markdown("---")
st.markdown('<div style="text-align: center; color: #888;">Powered by TrOCR | Fine-tuned on SinOCR Dataset</div>', unsafe_allow_html=True)
