# SINHALA HANDWRITTEN OCR
# Premium Clean Design - Matching Reference Style
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
# COLORS - Clean Professional Palette
# ============================================

PRIMARY = "#FF6B35"
PRIMARY_DARK = "#E85D2C"
PRIMARY_LIGHT = "#FF8A5C"
SECONDARY = "#4A5568"
BG_WHITE = "#FFFFFF"
BG_GRAY = "#F7FAFC"
TEXT_DARK = "#1A202C"
TEXT_GRAY = "#718096"
TEXT_LIGHT = "#A0AEC0"
SUCCESS = "#38A169"
ERROR = "#E53E3E"
BORDER = "#E2E8F0"

# ============================================
# CSS - Clean Modern Design (Matching Reference)
# ============================================

st.markdown(f"""
<style>
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    header {{visibility: hidden !important;}}
    
    /* Main background */
    .stApp {{
        background: linear-gradient(135deg, {BG_GRAY} 0%, {BG_WHITE} 100%) !important;
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
    
    /* Header Section */
    .header-section {{
        text-align: center;
        padding: 2rem 2rem 0 2rem;
    }}
    
    .logo {{
        font-size: 3rem;
        margin-bottom: 1rem;
    }}
    
    .main-title {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    
    .main-subtitle {{
        font-size: 1rem;
        color: {TEXT_GRAY};
        max-width: 500px;
        margin: 0 auto;
    }}
    
    /* Auth Container */
    .auth-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
        flex: 1;
    }}
    
    .auth-card {{
        background: {BG_WHITE};
        border-radius: 24px;
        padding: 2.5rem;
        max-width: 440px;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
        border: 1px solid {BORDER};
    }}
    
    .auth-header {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .auth-title {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
    }}
    
    .auth-subtitle {{
        font-size: 0.9rem;
        color: {TEXT_GRAY};
    }}
    
    /* Input Fields - Clean Style */
    .input-label {{
        font-size: 0.85rem;
        font-weight: 500;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
        display: block;
    }}
    
    .stTextInput > div > div > input {{
        background: {BG_WHITE} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        color: {TEXT_DARK} !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        margin-bottom: 1rem;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
        outline: none !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {TEXT_LIGHT} !important;
    }}
    
    /* Button Styling */
    .stButton > button {{
        width: 100%;
        background: {PRIMARY} !important;
        color: white !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin-top: 0.5rem;
    }}
    
    .stButton > button:hover {{
        background: {PRIMARY_DARK} !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Divider */
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
        color: {TEXT_GRAY};
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
    
    /* Link Buttons Row */
    .link-buttons {{
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }}
    
    .link-buttons .stButton {{
        flex: 1;
    }}
    
    .link-buttons .stButton > button {{
        background: transparent !important;
        color: {TEXT_GRAY} !important;
        border: 1px solid {BORDER} !important;
        box-shadow: none !important;
    }}
    
    .link-buttons .stButton > button:hover {{
        border-color: {PRIMARY} !important;
        color: {PRIMARY} !important;
        background: transparent !important;
        transform: none !important;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        padding: 2rem;
        color: {TEXT_GRAY};
        font-size: 0.75rem;
        border-top: 1px solid {BORDER};
        margin-top: auto;
    }}
    
    /* Messages */
    .success-msg {{
        background: #F0FFF4;
        border: 1px solid #C6F6D5;
        color: {SUCCESS};
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }}
    
    .error-msg {{
        background: #FFF5F5;
        border: 1px solid #FED7D7;
        color: {ERROR};
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }}
    
    /* Checkbox styling */
    .stCheckbox {{
        margin: 1rem 0;
    }}
    
    .stCheckbox label {{
        color: {TEXT_GRAY};
        font-size: 0.85rem;
    }}
    
    /* Hide form backgrounds */
    div[data-testid="stForm"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    
    div[data-testid="stForm"] > div {{
        background: transparent !important;
    }}
    
    /* Main App Styles */
    .main-header {{
        background: {BG_WHITE};
        border-bottom: 1px solid {BORDER};
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}
    
    .welcome-card {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
        border-radius: 20px;
        padding: 2rem;
        color: white;
        margin-bottom: 2rem;
    }}
    
    .stat-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }}
    
    .stat-item {{
        background: {BG_WHITE};
        border-radius: 16px;
        padding: 1.25rem;
        text-align: center;
        border: 1px solid {BORDER};
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }}
    
    .stat-number {{
        font-size: 1.75rem;
        font-weight: 700;
        color: {PRIMARY};
    }}
    
    .glass-card {{
        background: {BG_WHITE};
        border-radius: 20px;
        padding: 1.5rem;
        border: 1px solid {BORDER};
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        height: 100%;
    }}
    
    .result-area {{
        background: #F7FAFC;
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid {PRIMARY};
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .auth-card {{
            padding: 1.5rem;
        }}
        .main-title {{
            font-size: 1.75rem;
        }}
        .stat-grid {{
            grid-template-columns: repeat(2, 1fr);
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
if 'remember_me' not in st.session_state:
    st.session_state.remember_me = False

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
# LOGIN PAGE - Clean & Professional
# ============================================

def login_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-section">
        <div class="logo">📝</div>
        <div class="main-title">Sinhala Handwritten OCR</div>
        <div class="main-subtitle">Transform handwritten Sinhala into digital text</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auth Card
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Welcome Back</div>
        <div class="auth-subtitle">Sign in to continue your journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input fields with labels
    st.markdown('<label class="input-label">Email or Username</label>', unsafe_allow_html=True)
    email_or_user = st.text_input("", placeholder="Enter your email or username", key="login_email", label_visibility="collapsed")
    
    st.markdown('<label class="input-label">Password</label>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Enter your password", key="login_pass", label_visibility="collapsed")
    
    # Remember me checkbox
    remember = st.checkbox("Remember me", key="remember_me")
    
    # Sign In button
    if st.button("Sign In", key="signin_btn"):
        if email_or_user and password:
            success, result = login_user(email_or_user, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = result['username']
                st.session_state.email = result['email']
                st.session_state.remember_me = remember
                st.session_state.page = 'main'
                st.rerun()
            else:
                st.markdown(f'<div class="error-msg">❌ {result}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="error-msg">❌ Please fill in all fields</div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="divider"><span>or</span></div>', unsafe_allow_html=True)
    
    # Link buttons
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
    
    # Footer
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-section">
        <div class="logo">📝</div>
        <div class="main-title">Create Account</div>
        <div class="main-subtitle">Join us and start your OCR journey</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Get Started</div>
        <div class="auth-subtitle">Create your free account</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<label class="input-label">Email Address</label>', unsafe_allow_html=True)
    email = st.text_input("", placeholder="Enter your email", key="signup_email", label_visibility="collapsed")
    
    st.markdown('<label class="input-label">Username</label>', unsafe_allow_html=True)
    username = st.text_input("", placeholder="Choose a username", key="signup_user", label_visibility="collapsed")
    
    st.markdown('<label class="input-label">Password</label>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Create a password (min 6 characters)", key="signup_pass", label_visibility="collapsed")
    
    st.markdown('<label class="input-label">Confirm Password</label>', unsafe_allow_html=True)
    confirm = st.text_input("", type="password", placeholder="Confirm your password", key="signup_confirm", label_visibility="collapsed")
    
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
    
    st.markdown('<div class="divider"><span>Already have an account?</span></div>', unsafe_allow_html=True)
    
    if st.button("← Back to Login", key="back_login", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Secure & Fast</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-section">
        <div class="logo">🔐</div>
        <div class="main-title">Reset Password</div>
        <div class="main-subtitle">We'll help you get back in</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-title">Create New Password</div>
        <div class="auth-subtitle">Enter your email and new password</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<label class="input-label">Email Address</label>', unsafe_allow_html=True)
    email = st.text_input("", placeholder="Enter your registered email", key="reset_email", label_visibility="collapsed")
    
    st.markdown('<label class="input-label">New Password</label>', unsafe_allow_html=True)
    new_password = st.text_input("", type="password", placeholder="Create new password (min 6 characters)", key="new_pass", label_visibility="collapsed")
    
    st.markdown('<label class="input-label">Confirm New Password</label>', unsafe_allow_html=True)
    confirm_password = st.text_input("", type="password", placeholder="Confirm your new password", key="confirm_pass", label_visibility="collapsed")
    
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
    
    st.markdown('<div class="divider"><span>Remember your password?</span></div>', unsafe_allow_html=True)
    
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
    # Header with logout
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"""
        <div style="padding: 1rem 0;">
            <h1 style="color: #1A202C; font-size: 1.5rem;">📝 Sinhala Handwritten OCR</h1>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", key="logout_btn"):
            logout()
    
    st.markdown('<div class="main-container" style="padding: 0 2rem;">', unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown(f"""
    <div class="welcome-card">
        <h2 style="margin: 0 0 0.5rem 0;">👋 Welcome back, {st.session_state.username}!</h2>
        <p style="margin: 0; opacity: 0.9;">Ready to convert your handwritten Sinhala documents? Upload an image below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Grid
    st.markdown("""
    <div class="stat-grid">
        <div class="stat-item">
            <div class="stat-number">85%+</div>
            <div style="color: #718096;">Accuracy Rate</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">771</div>
            <div style="color: #718096;">Training Samples</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">104</div>
            <div style="color: #718096;">Characters</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">⚡</div>
            <div style="color: #718096;">Real-time</div>
        </div>
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
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #1A202C; margin-bottom: 1rem;">📤 Upload Image</h3>', unsafe_allow_html=True)
        
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
                <p style="color: #718096;">Drag & drop or click to upload<br>a handwritten Sinhala image</p>
                <p style="font-size: 0.8rem; color: #A0AEC0;">Supports PNG, JPG, JPEG</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #1A202C; margin-bottom: 1rem;">📝 Recognized Text</h3>', unsafe_allow_html=True)
        
        if st.session_state.predicted_text:
            st.markdown(f"""
            <div class="result-area">
                <strong style="color: #FF6B35;">Output:</strong>
                <p style="color: #2D3748; margin-top: 1rem; line-height: 1.6;">
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
                <p style="color: #718096;">Upload an image and click<br>"Recognize Text" to see results</p>
                <p style="font-size: 0.8rem; color: #A0AEC0;">Results will appear here</p>
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
