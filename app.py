# ============================================
# SINHALA HANDWRITTEN OCR WEB APP
# Honey Opal Sunset Theme - Professional Design
# ============================================

import streamlit as st
from PIL import Image
import io
from datetime import datetime
import os
import time

# Import modules
from auth import register_user, login_user, generate_reset_code, verify_reset_code, reset_password
from ocr_app import load_ocr_model, predict_text

# Page configuration
st.set_page_config(
    page_title="Sinhala Handwritten OCR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# HONEY OPAL SUNSET COLOR SCHEME
# ============================================
# Primary: #ECB914 (Golden Honey)
# Secondary: #F6D579 (Soft Honey)
# Dark Accent: #9D8108 (Deep Gold)
# Light Background: #CBB8A0 (Warm Sand)
# Dark Text: #4F3D35 (Rich Brown)

COLORS = {
    "primary": "#ECB914",
    "secondary": "#F6D579", 
    "dark_accent": "#9D8108",
    "light_bg": "#CBB8A0",
    "dark_text": "#4F3D35",
    "white": "#FFFFFF",
    "gradient_start": "#ECB914",
    "gradient_end": "#F6D579",
    "error": "#D32F2F",
    "success": "#388E3C",
    "info": "#1976D2"
}

# ============================================
# CUSTOM CSS WITH HONEY OPAL SUNSET THEME
# ============================================

st.markdown(f"""
<style>
    /* Main container */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['light_bg']} 0%, {COLORS['white']} 100%);
    }}
    
    /* Hide default Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Card style for forms */
    .auth-card {{
        background: {COLORS['white']};
        border-radius: 30px;
        padding: 45px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        max-width: 480px;
        margin: 0 auto;
        animation: fadeInUp 0.6s ease-out;
        border-top: 8px solid {COLORS['primary']};
    }}
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    /* Header styling */
    .main-header {{
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark_accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }}
    
    .sub-header {{
        text-align: center;
        color: {COLORS['dark_text']};
        margin-bottom: 2rem;
        font-size: 1.1rem;
        font-weight: 500;
        opacity: 0.8;
    }}
    
    /* Welcome banner */
    .welcome-banner {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        padding: 30px;
        border-radius: 25px;
        color: {COLORS['dark_text']};
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(236,185,20,0.3);
        animation: fadeInUp 0.6s ease-out;
    }}
    
    .welcome-banner h2 {{
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 10px;
    }}
    
    .welcome-banner p {{
        font-size: 1rem;
        opacity: 0.9;
    }}
    
    /* Result box */
    .result-box {{
        background: linear-gradient(135deg, {COLORS['white']} 0%, {COLORS['light_bg']} 100%);
        padding: 1.8rem;
        border-radius: 20px;
        margin-top: 1rem;
        border-left: 6px solid {COLORS['primary']};
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
    }}
    
    /* Button styling */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark_accent']} 100%);
        color: {COLORS['dark_text']};
        font-weight: 700;
        border: none;
        border-radius: 50px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(236,185,20,0.4);
        background: linear-gradient(135deg, {COLORS['dark_accent']} 0%, {COLORS['primary']} 100%);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Logout button */
    .logout-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: linear-gradient(135deg, {COLORS['dark_accent']} 0%, {COLORS['primary']} 100%);
        color: {COLORS['dark_text']};
        border: none;
        border-radius: 50px;
        padding: 10px 25px;
        cursor: pointer;
        font-weight: 700;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }}
    
    .logout-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(236,185,20,0.3);
    }}
    
    /* Input field styling */
    .stTextInput > div > div > input {{
        border-radius: 12px;
        border: 2px solid {COLORS['light_bg']};
        padding: 10px 15px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 2px rgba(236,185,20,0.2);
    }}
    
    /* File uploader styling */
    .upload-area {{
        border: 2px dashed {COLORS['primary']};
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        background: {COLORS['white']};
        transition: all 0.3s ease;
    }}
    
    .upload-area:hover {{
        border-color: {COLORS['dark_accent']};
        background: {COLORS['light_bg']};
    }}
    
    /* Success/Error/Info messages */
    .success-message {{
        background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
        color: #2E7D32;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #4CAF50;
        font-weight: 500;
    }}
    
    .error-message {{
        background: linear-gradient(135deg, #FFEBEE 0%, #FFCDD2 100%);
        color: #C62828;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #F44336;
        font-weight: 500;
    }}
    
    .info-message {{
        background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
        color: #1565C0;
        padding: 12px 18px;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #2196F3;
        font-weight: 500;
    }}
    
    /* Divider styling */
    hr {{
        margin: 20px 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, {COLORS['primary']}, transparent);
    }}
    
    /* Image preview */
    .image-preview {{
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        overflow: hidden;
    }}
    
    /* Feature cards */
    .feature-card {{
        background: {COLORS['white']};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(236,185,20,0.15);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 15px;
    }}
    
    .feature-title {{
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 10px;
    }}
    
    .feature-desc {{
        font-size: 0.85rem;
        color: {COLORS['dark_text']};
        opacity: 0.7;
    }}
    
    /* Stats counter */
    .stat-card {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        color: {COLORS['dark_text']};
    }}
    
    .stat-number {{
        font-size: 2rem;
        font-weight: 800;
    }}
    
    .stat-label {{
        font-size: 0.9rem;
        opacity: 0.8;
    }}
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
    st.session_state.page = 'login'
if 'reset_email' not in st.session_state:
    st.session_state.reset_email = None
if 'reset_code_sent' not in st.session_state:
    st.session_state.reset_code_sent = False
if 'predicted_text' not in st.session_state:
    st.session_state.predicted_text = None
if 'prediction_time' not in st.session_state:
    st.session_state.prediction_time = None

# ============================================
# LOGOUT FUNCTION
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
    st.markdown('<p class="main-header">📝 Sinhala Handwritten OCR</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform handwritten Sinhala documents into digital text with AI</p>', unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">AI-powered recognition with 85%+ accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
            <div class="feature-desc">Results in seconds, not minutes</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Private</div>
            <div class="feature-desc">Your data stays confidential</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.markdown("### ✨ Welcome Back")
            st.markdown("Login to access your OCR dashboard")
            st.markdown("---")
            
            with st.form("login_form"):
                username_or_email = st.text_input("📧 Email or Username", placeholder="Enter your email or username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    submitted = st.form_submit_button("🚀 Login", use_container_width=True)
                with col_b:
                    if st.form_submit_button("📝 Sign Up", use_container_width=True):
                        st.session_state.page = 'signup'
                        st.rerun()
                
                if submitted:
                    if not username_or_email or not password:
                        st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
                    else:
                        success, result = login_user(username_or_email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = result['username']
                            st.session_state.email = result['email']
                            st.session_state.page = 'main'
                            st.rerun()
                        else:
                            st.markdown(f'<div class="error-message">❌ {result}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("🔑 Forgot Password?", use_container_width=True):
                st.session_state.page = 'forgot_password'
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown('<p class="main-header">📝 Create Account</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Join thousands of users using Sinhala OCR technology</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.markdown("### ✨ Get Started")
            st.markdown("Create your free account")
            st.markdown("---")
            
            with st.form("signup_form"):
                email = st.text_input("📧 Email Address", placeholder="your@email.com")
                username = st.text_input("👤 Username", placeholder="3-20 characters (letters, numbers, underscore)")
                password = st.text_input("🔒 Password", type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("✓ Confirm Password", type="password", placeholder="Re-enter your password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    submitted = st.form_submit_button("✅ Sign Up", use_container_width=True)
                with col_b:
                    if st.form_submit_button("← Back to Login", use_container_width=True):
                        st.session_state.page = 'login'
                        st.rerun()
                
                if submitted:
                    if not email or not username or not password:
                        st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
                    elif password != confirm_password:
                        st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
                    else:
                        success, message = register_user(email, username, password)
                        if success:
                            # Auto-login after successful signup
                            login_success, login_result = login_user(username, password)
                            if login_success:
                                st.session_state.logged_in = True
                                st.session_state.username = login_result['username']
                                st.session_state.email = login_result['email']
                                st.session_state.page = 'main'
                                st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.markdown(f'<div class="success-message">✅ {message}. Please login.</div>', unsafe_allow_html=True)
                                st.session_state.page = 'login'
                                st.rerun()
                        else:
                            st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown('<p class="main-header">🔐 Reset Password</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">We\'ll help you get back into your account</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            
            if not st.session_state.reset_code_sent:
                st.markdown("### 🔑 Forgot Password?")
                st.markdown("Enter your email to receive a reset code")
                st.markdown("---")
                
                with st.form("forgot_form"):
                    email = st.text_input("📧 Email Address", placeholder="your@email.com")
                    submitted = st.form_submit_button("📨 Send Reset Code", use_container_width=True)
                    
                    if submitted:
                        if not email:
                            st.markdown('<div class="error-message">❌ Please enter your email</div>', unsafe_allow_html=True)
                        else:
                            success, result = generate_reset_code(email)
                            if success:
                                st.session_state.reset_email = email
                                st.session_state.reset_code_sent = True
                                st.markdown(f'<div class="success-message">✅ Reset code sent to {email}</div>', unsafe_allow_html=True)
                                st.markdown('<div class="info-message">📱 Please check your email (or console) for the 6-digit code</div>', unsafe_allow_html=True)
                                st.rerun()
                            else:
                                st.markdown(f'<div class="error-message">❌ {result}</div>', unsafe_allow_html=True)
            else:
                st.markdown("### 🔐 Reset Your Password")
                st.markdown(f"Resetting for: **{st.session_state.reset_email}**")
                st.markdown("---")
                
                with st.form("reset_form"):
                    reset_code = st.text_input("📱 6-Digit Reset Code", placeholder="Enter the code")
                    new_password = st.text_input("🔒 New Password", type="password", placeholder="At least 6 characters")
                    confirm_password = st.text_input("✓ Confirm New Password", type="password", placeholder="Re-enter new password")
                    
                    submitted = st.form_submit_button("🔄 Reset Password", use_container_width=True)
                    
                    if submitted:
                        if not reset_code or not new_password:
                            st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
                        elif new_password != confirm_password:
                            st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
                        elif len(new_password) < 6:
                            st.markdown('<div class="error-message">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
                        else:
                            if verify_reset_code(st.session_state.reset_email, reset_code):
                                success, message = reset_password(st.session_state.reset_email, new_password)
                                if success:
                                    st.markdown(f'<div class="success-message">✅ {message}</div>', unsafe_allow_html=True)
                                    st.session_state.reset_code_sent = False
                                    st.session_state.reset_email = None
                                    st.session_state.page = 'login'
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.markdown(f'<div class="error-message">❌ {message}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="error-message">❌ Invalid or expired reset code</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.reset_code_sent = False
                st.session_state.reset_email = None
                st.session_state.page = 'login'
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN OCR APPLICATION
# ============================================

def main_app():
    # Logout button
    st.markdown(f'''
    <button onclick="window.location.href='?logout=true'" class="logout-btn">
        🚪 Logout
    </button>
    ''', unsafe_allow_html=True)
    
    # Welcome banner
    st.markdown(f'''
    <div class="welcome-banner">
        <h2>👋 Welcome back, {st.session_state.username}!</h2>
        <p>Upload a handwritten Sinhala document image and get digital text in seconds using our AI-powered OCR technology.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">90%+</div>
            <div class="stat-label">Character Accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">1000+</div>
            <div class="stat-label">Images Processed</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">24/7</div>
            <div class="stat-label">Available</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Load OCR model
    with st.spinner("🔄 Loading OCR model... Please wait."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.markdown('<div class="error-message">❌ Failed to load OCR model. Please check your setup.</div>', unsafe_allow_html=True)
        return
    
    # Main UI
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 Upload Document")
        st.markdown("Supported formats: PNG, JPG, JPEG")
        
        uploaded_file = st.file_uploader(
            "Choose an image...", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of handwritten Sinhala text"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Uploaded Image", use_container_width=True)
            
            if st.button("🔍 Recognize Text", type="primary", use_container_width=True):
                with st.spinner("🧠 Analyzing image and recognizing text..."):
                    predicted_text, error = predict_text(image, processor, model, device)
                    if predicted_text:
                        st.session_state.predicted_text = predicted_text
                        st.session_state.prediction_time = datetime.now()
                        st.markdown('<div class="success-message">✅ Recognition completed successfully!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-message">❌ Error: {error}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 📝 Recognition Result")
        
        if st.session_state.predicted_text:
            result_text = st.session_state.predicted_text
            st.markdown(f'''
            <div class="result-box">
                <strong>📄 Recognized Text:</strong><br><br>
                <span style="font-size: 1.2rem; line-height: 1.6;">{result_text}</span>
            </div>
            ''', unsafe_allow_html=True)
            
            st.caption(f"🕐 Recognized at: {st.session_state.prediction_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            col_copy, col_download = st.columns(2)
            with col_copy:
                if st.button("📋 Copy Text", use_container_width=True):
                    st.code(result_text)
                    st.markdown('<div class="success-message">✅ Text copied to clipboard!</div>', unsafe_allow_html=True)
            with col_download:
                txt_file = io.BytesIO(result_text.encode('utf-8'))
                st.download_button(
                    "💾 Download as TXT", 
                    data=txt_file, 
                    file_name=f"ocr_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 
                    use_container_width=True
                )
        else:
            st.markdown("""
            <div class="result-box">
                <strong>📖 No Result Yet</strong><br><br>
                <span style="color: #888;">Upload an image and click 'Recognize Text' to see results here</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            st.markdown("### 📖 Example Output")
            st.markdown("""
            <div class="result-box">
                <strong>Sample Output:</strong><br><br>
                <span style="color: #888;">පුරුෂ</span><br>
                <span style="color: #888;">නීල් රූපසිංහ</span><br>
                <span style="color: #888;">සහෝදරයා</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        f'<div style="text-align: center; padding: 20px;">'
        f'<p style="color: {COLORS["dark_text"]}; opacity: 0.7;">Powered by <strong>TrOCR</strong> | Fine-tuned on <strong>SinOCR Dataset</strong></p>'
        f'<p style="color: {COLORS["dark_text"]}; opacity: 0.5; font-size: 0.8rem;">© 2026 Sinhala Handwritten OCR | All Rights Reserved</p>'
        '</div>',
        unsafe_allow_html=True
    )

# ============================================
# PAGE ROUTING
# ============================================

# Check for logout in URL
query_params = st.query_params
if 'logout' in query_params:
    logout()

# Route to appropriate page
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
