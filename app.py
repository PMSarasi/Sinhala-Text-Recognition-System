# ============================================
# SINHALA HANDWRITTEN OCR
# Modern Professional Design - Enhanced
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

# Page config
st.set_page_config(
    page_title="Sinhala Handwritten OCR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# COLORS
# ============================================

PRIMARY = "#ECB914"
PRIMARY_DARK = "#D4A010"
SECONDARY = "#F6D579"
BG_LIGHT = "#F5F0E8"
TEXT_DARK = "#2C1810"
WHITE = "#FFFFFF"
ERROR = "#E53935"
SUCCESS = "#43A047"
CARD_BG = "#FFFFFF"
ACCENT = "#8B6914"

# ============================================
# CSS - COMPLETELY REDESIGNED
# ============================================

st.markdown(f"""
<style>
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    header {{visibility: hidden !important;}}
    
    /* Remove default Streamlit padding */
    .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    
    /* Hide Streamlit default elements */
    [data-testid="stAppViewContainer"] {{
        background: none !important;
    }}
    
    .stApp {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, #EDE4D3 50%, #E8DCC8 100%) !important;
        min-height: 100vh;
    }}
    
    /* Remove form borders and backgrounds */
    [data-testid="stForm"] {{
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }}
    
    /* Main container */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 1.5rem 2rem;
    }}
    
    /* Hero section */
    .hero-section {{
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeIn 0.8s ease;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .main-title {{
        font-size: 3rem;
        font-weight: 800;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, {TEXT_DARK}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    .main-subtitle {{
        font-size: 1.1rem;
        color: #6B5B4F;
        font-weight: 400;
        margin-bottom: 1.5rem;
    }}
    
    /* Feature cards - Glass morphism */
    .feature-grid {{
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin-bottom: 2.5rem;
        flex-wrap: wrap;
    }}
    
    .feature-item {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 200px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        border: 1px solid rgba(255,255,255,0.8);
        transition: all 0.3s ease;
        animation: slideUp 0.6s ease;
    }}
    
    .feature-item:hover {{
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        border-color: {PRIMARY};
    }}
    
    @keyframes slideUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        display: block;
    }}
    
    .feature-title {{
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 0.25rem;
        font-size: 1.1rem;
    }}
    
    .feature-desc {{
        font-size: 0.85rem;
        color: #8B7B6B;
    }}
    
    /* Auth card - Modern floating */
    .auth-card {{
        background: {WHITE};
        border-radius: 24px;
        padding: 2.5rem 2rem;
        max-width: 420px;
        margin: 0 auto;
        box-shadow: 0 20px 60px rgba(0,0,0,0.08);
        border: 1px solid rgba(236, 185, 20, 0.1);
        position: relative;
    }}
    
    .auth-card::before {{
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: linear-gradient(45deg, {PRIMARY}, {SECONDARY}, {PRIMARY});
        border-radius: 24px;
        z-index: -1;
        opacity: 0.3;
    }}
    
    .auth-title {{
        text-align: center;
        font-size: 1.8rem;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 1.8rem;
    }}
    
    /* Modern buttons */
    .stButton > button {{
        width: 100%;
        background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK}) !important;
        color: {TEXT_DARK} !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 1.5rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(236, 185, 20, 0.3) !important;
        font-size: 1rem !important;
        letter-spacing: 0.3px !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, {PRIMARY_DARK}, #C4940A) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(236, 185, 20, 0.4) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}
    
    /* Secondary button */
    .secondary-btn > button {{
        background: {WHITE} !important;
        color: {TEXT_DARK} !important;
        border: 2px solid {PRIMARY} !important;
        box-shadow: none !important;
    }}
    
    .secondary-btn > button:hover {{
        background: {BG_LIGHT} !important;
        border-color: {PRIMARY_DARK} !important;
    }}
    
    /* Input styling - Modern minimal */
    .stTextInput input {{
        border-radius: 12px !important;
        border: 2px solid #E8DCC8 !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        background: {WHITE} !important;
        transition: all 0.3s ease !important;
        color: {TEXT_DARK} !important;
    }}
    
    .stTextInput input:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(236, 185, 20, 0.1) !important;
        outline: none !important;
    }}
    
    .stTextInput input::placeholder {{
        color: #B8A898 !important;
    }}
    
    /* Remove Streamlit's default form background */
    div[data-testid="stForm"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    
    div[data-testid="stForm"] > div {{
        background: transparent !important;
    }}
    
    /* Divider */
    .divider {{
        text-align: center;
        margin: 1.5rem 0;
        color: #B8A898;
        font-size: 0.85rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }}
    
    .divider::before,
    .divider::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: #E8DCC8;
    }}
    
    /* Messages */
    .success-msg {{
        background: linear-gradient(135deg, #E8F5E9, #C8E6C9);
        color: #2E7D32;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        border-left: 4px solid #43A047;
        animation: slideIn 0.3s ease;
    }}
    
    .error-msg {{
        background: linear-gradient(135deg, #FFEBEE, #FFCDD2);
        color: #C62828;
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        border-left: 4px solid #E53935;
        animation: slideIn 0.3s ease;
    }}
    
    @keyframes slideIn {{
        from {{ opacity: 0; transform: translateX(-10px); }}
        to {{ opacity: 1; transform: translateX(0); }}
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(139, 105, 20, 0.1);
        font-size: 0.8rem;
        color: #8B7B6B;
    }}
    
    /* Logout button */
    .logout-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: {WHITE} !important;
        color: {TEXT_DARK} !important;
        border: 2px solid {PRIMARY} !important;
        border-radius: 50px !important;
        padding: 10px 20px !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        z-index: 1000 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
        transition: all 0.3s ease !important;
    }}
    
    .logout-btn:hover {{
        background: {PRIMARY} !important;
        transform: translateY(-2px) !important;
    }}
    
    /* Welcome banner - Gradient */
    .welcome-box {{
        background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
        border-radius: 20px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(236, 185, 20, 0.2);
    }}
    
    /* Stats */
    .stats-row {{
        display: flex;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }}
    
    .stat-box {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        flex: 1;
        min-width: 150px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.05);
        border: 1px solid rgba(255,255,255,0.8);
        transition: all 0.3s ease;
    }}
    
    .stat-box:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.1);
    }}
    
    .stat-number {{
        font-size: 2rem;
        font-weight: 800;
        color: {PRIMARY};
        background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    
    /* Upload & Result columns */
    .column-container {{
        background: {WHITE};
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        min-height: 400px;
    }}
    
    .result-box {{
        background: linear-gradient(135deg, #FEFAF3, #FDF5E6);
        border-radius: 16px;
        padding: 1.5rem;
        border-left: 4px solid {PRIMARY};
        margin-top: 1rem;
    }}
    
    /* Hide Streamlit's default padding */
    div[data-testid="stVerticalBlock"] > div {{
        background: transparent !important;
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2rem;
        }}
        .feature-grid {{
            flex-direction: column;
        }}
        .auth-card {{
            padding: 2rem 1.5rem;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE (Keeping your existing code)
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
    import re
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
    return True, "Registration successful! Welcome aboard! 🎉"

def login_user(email_or_username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT username, email, password FROM users WHERE email = ? OR username = ?",
              (email_or_username, email_or_username))
    user = c.fetchone()
    conn.close()
    if user and verify_pw(password, user[2]):
        return True, {"username": user[0], "email": user[1]}
    return False, "Invalid credentials. Please try again."

def reset_user_password(email, new_password):
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters"
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hash_pw(new_password), email))
    conn.commit()
    conn.close()
    return True, "Password reset successful! Please login."

def email_exists(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

init_db()

# ============================================
# SESSION (Keeping your existing code)
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
if 'reset_tokens' not in st.session_state:
    st.session_state.reset_tokens = {}
if 'reset_step' not in st.session_state:
    st.session_state.reset_step = 'request'
if 'reset_email' not in st.session_state:
    st.session_state.reset_email = None

# ============================================
# RESET (Keeping your existing code)
# ============================================

def generate_token(email):
    token = ''.join(random.choices(string.digits, k=6))
    st.session_state.reset_tokens[email] = {'token': token, 'expires': time.time() + 3600}
    return token

def verify_token(email, token):
    if email in st.session_state.reset_tokens:
        data = st.session_state.reset_tokens[email]
        if data['token'] == token and time.time() < data['expires']:
            return True
    return False

def clear_token(email):
    if email in st.session_state.reset_tokens:
        del st.session_state.reset_tokens[email]

# ============================================
# OCR (Keeping your existing code)
# ============================================

from ocr_app import load_ocr_model, predict_text

# ============================================
# LOGOUT (Keeping your existing code)
# ============================================

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.email = None
    st.session_state.page = 'login'
    st.session_state.predicted_text = None
    st.rerun()

# ============================================
# LOGIN PAGE - REDESIGNED
# ============================================

def login_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Hero section
    st.markdown(f"""
    <div class="hero-section">
        <div class="main-title">📝 Sinhala Handwritten OCR</div>
        <div class="main-subtitle">Transform handwritten Sinhala documents into digital text with AI-powered precision</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-item">
            <span class="feature-icon">🎯</span>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">85%+ recognition rate with advanced deep learning</div>
        </div>
        <div class="feature-item">
            <span class="feature-icon">⚡</span>
            <div class="feature-title">Lightning Fast</div>
            <div class="feature-desc">Get results in seconds, not minutes</div>
        </div>
        <div class="feature-item">
            <span class="feature-icon">🔒</span>
            <div class="feature-title">Secure & Private</div>
            <div class="feature-desc">Your data stays with you, always encrypted</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Auth card
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="auth-title">Welcome Back 👋</div>', unsafe_allow_html=True)
    
    # Using columns to remove white box effect
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        email_or_user = st.text_input("", placeholder="📧 Email or Username", key="login_email", label_visibility="collapsed")
        password = st.text_input("", type="password", placeholder="🔒 Password", key="login_pass", label_visibility="collapsed")
        
        col_btn1, col_btn2 = st.columns([3, 1])
        with col_btn1:
            if st.button("✨ Sign In", use_container_width=True, key="signin_btn"):
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
    
    # Divider
    st.markdown('<div class="divider">or continue with</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Create Account", use_container_width=True, key="create_acc"):
            st.session_state.page = 'signup'
            st.rerun()
    with col2:
        if st.button("🔑 Forgot Password?", use_container_width=True, key="forgot_pw"):
            st.session_state.page = 'forgot_password'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR • AI • Innovation</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE - REDESIGNED
# ============================================

def signup_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="hero-section">
        <div class="main-title">📝 Create Account</div>
        <div class="main-subtitle">Join our community and unlock the power of Sinhala OCR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="auth-title">Get Started 🚀</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        email = st.text_input("", placeholder="📧 Email Address", key="signup_email", label_visibility="collapsed")
        username = st.text_input("", placeholder="👤 Username", key="signup_user", label_visibility="collapsed")
        password = st.text_input("", type="password", placeholder="🔒 Password (min 6 characters)", key="signup_pass", label_visibility="collapsed")
        confirm = st.text_input("", type="password", placeholder="🔒 Confirm Password", key="signup_confirm", label_visibility="collapsed")
        
        if st.button("🎉 Create Account", use_container_width=True, key="create_btn"):
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
    
    st.markdown("---")
    if st.button("← Back to Login", use_container_width=True, key="back_login"):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Secure • Fast • Accurate</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE - REDESIGNED
# ============================================

def forgot_password_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="hero-section">
        <div class="main-title">🔐 Reset Password</div>
        <div class="main-subtitle">Don't worry, we'll help you get back in</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.reset_step == 'request':
        st.markdown(f'<div class="auth-title">Forgot Password?</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            email = st.text_input("", placeholder="📧 Enter your email address", key="reset_email_input", label_visibility="collapsed")
            
            if st.button("📤 Send Reset Code", use_container_width=True, key="send_reset"):
                if email:
                    if email_exists(email):
                        token = generate_token(email)
                        st.session_state.reset_email = email
                        st.session_state.reset_step = 'verify'
                        st.markdown(f"""
                        <div class="success-msg">
                            ✅ Reset code generated successfully!<br>
                            <strong>Your Code: {token}</strong><br>
                            <small>Use this code to reset your password. Valid for 1 hour.</small>
                        </div>
                        """, unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-msg">❌ Email not found in our system</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-msg">❌ Please enter your email address</div>', unsafe_allow_html=True)
    
    elif st.session_state.reset_step == 'verify':
        st.markdown(f'<div class="auth-title">Create New Password</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.markdown(f"""
            <p style="text-align:center; color:#8B7B6B; margin-bottom:1rem;">
                Resetting password for<br><strong>{st.session_state.reset_email}</strong>
            </p>
            """, unsafe_allow_html=True)
            
            code = st.text_input("", placeholder="🔢 Enter 6-Digit Code", key="reset_code", label_visibility="collapsed")
            new_password = st.text_input("", type="password", placeholder="🔒 New Password", key="new_pass", label_visibility="collapsed")
            confirm = st.text_input("", type="password", placeholder="🔒 Confirm New Password", key="confirm_pass", label_visibility="collapsed")
            
            if st.button("🔄 Reset Password", use_container_width=True, key="reset_btn"):
                if code and new_password and confirm:
                    if new_password != confirm:
                        st.markdown('<div class="error-msg">❌ Passwords do not match</div>', unsafe_allow_html=True)
                    elif len(new_password) < 6:
                        st.markdown('<div class="error-msg">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
                    else:
                        if verify_token(st.session_state.reset_email, code):
                            success, msg = reset_user_password(st.session_state.reset_email, new_password)
                            if success:
                                clear_token(st.session_state.reset_email)
                                st.markdown(f'<div class="success-msg">✅ {msg}</div>', unsafe_allow_html=True)
                                st.session_state.reset_step = 'request'
                                st.session_state.reset_email = None
                                time.sleep(1.5)
                                st.session_state.page = 'login'
                                st.rerun()
                            else:
                                st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-msg">❌ Invalid or expired code</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-msg">❌ Please fill in all fields</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("← Back to Login", use_container_width=True, key="back_login_reset"):
        st.session_state.reset_step = 'request'
        st.session_state.reset_email = None
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Security First</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN APP - REDESIGNED
# ============================================

def main_app():
    # Logout button
    st.markdown(f"""
    <div style="position: fixed; top: 20px; right: 20px; z-index: 1000;">
        <form action="/?logout=true" method="get">
            <button type="submit" class="logout-btn">🚪 Logout</button>
        </form>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome banner
    st.markdown(f"""
    <div class="welcome-box">
        <strong style="font-size: 1.3rem;">👋 Welcome back, {st.session_state.username}!</strong>
        <p style="margin-top: 8px; font-size: 0.95rem; opacity: 0.9;">Ready to convert your handwritten Sinhala documents? Upload an image below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
    <div class="stats-row">
        <div class="stat-box">
            <div class="stat-number">85%+</div>
            <div style="color: #6B5B4F; font-size: 0.9rem;">Accuracy Rate</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">771</div>
            <div style="color: #6B5B4F; font-size: 0.9rem;">Training Samples</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">104</div>
            <div style="color: #6B5B4F; font-size: 0.9rem;">Characters Recognized</div>
        </div>
        <div class="stat-box">
            <div class="stat-number">⚡</div>
            <div style="color: #6B5B4F; font-size: 0.9rem;">Real-time Processing</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    with st.spinner("🔄 Loading AI model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("❌ Failed to load OCR model. Please try again.")
        return
    
    # Two columns layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="column-container">
            <h3 style="color: #2C1810; margin-bottom: 1rem;">📤 Upload Image</h3>
        """, unsafe_allow_html=True)
        
        uploaded = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg'],
            label_visibility="collapsed"
        )
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True, caption="Uploaded Image")
            
            if st.button("🔍 Recognize Text", use_container_width=True):
                with st.spinner("🧠 Processing image..."):
                    text, error = predict_text(image, processor, model, device)
                    if text:
                        st.session_state.predicted_text = text
                        st.session_state.prediction_time = datetime.now()
                        st.balloons()
                    else:
                        st.error(f"❌ Error: {error}")
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #B8A898;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📸</div>
                <p style="font-size: 1rem;">Drag & drop or click to upload<br>a handwritten Sinhala image</p>
                <p style="font-size: 0.8rem;">Supports PNG, JPG, JPEG</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="column-container">
            <h3 style="color: #2C1810; margin-bottom: 1rem;">📝 Recognized Text</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.predicted_text:
            st.markdown(f"""
            <div class="result-box">
                <strong style="color: #2C1810;">Output:</strong><br><br>
                <span style="font-size: 1.1rem; line-height: 1.8; color: #2C1810;">
                    {st.session_state.predicted_text}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            st.caption(f"🕐 Processed at: {st.session_state.prediction_time.strftime('%I:%M:%S %p')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button(
                "💾 Download Text",
                data=txt_data,
                file_name="recognized_text.txt",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div style="text-align: center; padding: 3rem 1rem; color: #B8A898;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">📄</div>
                <p style="font-size: 1rem;">Upload an image and click<br>"Recognize Text" to see results</p>
                <p style="font-size: 0.8rem;">Results will appear here instantly</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR • Deep Learning • Innovation</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ROUTING (Keeping your existing code)
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
