# ============================================
# OCR MODULE
# Handles all OCR functionality
# ============================================

import torch
from PIL import Image
import numpy as np
import cv2
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import streamlit as st

@st.cache_resource
def load_ocr_model():
    """Load the OCR model (cached for performance)"""
    try:
        # Try to load fine-tuned model
        model_path = "./trocr_sinhala_best"
        
        if os.path.exists(model_path):
            processor = TrOCRProcessor.from_pretrained(model_path)
            model = VisionEncoderDecoderModel.from_pretrained(model_path)
        else:
            # Fallback to Ransaka's fine-tuned model
            processor = TrOCRProcessor.from_pretrained("Ransaka/sinhala-ocr-model-v3")
            model = VisionEncoderDecoderModel.from_pretrained("Ransaka/sinhala-ocr-model-v3")
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = model.to(device)
        
        return processor, model, device
    except Exception as e:
        st.error(f"Failed to load OCR model: {str(e)}")
        return None, None, None

def preprocess_image(image):
    """Preprocess image for better OCR"""
    img = np.array(image)
    
    # Convert to grayscale
    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding
    _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    img = 255 - img
    
    return Image.fromarray(img)

def predict_text(image, processor, model, device):
    """Predict Sinhala text from image"""
    try:
        # Preprocess
        processed_img = preprocess_image(image)
        
        # Process for model
        pixel_values = processor(images=processed_img, return_tensors="pt").pixel_values.to(device)
        
        # Generate prediction
        generated_ids = model.generate(
            pixel_values,
            max_length=128,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=2,
        )
        
        # Decode
        predicted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        return predicted_text, None
    except Exception as e:
        return None, str(e)
