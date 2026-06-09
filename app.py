# SINHALA HANDWRITTEN OCR
# Modern Premium Design - Clean & Attractive
# ============================================

import streamlit as st
from PIL import Image
import io
from datetime import datetime
import os
import time
import random
import string
import sqlite3
import bcrypt
import re

# Page config
st.set_page_config(
    page_title="Sinhala Handwritten OCR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# COLORS - Premium Color Palette
# ============================================

PRIMARY = "#FF6B35"
PRIMARY_DARK = "#E85D2C"
PRIMARY_LIGHT = "#FF8A5C"
SECONDARY = "#2D3436"
ACCENT = "#00B4D8"
BG_DARK = "#1a1a2e"
BG_LIGHT = "#0f0f1a"
CARD_BG = "#16213e"
TEXT_LIGHT = "#FFFFFF"
TEXT_MUTED = "#A0A0B0"
WHITE = "#FFFFFF"
ERROR = "#FF4757"
SUCCESS = "#00D26A"
BORDER = "rgba(255,255,255,0.08)"

# ============================================
# CSS - Premium Modern Design
# ============================================

st.markdown(f"""
<style>
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    header {{visibility: hidden !important;}}
    
    /* Main background */
    .stApp {{
        background: linear-gradient(135deg, {BG_DARK} 0%, {BG_LIGHT} 100%) !important;
        min-height: 100vh;
    }}
    
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    
    /* Main container */
    .main-container {{
        min-height: 100vh;
        display: flex;
        flex-direction: column;
    }}
    
    /* Hero Section */
    .hero-section {{
        text-align: center;
        padding: 3rem 2rem 1rem 2rem;
    }}
    
    .logo-badge {{
        display: inline-block;
        background: rgba(255, 107, 53, 0.15);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.85rem;
        color: {PRIMARY};
        margin-bottom: 1.5rem;
        backdrop-filter: blur(10px);
    }}
    
    .main-title {{
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, {WHITE} 0%, {PRIMARY} 50%, {PRIMARY_LIGHT} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }}
    
    .main-subtitle {{
        font-size: 1.1rem;
        color: {TEXT_MUTED};
        max-width: 600px;
        margin: 0 auto;
    }}
    
    /* Feature Cards */
    .feature-grid {{
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        padding: 2rem;
        flex-wrap: wrap;
    }}
    
    .feature-card {{
        background: rgba(22, 33, 62, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        min-width: 180px;
        border: 1px solid {BORDER};
        transition: all 0.3s ease;
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        border-color: {PRIMARY};
        background: rgba(22, 33, 62, 0.95);
    }}
    
    .feature-icon {{
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }}
    
    .feature-title {{
        font-weight: 600;
        color: {WHITE};
        margin-bottom: 0.25rem;
    }}
    
    .feature-desc {{
        font-size: 0.8rem;
        color: {TEXT_MUTED};
    }}
    
    /* Auth Container - Premium Card */
    .auth-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        flex: 1;
    }}
    
    .auth-card {{
        background: {CARD_BG};
        border-radius: 32px;
        padding: 2.5rem;
        max-width: 450px;
        width: 100%;
        border: 1px solid {BORDER};
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        animation: fadeInUp 0.6s ease;
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
    
    .auth-header {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .auth-title {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {WHITE};
        margin-bottom: 0.5rem;
    }}
    
    .auth-subtitle {{
        font-size: 0.9rem;
        color: {TEXT_MUTED};
    }}
    
    /* Input Styling */
    .stTextInput > div > div > input {{
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid {BORDER} !important;
        border-radius: 14px !important;
        padding: 12px 16px !important;
        color: {WHITE} !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
        background: rgba(255,255,255,0.08) !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {TEXT_MUTED} !important;
    }}
    
    /* Button Styling */
    .stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK}) !important;
        color: {WHITE} !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 12px !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 25px -5px rgba(255, 107, 53, 0.4) !important;
    }}
    
    .secondary-btn > button {{
        background: transparent !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT_MUTED} !important;
    }}
    
    .secondary-btn > button:hover {{
        border-color: {PRIMARY} !important;
        color: {PRIMARY} !important;
        background: rgba(255, 107, 53, 0.05) !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    
    /* Divider */
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: {TEXT_MUTED};
        font-size: 0.8rem;
    }}
    
    .divider::before,
    .divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid {BORDER};
    }}
    
    .divider span {{
        margin: 0 1rem;
    }}
    
    /* Link Row */
    .link-row {{
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
        font-size: 0.85rem;
    }}
    
    .link-row a {{
        color: {PRIMARY};
        text-decoration: none;
        cursor: pointer;
    }}
    
    .link-row a:hover {{
        text-decoration: underline;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {TEXT_MUTED};
        font-size: 0.75rem;
        border-top: 1px solid {BORDER};
        margin-top: auto;
    }}
    
    /* Messages */
    .success-msg {{
        background: rgba(0, 210, 106, 0.1);
        border: 1px solid rgba(0, 210, 106, 0.3);
        color: {SUCCESS};
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }}
    
    .error-msg {{
        background: rgba(255, 71, 87, 0.1);
        border: 1px solid rgba(255, 71, 87, 0.3);
        color: {ERROR};
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }}
    
    /* Main App Styles */
    .welcome-header {{
        background: linear-gradient(135deg, {CARD_BG}, rgba(22, 33, 62, 0.8));
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid {BORDER};
    }}
    
    .stat-card {{
        background: {CARD_BG};
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        border: 1px solid {BORDER};
        transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-3px);
        border-color: {PRIMARY};
    }}
    
    .stat-number {{
        font-size: 2rem;
        font-weight: 700;
        color: {PRIMARY};
    }}
    
    .glass-card {{
        background: {CARD_BG};
        border-radius: 24px;
        padding: 1.5rem;
        border: 1px solid {BORDER};
        height: 100%;
    }}
    
    /* Remove any white boxes */
    div[data-testid="stForm"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    
    div[data-testid="stForm"] > div {{
        background: transparent !important;
    }}
    
    /* Logout button */
    .logout-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: {CARD_BG} !important;
        color: {WHITE} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        padding: 8px 20px !important;
        font-size: 0.85rem !important;
        cursor: pointer !important;
        z-index: 1000 !important;
        transition: all 0.3s ease !important;
    }}
    
    .logout-btn:hover {{
        border-color: {PRIMARY} !important;
        color: {PRIMARY} !important;
    }}
    
    /* Hide Streamlit default elements */
    [data-testid="stVerticalBlock"] > div {{
        background: transparent !important;
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2rem;
        }}
        .auth-card {{
            padding: 1.5rem;
        }}
        .feature-grid {{
            flex-direction: column;
            align-items: center;
        }}
        .feature-card {{
            width: 100%;
            max-width: 300px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE FUNCTIONS
# ============================================

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE,
                  username TEXT UNIQUE,
                  password TEXT)''')
    conn.commit()
    conn.close()

def hash_pw(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_pw(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def register_user(email, username, password):
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return False, "Invalid email format"
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return False, "Username must be 3-20 characters (letters, numbers, underscore)"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ? OR username = ?", (email, username))
    if c.fetchone():
        conn.close()
        return False, "Email or username already exists"
    
    c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
              (email, username, hash_pw(password)))
    conn.commit()
    conn.close()
    return True, "Registration successful!"

def login_user(email_or_username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT username, email, password FROM users WHERE email = ? OR username = ?",
              (email_or_username, email_or_username))
    user = c.fetchone()
    conn.close()
    if user and verify_pw(password, user[2]):
        return True, {"username": user[0], "email": user[1]}
    return False, "Invalid credentials"

def reset_user_password(email, new_password):
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters"
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hash_pw(new_password), email))
    conn.commit()
    conn.close()
    return True, "Password reset successful!"

def email_exists(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

init_db()

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
# LOGOUT
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
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="logo-badge">✨ AI-POWERED OCR</div>
        <div class="main-title">Sinhala Handwritten OCR</div>
        <div class="main-subtitle">Transform handwritten Sinhala documents into digital text with cutting-edge AI technology</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">85%+ Accuracy</div>
            <div class="feature-desc">Advanced deep learning model</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Real-time</div>
            <div class="feature-desc">Instant recognition</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure</div>
            <div class="feature-desc">Your privacy matters</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auth Card
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Welcome Back</div>
        <div class="auth-subtitle">Sign in to continue your journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    email_or_user = st.text_input("", placeholder="Email or Username", key="login_email", label_visibility="collapsed")
    password = st.text_input("", type="password", placeholder="Password", key="login_pass", label_visibility="collapsed")
    
    if st.button("Sign In", key="signin_btn"):
        if email_or_user and password:
            success, result = login_user(email_or_user, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = result['username']
                st.session_state.email = result['email']
                st.session_state.page = 'main'
                st.rerun()
            else:
                st.markdown(f'<div class="error-msg">❌ {result}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-msg">❌ Please fill in all fields</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"><span>or</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account", key="create_acc", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()
    with col2:
        if st.button("Forgot Password?", key="forgot_pw", use_container_width=True):
            st.session_state.page = 'forgot_password'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <div class="logo-badge">✨ JOIN US</div>
        <div class="main-title">Get Started</div>
        <div class="main-subtitle">Create your account and start your OCR journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Create Account</div>
        <div class="auth-subtitle">Join our community today</div>
    </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input("", placeholder="Email Address", key="signup_email", label_visibility="collapsed")
    username = st.text_input("", placeholder="Username", key="signup_user", label_visibility="collapsed")
    password = st.text_input("", type="password", placeholder="Password (min 6 characters)", key="signup_pass", label_visibility="collapsed")
    confirm = st.text_input("", type="password", placeholder="Confirm Password", key="signup_confirm", label_visibility="collapsed")
    
    if st.button("Create Account", key="create_btn"):
        if not email or not username or not password:
            st.markdown('<div class="error-msg">❌ Please fill in all fields</div>', unsafe_allow_html=True)
        elif password != confirm:
            st.markdown('<div class="error-msg">❌ Passwords do not match</div>', unsafe_allow_html=True)
        else:
            success, msg = register_user(email, username, password)
            if success:
                st.markdown(f'<div class="success-msg">✅ {msg}</div>', unsafe_allow_html=True)
                login_success, login_result = login_user(username, password)
                if login_success:
                    st.session_state.logged_in = True
                    st.session_state.username = login_result['username']
                    st.session_state.email = login_result['email']
                    st.session_state.page = 'main'
                    st.rerun()
            else:
                st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"><span>already have an account?</span></div>', unsafe_allow_html=True)
    
    if st.button("← Back to Login", key="back_login", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Secure & Fast</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE - Direct reset without email code
# ============================================

def forgot_password_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <div class="logo-badge">🔐 SECURITY</div>
        <div class="main-title">Reset Password</div>
        <div class="main-subtitle">Enter your email and create a new password</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Create New Password</div>
        <div class="auth-subtitle">We'll verify your email and reset your password</div>
    </div>
    """, unsafe_allow_html=True)
    
    email = st.text_input("", placeholder="Email Address", key="reset_email", label_visibility="collapsed")
    new_password = st.text_input("", type="password", placeholder="New Password (min 6 characters)", key="new_pass", label_visibility="collapsed")
    confirm_password = st.text_input("", type="password", placeholder="Confirm New Password", key="confirm_pass", label_visibility="collapsed")
    
    if st.button("Reset Password", key="reset_btn"):
        if not email or not new_password or not confirm_password:
            st.markdown('<div class="error-msg">❌ Please fill in all fields</div>', unsafe_allow_html=True)
        elif new_password != confirm_password:
            st.markdown('<div class="error-msg">❌ Passwords do not match</div>', unsafe_allow_html=True)
        elif len(new_password) < 6:
            st.markdown('<div class="error-msg">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
        else:
            if email_exists(email):
                success, msg = reset_user_password(email, new_password)
                if success:
                    st.markdown(f'<div class="success-msg">✅ {msg} You can now login with your new password.</div>', unsafe_allow_html=True)
                    time.sleep(1.5)
                    st.session_state.page = 'login'
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-msg">❌ Email not found in our system</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"><span>remember your password?</span></div>', unsafe_allow_html=True)
    
    if st.button("← Back to Login", key="back_login_reset", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Account Recovery</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================

def main_app():
    # Logout button
    col1, col2, col3 = st.columns([8, 1, 1])
    with col3:
        if st.button("🚪 Logout", key="logout_btn"):
            logout()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome Banner
    st.markdown(f"""
    <div class="welcome-header">
        <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
            <div style="flex: 1;">
                <div class="logo-badge" style="display: inline-block;">👋 WELCOME BACK</div>
                <h2 style="color: white; margin: 0.5rem 0;">{st.session_state.username}</h2>
                <p style="color: #A0A0B0; margin: 0;">Ready to convert your handwritten documents? Upload an image below.</p>
            </div>
            <div style="text-align: center; background: rgba(255,107,53,0.1); padding: 1rem 1.5rem; border-radius: 20px;">
                <div style="font-size: 2rem;">📝</div>
                <div style="color: #FF6B35; font-weight: 600;">AI Ready</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">85%+</div>
            <div style="color: #A0A0B0;">Accuracy Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">771</div>
            <div style="color: #A0A0B0;">Training Samples</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">104</div>
            <div style="color: #A0A0B0;">Characters</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="stat-card">
            <div class="stat-number">⚡</div>
            <div style="color: #A0A0B0;">Real-time</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Load OCR Model
    try:
        from ocr_app import load_ocr_model, predict_text
        with st.spinner("🔄 Loading AI Model..."):
            processor, model, device = load_ocr_model()
        
        if processor is None:
            st.error("❌ Failed to load OCR model")
            return
    except Exception as e:
        st.warning("⚠️ OCR Model not loaded. Please ensure ocr_app.py is available.")
        processor, model, device = None, None, None
    
    # Two Column Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; margin-bottom: 1rem;">📤 Upload Image</h3>
        """, unsafe_allow_html=True)
        
        uploaded = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg'],
            label_visibility="collapsed"
        )
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True, caption="Your Uploaded Image")
            
            if processor and st.button("🔍 Recognize Text", use_container_width=True):
                with st.spinner("🧠 Processing image..."):
                    text, error = predict_text(image, processor, model, device)
                    if text:
                        st.session_state.predicted_text = text
                        st.session_state.prediction_time = datetime.now()
                        st.balloons()
                        st.success("✅ Text recognized successfully!")
                    else:
                        st.error(f"❌ Error: {error}")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
                <p style="color: #A0A0B0;">Drag & drop or click to upload<br>a handwritten Sinhala image</p>
                <p style="font-size: 0.8rem; color: #666;">Supports PNG, JPG, JPEG</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3 style="color: white; margin-bottom: 1rem;">📝 Recognized Text</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.predicted_text:
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); border-radius: 16px; padding: 1.5rem; border-left: 4px solid #FF6B35;">
                <strong style="color: #FF6B35;">Output:</strong>
                <p style="color: white; margin-top: 1rem; line-height: 1.6; font-size: 1rem;">
                    {st.session_state.predicted_text}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.prediction_time:
                st.caption(f"🕐 Processed at: {st.session_state.prediction_time.strftime('%I:%M:%S %p')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button(
                "💾 Download as Text",
                data=txt_data,
                file_name="recognized_text.txt",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
                <p style="color: #A0A0B0;">Upload an image and click<br>"Recognize Text" to see results</p>
                <p style="font-size: 0.8rem; color: #666;">Results will appear here</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR • Deep Learning • AI Innovation</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ROUTING
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
