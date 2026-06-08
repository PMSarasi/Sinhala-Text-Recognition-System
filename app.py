# ============================================
# MAIN APPLICATION WITH AUTHENTICATION
# Sinhala Handwritten OCR Web App
# ============================================

import streamlit as st
from PIL import Image
import io
from datetime import datetime
import os

# Import modules
from auth import register_user, login_user, generate_reset_code, verify_reset_code, reset_password
from ocr_app import load_ocr_model, predict_text

# Page configuration
st.set_page_config(
    page_title="Sinhala Handwritten OCR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
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
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    .login-box {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        max-width: 400px;
        margin: 0 auto;
    }
    .stButton button {
        background-color: #2E86AB;
        color: white;
        font-weight: bold;
        width: 100%;
    }
    .logout-btn {
        position: fixed;
        top: 10px;
        right: 20px;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'email' not in st.session_state:
    st.session_state.email = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'  # login, signup, forgot_password, reset_password, main
if 'reset_email' not in st.session_state:
    st.session_state.reset_email = None
if 'reset_code_sent' not in st.session_state:
    st.session_state.reset_code_sent = False
if 'predicted_text' not in st.session_state:
    st.session_state.predicted_text = None
if 'prediction_time' not in st.session_state:
    st.session_state.prediction_time = None

# ============================================
# LOGOUT BUTTON
# ============================================

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.email = None
    st.session_state.page = 'login'
    st.session_state.predicted_text = None
    st.rerun()

# ============================================
# LOGIN PAGE
# ============================================

def login_page():
    st.markdown('<p class="main-header">🔐 Sinhala Handwritten OCR</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Login to access the OCR system</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("login_form"):
                st.markdown("### Login")
                username_or_email = st.text_input("Username or Email")
                password = st.text_input("Password", type="password")
                
                submitted = st.form_submit_button("Login")
                
                if submitted:
                    if not username_or_email or not password:
                        st.error("Please fill all fields")
                    else:
                        success, result = login_user(username_or_email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = result['username']
                            st.session_state.email = result['email']
                            st.session_state.page = 'main'
                            st.rerun()
                        else:
                            st.error(result)
            
            st.markdown("---")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Create Account", use_container_width=True):
                    st.session_state.page = 'signup'
                    st.rerun()
            with col_b:
                if st.button("Forgot Password?", use_container_width=True):
                    st.session_state.page = 'forgot_password'
                    st.rerun()

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown('<p class="main-header">📝 Create Account</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("signup_form"):
                st.markdown("### Sign Up")
                email = st.text_input("Email")
                username = st.text_input("Username (3-20 characters, letters, numbers, underscore)")
                password = st.text_input("Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                
                submitted = st.form_submit_button("Register")
                
                if submitted:
                    if not email or not username or not password:
                        st.error("Please fill all fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = register_user(email, username, password)
                        if success:
                            st.success(message)
                            st.session_state.page = 'login'
                            st.rerun()
                        else:
                            st.error(message)
            
            st.markdown("---")
            if st.button("Back to Login", use_container_width=True):
                st.session_state.page = 'login'
                st.rerun()

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown('<p class="main-header">🔑 Forgot Password</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if not st.session_state.reset_code_sent:
                with st.form("forgot_form"):
                    st.markdown("### Enter your email")
                    email = st.text_input("Email")
                    
                    submitted = st.form_submit_button("Send Reset Code")
                    
                    if submitted:
                        if not email:
                            st.error("Please enter your email")
                        else:
                            success, result = generate_reset_code(email)
                            if success:
                                st.session_state.reset_email = email
                                st.session_state.reset_code_sent = True
                                st.success(f"Reset code sent to {email}")
                                st.info("Please check your email for the 6-digit code")
                                st.rerun()
                            else:
                                st.error(result)
            else:
                with st.form("reset_form"):
                    st.markdown(f"### Reset Password for {st.session_state.reset_email}")
                    reset_code = st.text_input("Enter 6-digit reset code")
                    new_password = st.text_input("New Password", type="password")
                    confirm_password = st.text_input("Confirm New Password", type="password")
                    
                    submitted = st.form_submit_button("Reset Password")
                    
                    if submitted:
                        if not reset_code or not new_password:
                            st.error("Please fill all fields")
                        elif new_password != confirm_password:
                            st.error("Passwords do not match")
                        elif len(new_password) < 6:
                            st.error("Password must be at least 6 characters")
                        else:
                            if verify_reset_code(st.session_state.reset_email, reset_code):
                                success, message = reset_password(st.session_state.reset_email, new_password)
                                if success:
                                    st.success(message)
                                    st.session_state.reset_code_sent = False
                                    st.session_state.reset_email = None
                                    st.session_state.page = 'login'
                                    st.rerun()
                                else:
                                    st.error(message)
                            else:
                                st.error("Invalid or expired reset code")
            
            st.markdown("---")
            if st.button("Back to Login", use_container_width=True):
                st.session_state.reset_code_sent = False
                st.session_state.reset_email = None
                st.session_state.page = 'login'
                st.rerun()

# ============================================
# MAIN OCR APPLICATION
# ============================================

def main_app():
    # Logout button
    st.markdown(f'<div class="logout-btn"><button onclick="location.reload()" style="background:#ff4444; color:white; border:none; padding:8px 15px; border-radius:5px; cursor:pointer;">🚪 Logout</button></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="main-header">📝 Sinhala Handwritten OCR</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Welcome back, {st.session_state.username}! 👋</p>', unsafe_allow_html=True)
    
    # Load OCR model
    with st.spinner("Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load OCR model. Please check your setup.")
        return
    
    st.success("✅ OCR model loaded successfully!")
    
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
                    predicted_text, error = predict_text(image, processor, model, device)
                    if predicted_text:
                        st.session_state.predicted_text = predicted_text
                        st.session_state.prediction_time = datetime.now()
                        st.success("✅ Recognition completed!")
                    else:
                        st.error(f"Error: {error}")
    
    with col2:
        st.markdown("### 📝 Recognition Result")
        
        if st.session_state.predicted_text:
            result_text = st.session_state.predicted_text
            st.markdown(f'<div class="result-box"><strong>📄 Recognized Text:</strong><br><br><span style="font-size: 1.1rem;">{result_text}</span></div>', unsafe_allow_html=True)
            st.caption(f"Recognized at: {st.session_state.prediction_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            col_copy, col_download = st.columns(2)
            with col_copy:
                st.code(result_text)
            with col_download:
                txt_file = io.BytesIO(result_text.encode('utf-8'))
                st.download_button("💾 Download TXT", data=txt_file, file_name=f"ocr_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", use_container_width=True)
        else:
            st.info("👈 Upload an image and click 'Recognize Text' to see results here")
    
    st.markdown("---")
    st.markdown('<div style="text-align: center; color: #888;">Powered by TrOCR | Fine-tuned on SinOCR Dataset</div>', unsafe_allow_html=True)

# ============================================
# PAGE ROUTING
# ============================================

if st.session_state.logged_in and st.session_state.page == 'main':
    main_app()
elif st.session_state.page == 'login':
    login_page()
elif st.session_state.page == 'signup':
    signup_page()
elif st.session_state.page == 'forgot_password':
    forgot_password_page()
else:
    login_page()
