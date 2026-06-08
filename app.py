# ============================================
# SINHALA HANDWRITTEN OCR WEB APP
# Professional Structure: Header → Features → Login → Footer
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
# COLOR SCHEME - Honey Opal Sunset
# ============================================

COLORS = {
    "primary": "#ECB914",
    "secondary": "#F6D579",
    "dark_accent": "#9D8108",
    "light_bg": "#CBB8A0",
    "dark_text": "#4F3D35",
    "white": "#FFFFFF",
    "error": "#D32F2F",
    "success": "#388E3C",
}

# ============================================
# CUSTOM CSS
# ============================================

st.markdown(f"""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main container */
    .stApp {{
        background: linear-gradient(135deg, #faf9f7 0%, {COLORS['light_bg']} 100%);
        min-height: 100vh;
    }}
    
    /* Block container */
    .block-container {{
        padding: 2rem 3rem;
    }}
    
    /* Header Section */
    .header-section {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .main-title {{
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['dark_accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}
    
    .main-subtitle {{
        font-size: 1.1rem;
        color: {COLORS['dark_text']};
        opacity: 0.7;
    }}
    
    /* Features Section */
    .features-section {{
        margin: 3rem 0;
    }}
    
    .section-title {{
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 2rem;
    }}
    
    .feature-card {{
        background: {COLORS['white']};
        border-radius: 15px;
        padding: 25px 20px;
        text-align: center;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05);
        transition: transform 0.3s;
        height: 100%;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.1);
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 15px;
    }}
    
    .feature-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 10px;
    }}
    
    .feature-desc {{
        font-size: 0.85rem;
        color: {COLORS['dark_text']};
        opacity: 0.7;
        line-height: 1.4;
    }}
    
    /* Login Section */
    .login-section {{
        margin: 2rem 0;
    }}
    
    .login-card {{
        background: {COLORS['white']};
        border-radius: 20px;
        padding: 35px;
        max-width: 450px;
        margin: 0 auto;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }}
    
    .login-title {{
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 25px;
    }}
    
    .or-divider {{
        text-align: center;
        margin: 20px 0;
        position: relative;
    }}
    
    .or-divider::before,
    .or-divider::after {{
        content: "";
        position: absolute;
        top: 50%;
        width: 40%;
        height: 1px;
        background: #ddd;
    }}
    
    .or-divider::before {{ left: 0; }}
    .or-divider::after {{ right: 0; }}
    
    .or-divider span {{
        background: {COLORS['white']};
        padding: 0 10px;
        color: #999;
        font-size: 0.8rem;
    }}
    
    /* Footer Section */
    .footer-section {{
        margin-top: 4rem;
        padding: 2rem;
        text-align: center;
        border-top: 1px solid rgba(79,61,53,0.1);
    }}
    
    .footer-text {{
        color: {COLORS['dark_text']};
        opacity: 0.6;
        font-size: 0.8rem;
    }}
    
    /* Form inputs */
    .stTextInput > div > div > input {{
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        padding: 10px 15px;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 2px rgba(236,185,20,0.2);
    }}
    
    /* Buttons */
    .stButton > button {{
        background: {COLORS['primary']};
        color: {COLORS['dark_text']};
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        width: 100%;
        transition: all 0.2s;
    }}
    
    .stButton > button:hover {{
        background: {COLORS['dark_accent']};
        color: white;
        transform: translateY(-2px);
    }}
    
    /* Logout button */
    .logout-btn {{
        position: fixed;
        top: 15px;
        right: 20px;
        background: {COLORS['primary']};
        color: {COLORS['dark_text']};
        border: none;
        border-radius: 25px;
        padding: 8px 20px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        z-index: 1000;
        transition: all 0.2s;
    }}
    
    .logout-btn:hover {{
        background: {COLORS['dark_accent']};
        color: white;
    }}
    
    /* Messages */
    .success-msg {{
        background: #e8f5e9;
        color: #2e7d32;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }}
    
    .error-msg {{
        background: #ffebee;
        color: #c62828;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 15px;
        font-size: 0.9rem;
    }}
    
    /* Stats cards for main app */
    .stat-card {{
        background: {COLORS['white']};
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }}
    
    .stat-number {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORS['primary']};
    }}
    
    .stat-label {{
        font-size: 0.8rem;
        color: {COLORS['dark_text']};
        opacity: 0.7;
    }}
    
    /* Result box */
    .result-box {{
        background: {COLORS['white']};
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid {COLORS['primary']};
        margin-top: 10px;
    }}
    
    /* Welcome banner */
    .welcome-banner {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 15px;
        padding: 25px 30px;
        margin-bottom: 25px;
    }}
    
    .welcome-banner h2 {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 5px;
    }}
    
    hr {{
        margin: 30px 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS['primary']}, transparent);
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE
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
# FUNCTIONS
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
    # ========== HEADER SECTION ==========
    st.markdown("""
    <div class="header-section">
        <div class="main-title">📝 Sinhala Handwritten OCR</div>
        <div class="main-subtitle">Transform handwritten Sinhala documents into digital text with AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # ========== FEATURES SECTION ==========
    st.markdown('<div class="section-title">✨ Why Choose Us</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">AI-powered recognition with 85%+ character accuracy for reliable results</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
            <div class="feature-desc">Get your results in seconds, not minutes. Built for efficiency</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Private</div>
            <div class="feature-desc">Your documents and data stay confidential and secure</div>
        </div>
        """, unsafe_allow_html=True)
    
    # ========== LOGIN SECTION ==========
    st.markdown('<div class="section-title">🔐 Get Started</div>', unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">Welcome Back</div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            email_or_username = st.text_input("Email or Username", placeholder="Enter your email or username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if email_or_username and password:
                    success, result = login_user(email_or_username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = result['username']
                        st.session_state.email = result['email']
                        st.session_state.page = 'main'
                        st.rerun()
                    else:
                        st.markdown(f'<div class="error-msg">❌ {result}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-msg">❌ Please fill all fields</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="or-divider"><span>or</span></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Create Account", use_container_width=True):
                st.session_state.page = 'signup'
                st.rerun()
        with col_b:
            if st.button("Forgot Password?", use_container_width=True):
                st.session_state.page = 'forgot_password'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # ========== FOOTER SECTION ==========
    st.markdown("""
    <div class="footer-section">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR | Fine-tuned on SinOCR Dataset</div>
        <div class="footer-text" style="margin-top: 5px;">All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown("""
    <div class="header-section">
        <div class="main-title">📝 Create Account</div>
        <div class="main-subtitle">Join us and start using Sinhala OCR technology</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="login-title">✏️ Sign Up</div>', unsafe_allow_html=True)
        
        with st.form("signup_form"):
            email = st.text_input("Email Address", placeholder="your@email.com")
            username = st.text_input("Username", placeholder="3-20 characters (letters, numbers, underscore)")
            password = st.text_input("Password", type="password", placeholder="At least 6 characters")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            if st.form_submit_button("Sign Up", use_container_width=True):
                if not email or not username or not password:
                    st.markdown('<div class="error-msg">❌ Please fill all fields</div>', unsafe_allow_html=True)
                elif password != confirm:
                    st.markdown('<div class="error-msg">❌ Passwords do not match</div>', unsafe_allow_html=True)
                else:
                    success, msg = register_user(email, username, password)
                    if success:
                        login_success, login_result = login_user(username, password)
                        if login_success:
                            st.session_state.logged_in = True
                            st.session_state.username = login_result['username']
                            st.session_state.email = login_result['email']
                            st.session_state.page = 'main'
                            st.rerun()
                        else:
                            st.markdown(f'<div class="success-msg">✅ {msg}. Please login.</div>', unsafe_allow_html=True)
                            st.session_state.page = 'login'
                            st.rerun()
                    else:
                        st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.page = 'login'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-section">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown("""
    <div class="header-section">
        <div class="main-title">🔐 Reset Password</div>
        <div class="main-subtitle">We'll help you get back into your account</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        
        if not st.session_state.reset_code_sent:
            st.markdown('<div class="login-title">Forgot Password?</div>', unsafe_allow_html=True)
            
            with st.form("forgot_form"):
                email = st.text_input("Email Address", placeholder="Enter your registered email")
                
                if st.form_submit_button("Send Reset Code", use_container_width=True):
                    if email:
                        success, result = generate_reset_code(email)
                        if success:
                            st.session_state.reset_email = email
                            st.session_state.reset_code_sent = True
                            st.markdown(f'<div class="success-msg">✅ Reset code sent to {email}</div>', unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown(f'<div class="error-msg">❌ {result}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-msg">❌ Please enter your email</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="login-title">Reset Password</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="text-align: center; margin-bottom: 20px;">Resetting for: <strong>{st.session_state.reset_email}</strong></p>', unsafe_allow_html=True)
            
            with st.form("reset_form"):
                code = st.text_input("Reset Code", placeholder="Enter 6-digit code")
                new_password = st.text_input("New Password", type="password", placeholder="At least 6 characters")
                confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter new password")
                
                if st.form_submit_button("Reset Password", use_container_width=True):
                    if code and new_password and confirm:
                        if new_password != confirm:
                            st.markdown('<div class="error-msg">❌ Passwords do not match</div>', unsafe_allow_html=True)
                        elif len(new_password) < 6:
                            st.markdown('<div class="error-msg">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
                        else:
                            if verify_reset_code(st.session_state.reset_email, code):
                                success, msg = reset_password(st.session_state.reset_email, new_password)
                                if success:
                                    st.markdown(f'<div class="success-msg">✅ {msg}</div>', unsafe_allow_html=True)
                                    st.session_state.reset_code_sent = False
                                    st.session_state.reset_email = None
                                    st.session_state.page = 'login'
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="error-msg">❌ Invalid or expired code</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-msg">❌ Please fill all fields</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.reset_code_sent = False
            st.session_state.reset_email = None
            st.session_state.page = 'login'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-section">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN OCR APP
# ============================================

def main_app():
    # Logout button
    st.markdown(f'<button onclick="window.location.href=\'?logout=true\'" class="logout-btn">🚪 Logout</button>', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-section">
        <div class="main-title">📝 Sinhala Handwritten OCR</div>
        <div class="main-subtitle">Upload a handwritten document and get digital text instantly</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome banner
    st.markdown(f'''
    <div class="welcome-banner">
        <h2>👋 Welcome, {st.session_state.username}!</h2>
        <p>Ready to convert your handwritten Sinhala documents to digital text?</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stats
    st.markdown('<div class="section-title" style="font-size: 1.2rem;">📊 System Stats</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">85%+</div><div class="stat-label">Character Accuracy</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">771</div><div class="stat-label">Training Samples</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">104</div><div class="stat-label">Sinhala Characters</div></div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Load model
    with st.spinner("🔄 Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load OCR model")
        return
    
    # Main two-column layout
    col_upload, col_result = st.columns(2)
    
    with col_upload:
        st.markdown("### 📤 Upload Your Document")
        uploaded = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True)
            
            if st.button("🔍 Recognize Text", use_container_width=True):
                with st.spinner("Processing..."):
                    text, error = predict_text(image, processor, model, device)
                    if text:
                        st.session_state.predicted_text = text
                        st.session_state.prediction_time = datetime.now()
                        st.markdown('<div class="success-msg">✅ Recognition complete!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-msg">❌ {error}</div>', unsafe_allow_html=True)
    
    with col_result:
        st.markdown("### 📝 Recognition Result")
        
        if st.session_state.predicted_text:
            st.markdown(f'''
            <div class="result-box">
                <strong>Recognized Text:</strong><br><br>
                {st.session_state.predicted_text}
            </div>
            ''', unsafe_allow_html=True)
            st.caption(f"Recognized at: {st.session_state.prediction_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button("💾 Download as TXT", data=txt_data, file_name=f"ocr_result.txt", use_container_width=True)
        else:
            st.markdown(f'''
            <div class="result-box">
                <strong>No Result Yet</strong><br><br>
                <span style="color: #888;">Upload an image and click "Recognize Text" to see results here</span>
            </div>
            ''', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-section">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR | Fine-tuned on SinOCR Dataset</div>
        <div class="footer-text" style="margin-top: 5px;">All Rights Reserved</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# ROUTING
# ============================================

if 'logout' in st.query_params:
    logout()

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
