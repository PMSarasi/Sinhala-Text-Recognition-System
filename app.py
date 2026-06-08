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
import random
import string

# Import modules
from auth import register_user, login_user, reset_password
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
# Primary: #ECB914 (Golden Honey) - Buttons, accents, borders
# Secondary: #F6D579 (Soft Honey) - Backgrounds, highlights
# Dark Accent: #9D8108 (Deep Gold) - Hover states, active elements
# Light Background: #CBB8A0 (Warm Sand) - Page background
# Dark Text: #4F3D35 (Rich Brown) - Text color

COLORS = {
    "primary": "#ECB914",
    "secondary": "#F6D579",
    "dark_accent": "#9D8108",
    "light_bg": "#CBB8A0",
    "dark_text": "#4F3D35",
    "white": "#FFFFFF",
    "error": "#D32F2F",
    "success": "#388E3C",
    "info": "#1976D2",
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
        background: {COLORS['light_bg']};
    }}
    
    /* Block container */
    .block-container {{
        padding: 1rem 3rem 2rem 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    /* ========== HEADER SECTION ========== */
    .hero-section {{
        text-align: center;
        padding: 2rem 0 1rem 0;
    }}
    
    .hero-title {{
        font-size: 3rem;
        font-weight: 800;
        color: {COLORS['dark_text']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }}
    
    .hero-icon {{
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .hero-subtitle {{
        font-size: 1.1rem;
        color: {COLORS['dark_text']};
        opacity: 0.7;
        max-width: 600px;
        margin: 0 auto;
    }}
    
    .accent-line {{
        width: 80px;
        height: 3px;
        background: {COLORS['primary']};
        margin: 1.5rem auto;
        border-radius: 3px;
    }}
    
    /* ========== FEATURE CARDS ========== */
    .features-section {{
        padding: 2rem 0;
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
        border-radius: 20px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border-bottom: 3px solid transparent;
        height: 100%;
    }}
    
    .feature-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.12);
        border-bottom-color: {COLORS['primary']};
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }}
    
    .feature-title {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 0.5rem;
    }}
    
    .feature-desc {{
        font-size: 0.85rem;
        color: {COLORS['dark_text']};
        opacity: 0.7;
        line-height: 1.4;
    }}
    
    /* ========== LOGIN/SIGNUP CARDS ========== */
    .auth-card {{
        background: {COLORS['white']};
        border-radius: 24px;
        padding: 2rem;
        max-width: 450px;
        margin: 0 auto;
        box-shadow: 0 20px 50px rgba(0,0,0,0.15);
    }}
    
    .auth-title {{
        text-align: center;
        font-size: 1.6rem;
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 0.5rem;
    }}
    
    .auth-subtitle {{
        text-align: center;
        font-size: 0.85rem;
        color: {COLORS['dark_text']};
        opacity: 0.6;
        margin-bottom: 1.5rem;
    }}
    
    /* ========== BUTTONS ========== */
    .btn-primary {{
        background: {COLORS['primary']};
        color: {COLORS['dark_text']};
        border: none;
        border-radius: 50px;
        padding: 0.7rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }}
    
    .btn-primary:hover {{
        background: {COLORS['dark_accent']};
        color: {COLORS['white']};
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(157,129,8,0.3);
    }}
    
    .btn-secondary {{
        background: transparent;
        color: {COLORS['dark_text']};
        border: 2px solid {COLORS['primary']};
        border-radius: 50px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }}
    
    .btn-secondary:hover {{
        background: {COLORS['primary']};
        color: {COLORS['dark_text']};
        transform: translateY(-2px);
    }}
    
    /* ========== FORM INPUTS ========== */
    .stTextInput > div > div > input {{
        border-radius: 12px;
        border: 1.5px solid #e0e0e0;
        padding: 10px 15px;
        font-size: 0.95rem;
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 3px rgba(236,185,20,0.2);
    }}
    
    /* ========== DIVIDER ========== */
    .divider {{
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
    }}
    
    .divider::before,
    .divider::after {{
        content: "";
        position: absolute;
        top: 50%;
        width: 40%;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS['primary']}, transparent);
    }}
    
    .divider::before {{ left: 0; }}
    .divider::after {{ right: 0; }}
    
    .divider span {{
        background: {COLORS['white']};
        padding: 0 10px;
        color: {COLORS['dark_text']};
        opacity: 0.5;
        font-size: 0.8rem;
    }}
    
    /* ========== MESSAGES ========== */
    .success-msg {{
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        color: #2e7d32;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        border-left: 4px solid #4caf50;
    }}
    
    .error-msg {{
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        color: #c62828;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        border-left: 4px solid #f44336;
    }}
    
    /* ========== FOOTER ========== */
    .footer {{
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(79,61,53,0.1);
    }}
    
    .footer-text {{
        color: {COLORS['dark_text']};
        opacity: 0.5;
        font-size: 0.8rem;
    }}
    
    /* ========== LOGOUT BUTTON ========== */
    .logout-btn {{
        position: fixed;
        top: 15px;
        right: 20px;
        background: {COLORS['primary']};
        color: {COLORS['dark_text']};
        border: none;
        border-radius: 30px;
        padding: 8px 20px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        z-index: 1000;
        transition: all 0.3s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }}
    
    .logout-btn:hover {{
        background: {COLORS['dark_accent']};
        color: {COLORS['white']};
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(157,129,8,0.3);
    }}
    
    /* ========== MAIN APP STYLES ========== */
    .welcome-banner {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
    }}
    
    .welcome-banner h2 {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORS['dark_text']};
        margin-bottom: 0.25rem;
    }}
    
    .stat-card {{
        background: {COLORS['white']};
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-3px);
    }}
    
    .stat-number {{
        font-size: 1.8rem;
        font-weight: 800;
        color: {COLORS['primary']};
    }}
    
    .stat-label {{
        font-size: 0.8rem;
        color: {COLORS['dark_text']};
        opacity: 0.7;
    }}
    
    .result-box {{
        background: {COLORS['white']};
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid {COLORS['primary']};
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
    
    hr {{
        margin: 1.5rem 0;
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
if 'predicted_text' not in st.session_state:
    st.session_state.predicted_text = None
if 'prediction_time' not in st.session_state:
    st.session_state.prediction_time = None

# ============================================
# SIMPLE PASSWORD RESET (No Email Code)
# ============================================

# For demo purposes - store reset tokens in session
if 'reset_tokens' not in st.session_state:
    st.session_state.reset_tokens = {}

def generate_simple_reset(email):
    """Generate a simple reset token (6 digits)"""
    token = ''.join(random.choices(string.digits, k=6))
    st.session_state.reset_tokens[email] = {
        'token': token,
        'expires': time.time() + 3600  # 1 hour expiry
    }
    return token

def verify_simple_reset(email, token):
    """Verify reset token"""
    if email in st.session_state.reset_tokens:
        data = st.session_state.reset_tokens[email]
        if data['token'] == token and time.time() < data['expires']:
            return True
    return False

def clear_reset_token(email):
    """Clear reset token after use"""
    if email in st.session_state.reset_tokens:
        del st.session_state.reset_tokens[email]

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
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-icon">📝</div>
        <div class="hero-title">Sinhala Handwritten OCR</div>
        <div class="hero-subtitle">Transform handwritten Sinhala documents into digital text with AI-powered precision</div>
        <div class="accent-line"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown('<div class="section-title">✨ Why Choose Us</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">AI-powered recognition with 85%+ character accuracy for reliable results</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
            <div class="feature-desc">Get your results in seconds, not minutes. Built for efficiency</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure & Private</div>
            <div class="feature-desc">Your documents and data stay confidential and secure</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Login Card
    st.markdown('<div class="section-title" style="margin-top: 1rem;">🔐 Get Started</div>', unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">Welcome Back</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Login to your account</div>', unsafe_allow_html=True)
        
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
        
        st.markdown('<div class="divider"><span>or</span></div>', unsafe_allow_html=True)
        
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
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR | Fine-tuned on SinOCR Dataset</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-icon">📝</div>
        <div class="hero-title">Create Account</div>
        <div class="hero-subtitle">Join us and start using Sinhala OCR technology</div>
        <div class="accent-line"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-title">Sign Up</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Create your free account</div>', unsafe_allow_html=True)
        
        with st.form("signup_form"):
            email = st.text_input("Email Address", placeholder="your@email.com")
            username = st.text_input("Username", placeholder="3-20 characters")
            password = st.text_input("Password", type="password", placeholder="At least 6 characters")
            confirm = st.text_input("Confirm Password", type="password", placeholder="Re-enter your password")
            
            if st.form_submit_button("Sign Up", use_container_width=True):
                if not email or not username or not password:
                    st.markdown('<div class="error-msg">❌ Please fill all fields</div>', unsafe_allow_html=True)
                elif password != confirm:
                    st.markdown('<div class="error-msg">❌ Passwords do not match</div>', unsafe_allow_html=True)
                elif len(password) < 6:
                    st.markdown('<div class="error-msg">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
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
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE (Simple - No Email)
# ============================================

def forgot_password_page():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-icon">🔐</div>
        <div class="hero-title">Reset Password</div>
        <div class="hero-subtitle">Enter your email to receive a reset code</div>
        <div class="accent-line"></div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        
        if 'reset_step' not in st.session_state:
            st.session_state.reset_step = 'request'
        
        if st.session_state.reset_step == 'request':
            st.markdown('<div class="auth-title">Forgot Password?</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-subtitle">Enter your email to reset your password</div>', unsafe_allow_html=True)
            
            with st.form("reset_request"):
                email = st.text_input("Email Address", placeholder="Enter your registered email")
                
                if st.form_submit_button("Send Reset Code", use_container_width=True):
                    if email:
                        # Check if email exists
                        from auth import login_user
                        # Just check existence by trying to get user
                        import sqlite3
                        conn = sqlite3.connect('users.db')
                        c = conn.cursor()
                        c.execute("SELECT id FROM users WHERE email = ?", (email,))
                        user = c.fetchone()
                        conn.close()
                        
                        if user:
                            token = generate_simple_reset(email)
                            st.session_state.reset_email = email
                            st.session_state.reset_token = token
                            st.session_state.reset_step = 'verify'
                            st.markdown(f'<div class="success-msg">✅ Reset code: <strong>{token}</strong><br>Please use this code to reset your password.</div>', unsafe_allow_html=True)
                            st.rerun()
                        else:
                            st.markdown('<div class="error-msg">❌ Email not found</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-msg">❌ Please enter your email</div>', unsafe_allow_html=True)
        
        elif st.session_state.reset_step == 'verify':
            st.markdown('<div class="auth-title">Reset Password</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="auth-subtitle">Resetting for: {st.session_state.reset_email}</div>', unsafe_allow_html=True)
            
            with st.form("reset_verify"):
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
                            if verify_simple_reset(st.session_state.reset_email, code):
                                success, msg = reset_password(st.session_state.reset_email, new_password)
                                if success:
                                    clear_reset_token(st.session_state.reset_email)
                                    st.markdown(f'<div class="success-msg">✅ {msg}</div>', unsafe_allow_html=True)
                                    st.session_state.reset_step = 'request'
                                    st.session_state.reset_email = None
                                    st.session_state.reset_token = None
                                    time.sleep(1)
                                    st.session_state.page = 'login'
                                    st.rerun()
                                else:
                                    st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="error-msg">❌ Invalid or expired code</div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="error-msg">❌ Please fill all fields</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("← Back to Login", use_container_width=True):
            st.session_state.reset_step = 'request'
            st.session_state.reset_email = None
            st.session_state.reset_token = None
            st.session_state.page = 'login'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN OCR APP
# ============================================

def main_app():
    # Logout button with working JavaScript
    st.markdown(f'''
    <button onclick="window.location.href='?logout=true'" class="logout-btn">
        🚪 Logout
    </button>
    ''', unsafe_allow_html=True)
    
    # Welcome Banner
    st.markdown(f'''
    <div class="welcome-banner">
        <h2>👋 Welcome back, {st.session_state.username}!</h2>
        <p>Ready to convert your handwritten Sinhala documents to digital text?</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stats Section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">85%+</div><div class="stat-label">Character Accuracy</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">771</div><div class="stat-label">Training Samples</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">104</div><div class="stat-label">Sinhala Characters</div></div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Load OCR Model
    with st.spinner("🔄 Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load OCR model")
        return
    
    # Main Upload Section
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
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR | Fine-tuned on SinOCR Dataset</div>
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
