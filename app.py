# ============================================
# SINHALA HANDWRITTEN OCR WEB APP
# Professional Design - Honey Opal Sunset Theme
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

# Page configuration
st.set_page_config(
    page_title="Sinhala Handwritten OCR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# COLOR SCHEME
# ============================================

COLORS = {
    "primary": "#ECB914",
    "primary-dark": "#D4A010",
    "primary-darker": "#9D8108",
    "secondary": "#F6D579",
    "bg-light": "#CBB8A0",
    "text-dark": "#4F3D35",
    "text-light": "#FFFFFF",
    "error": "#E53935",
    "error-light": "#FFEBEE",
    "success": "#43A047",
    "success-light": "#E8F5E9",
    "border": "#E0E0E0",
    "shadow": "rgba(0,0,0,0.08)",
}

# ============================================
# PERFECT CSS - Clean & Professional
# ============================================

st.markdown(f"""
<style>
    /* Reset & Base */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    /* Hide Streamlit Default Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main Container */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg-light']} 0%, #D4C5B5 100%);
        min-height: 100vh;
    }}
    
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }}
    
    /* ========== TYPOGRAPHY ========== */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    html, body, .stApp, div, p, h1, h2, h3, h4, h5, h6, span, a, button, input {{
        font-family: 'Poppins', sans-serif !important;
    }}
    
    /* ========== HERO SECTION ========== */
    .hero-wrapper {{
        text-align: center;
        margin-bottom: 3rem;
    }}
    
    .hero-badge {{
        display: inline-block;
        background: {COLORS['primary']};
        color: {COLORS['text-dark']};
        font-size: 0.7rem;
        font-weight: 600;
        padding: 0.25rem 1rem;
        border-radius: 30px;
        letter-spacing: 0.5px;
        margin-bottom: 1rem;
    }}
    
    .hero-icon {{
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .hero-title {{
        font-size: 2.8rem;
        font-weight: 800;
        color: {COLORS['text-dark']};
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }}
    
    .hero-subtitle {{
        font-size: 1rem;
        color: {COLORS['text-dark']};
        opacity: 0.7;
        max-width: 550px;
        margin: 0 auto;
    }}
    
    /* ========== FEATURE CARDS ========== */
    .features-grid {{
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin-bottom: 3rem;
        flex-wrap: wrap;
    }}
    
    .feature-card {{
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 200px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px {COLORS['shadow']};
        border: 1px solid rgba(236,185,20,0.1);
    }}
    
    .feature-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        border-color: {COLORS['primary']};
    }}
    
    .feature-icon {{
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }}
    
    .feature-title {{
        font-size: 1rem;
        font-weight: 700;
        color: {COLORS['text-dark']};
        margin-bottom: 0.25rem;
    }}
    
    .feature-desc {{
        font-size: 0.75rem;
        color: {COLORS['text-dark']};
        opacity: 0.6;
    }}
    
    /* ========== AUTH CARD ========== */
    .auth-wrapper {{
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }}
    
    .auth-card {{
        background: white;
        border-radius: 24px;
        padding: 2rem;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }}
    
    .auth-header {{
        text-align: center;
        margin-bottom: 1.5rem;
    }}
    
    .auth-icon {{
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }}
    
    .auth-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORS['text-dark']};
        margin-bottom: 0.25rem;
    }}
    
    .auth-subtitle {{
        font-size: 0.8rem;
        color: {COLORS['text-dark']};
        opacity: 0.6;
    }}
    
    /* ========== FORM STYLES ========== */
    .form-group {{
        margin-bottom: 1rem;
    }}
    
    .form-label {{
        display: block;
        font-size: 0.75rem;
        font-weight: 600;
        color: {COLORS['text-dark']};
        margin-bottom: 0.25rem;
        letter-spacing: 0.3px;
    }}
    
    /* Streamlit Input Override */
    .stTextInput > div > div > input {{
        width: 100%;
        padding: 12px 16px;
        font-size: 0.9rem;
        font-family: 'Poppins', sans-serif;
        border: 1.5px solid {COLORS['border']};
        border-radius: 14px;
        background: white;
        transition: all 0.2s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        outline: none;
        box-shadow: 0 0 0 3px rgba(236,185,20,0.15);
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #BDBDBD;
        font-size: 0.85rem;
    }}
    
    /* Password field same as text field */
    .stTextInput > div > div > input[type="password"] {{
        padding: 12px 16px;
    }}
    
    /* ========== BUTTONS ========== */
    .stButton > button {{
        width: 100%;
        padding: 12px 20px;
        font-size: 0.9rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        border: none;
        border-radius: 40px;
        background: {COLORS['primary']};
        color: {COLORS['text-dark']};
        cursor: pointer;
        transition: all 0.2s ease;
        margin-bottom: 0.75rem;
    }}
    
    .stButton > button:hover {{
        background: {COLORS['primary-dark']};
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(236,185,20,0.3);
    }}
    
    .stButton > button:active {{
        transform: translateY(0);
    }}
    
    /* Secondary Button Style */
    .stButton > button[kind="secondary"] {{
        background: transparent;
        border: 2px solid {COLORS['primary']};
        color: {COLORS['text-dark']};
    }}
    
    .stButton > button[kind="secondary"]:hover {{
        background: {COLORS['primary']};
        color: {COLORS['text-dark']};
    }}
    
    /* ========== DIVIDER ========== */
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
    }}
    
    .divider::before,
    .divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid {COLORS['border']};
    }}
    
    .divider span {{
        padding: 0 1rem;
        font-size: 0.7rem;
        color: {COLORS['text-dark']};
        opacity: 0.5;
    }}
    
    /* ========== MESSAGES ========== */
    .success-message {{
        background: {COLORS['success-light']};
        color: {COLORS['success']};
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-bottom: 1rem;
        border-left: 3px solid {COLORS['success']};
    }}
    
    .error-message {{
        background: {COLORS['error-light']};
        color: {COLORS['error']};
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-bottom: 1rem;
        border-left: 3px solid {COLORS['error']};
    }}
    
    /* ========== FOOTER ========== */
    .footer {{
        text-align: center;
        padding-top: 2rem;
        margin-top: 2rem;
        border-top: 1px solid rgba(79,61,53,0.1);
    }}
    
    .footer-text {{
        font-size: 0.7rem;
        color: {COLORS['text-dark']};
        opacity: 0.5;
    }}
    
    /* ========== LOGOUT BUTTON ========== */
    .logout-fixed {{
        position: fixed;
        top: 15px;
        right: 20px;
        z-index: 1000;
    }}
    
    /* ========== MAIN APP STYLES ========== */
    .welcome-card {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }}
    
    .welcome-title {{
        font-size: 1.3rem;
        font-weight: 700;
        color: {COLORS['text-dark']};
        margin-bottom: 0.25rem;
    }}
    
    .stats-grid {{
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .stat-card {{
        background: white;
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        flex: 1;
        box-shadow: 0 2px 8px {COLORS['shadow']};
    }}
    
    .stat-number {{
        font-size: 1.5rem;
        font-weight: 800;
        color: {COLORS['primary']};
    }}
    
    .stat-label {{
        font-size: 0.7rem;
        color: {COLORS['text-dark']};
        opacity: 0.6;
    }}
    
    .result-card {{
        background: white;
        border-radius: 16px;
        padding: 1.2rem;
        border-left: 4px solid {COLORS['primary']};
        box-shadow: 0 2px 8px {COLORS['shadow']};
    }}
    
    .section-title {{
        font-size: 1.1rem;
        font-weight: 600;
        color: {COLORS['text-dark']};
        margin-bottom: 1rem;
    }}
    
    hr {{
        margin: 1rem 0;
        border: none;
        height: 1px;
        background: {COLORS['border']};
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
                  email TEXT UNIQUE NOT NULL,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(email, username, password):
    import re
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return False, "Invalid email format"
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return False, "Username must be 3-20 characters"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ? OR username = ?", (email, username))
    if c.fetchone():
        conn.close()
        return False, "Email or username already exists"
    
    hashed_pw = hash_password(password)
    c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
              (email, username, hashed_pw))
    conn.commit()
    conn.close()
    return True, "Registration successful!"

def login_user(username_or_email, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, username, email, password FROM users WHERE email = ? OR username = ?",
              (username_or_email, username_or_email))
    user = c.fetchone()
    conn.close()
    if user and verify_password(password, user[3]):
        return True, {"id": user[0], "username": user[1], "email": user[2]}
    return False, "Invalid credentials"

def reset_password(email, new_password):
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters"
    hashed_pw = hash_password(new_password)
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_pw, email))
    conn.commit()
    conn.close()
    return True, "Password reset successful"

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
if 'reset_tokens' not in st.session_state:
    st.session_state.reset_tokens = {}
if 'reset_step' not in st.session_state:
    st.session_state.reset_step = 'request'
if 'reset_email' not in st.session_state:
    st.session_state.reset_email = None
if 'show_reset_code' not in st.session_state:
    st.session_state.show_reset_code = False
if 'generated_code' not in st.session_state:
    st.session_state.generated_code = None

# ============================================
# RESET FUNCTIONS
# ============================================

def generate_reset_token(email):
    token = ''.join(random.choices(string.digits, k=6))
    st.session_state.reset_tokens[email] = {'token': token, 'expires': time.time() + 3600}
    return token

def verify_reset_token(email, token):
    if email in st.session_state.reset_tokens:
        data = st.session_state.reset_tokens[email]
        if data['token'] == token and time.time() < data['expires']:
            return True
    return False

def clear_reset_token(email):
    if email in st.session_state.reset_tokens:
        del st.session_state.reset_tokens[email]

# ============================================
# OCR FUNCTIONS
# ============================================

from ocr_app import load_ocr_model, predict_text

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
    <div class="hero-wrapper">
        <div class="hero-badge">✨ AI-POWERED OCR</div>
        <div class="hero-icon">📝</div>
        <div class="hero-title">Sinhala Handwritten OCR</div>
        <div class="hero-subtitle">Convert handwritten Sinhala documents to digital text with advanced AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    st.markdown("""
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
            <div class="feature-desc">85%+ recognition rate</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
            <div class="feature-desc">Results in seconds</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure</div>
            <div class="feature-desc">Your data is private</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Card
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-icon">🔐</div>
        <div class="auth-title">Welcome Back</div>
        <div class="auth-subtitle">Sign in to continue</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email_or_username = st.text_input("", placeholder="Email or Username", key="login_input")
        password = st.text_input("", type="password", placeholder="Password", key="password_input")
        
        if st.form_submit_button("Sign In", use_container_width=True):
            if email_or_username and password:
                success, result = login_user(email_or_username, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = result['username']
                    st.session_state.email = result['email']
                    st.session_state.page = 'main'
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-message">❌ {result}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider"><span>or</span></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account", key="signup_btn", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()
    with col2:
        if st.button("Forgot Password?", key="forgot_btn", use_container_width=True):
            st.session_state.page = 'forgot_password'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-badge">✨ GET STARTED</div>
        <div class="hero-icon">📝</div>
        <div class="hero-title">Create Account</div>
        <div class="hero-subtitle">Join us and start using Sinhala OCR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-icon">✏️</div>
        <div class="auth-title">Sign Up</div>
        <div class="auth-subtitle">Create your free account</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form"):
        email = st.text_input("", placeholder="Email Address", key="signup_email")
        username = st.text_input("", placeholder="Username", key="signup_username")
        password = st.text_input("", type="password", placeholder="Password", key="signup_password")
        confirm = st.text_input("", type="password", placeholder="Confirm Password", key="signup_confirm")
        
        if st.form_submit_button("Create Account", use_container_width=True):
            if not email or not username or not password:
                st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
            elif password != confirm:
                st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
            elif len(password) < 6:
                st.markdown('<div class="error-message">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
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
                        st.markdown(f'<div class="success-message">✅ {msg}. Please login.</div>', unsafe_allow_html=True)
                        st.session_state.page = 'login'
                        st.rerun()
                else:
                    st.markdown(f'<div class="error-message">❌ {msg}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("← Back to Login", use_container_width=True, key="back_btn"):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-wrapper">
        <div class="hero-badge">🔐 ACCOUNT RECOVERY</div>
        <div class="hero-icon">🔑</div>
        <div class="hero-title">Reset Password</div>
        <div class="hero-subtitle">We'll help you regain access</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.reset_step == 'request':
        st.markdown("""
        <div class="auth-header">
            <div class="auth-icon">📧</div>
            <div class="auth-title">Forgot Password?</div>
            <div class="auth-subtitle">Enter your email to reset</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("reset_request"):
            email = st.text_input("", placeholder="Email Address", key="reset_email")
            
            if st.form_submit_button("Send Reset Code", use_container_width=True):
                if email:
                    if email_exists(email):
                        token = generate_reset_token(email)
                        st.session_state.reset_email = email
                        st.session_state.generated_code = token
                        st.session_state.show_reset_code = True
                        st.session_state.reset_step = 'verify'
                        st.markdown(f'<div class="success-message">✅ Reset Code: <strong>{token}</strong><br>Use this code to reset your password.</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-message">❌ Email not found</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Please enter your email</div>', unsafe_allow_html=True)
    
    elif st.session_state.reset_step == 'verify':
        st.markdown(f"""
        <div class="auth-header">
            <div class="auth-icon">🔐</div>
            <div class="auth-title">Reset Password</div>
            <div class="auth-subtitle">Email: {st.session_state.reset_email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("reset_verify"):
            code = st.text_input("", placeholder="6-Digit Code", key="reset_code")
            new_password = st.text_input("", type="password", placeholder="New Password", key="new_pass")
            confirm = st.text_input("", type="password", placeholder="Confirm Password", key="confirm_pass")
            
            if st.form_submit_button("Reset Password", use_container_width=True):
                if code and new_password and confirm:
                    if new_password != confirm:
                        st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
                    elif len(new_password) < 6:
                        st.markdown('<div class="error-message">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
                    else:
                        if verify_reset_token(st.session_state.reset_email, code):
                            success, msg = reset_password(st.session_state.reset_email, new_password)
                            if success:
                                clear_reset_token(st.session_state.reset_email)
                                st.markdown(f'<div class="success-message">✅ {msg}</div>', unsafe_allow_html=True)
                                st.session_state.reset_step = 'request'
                                st.session_state.reset_email = None
                                st.session_state.show_reset_code = False
                                st.session_state.generated_code = None
                                time.sleep(1)
                                st.session_state.page = 'login'
                                st.rerun()
                            else:
                                st.markdown(f'<div class="error-message">❌ {msg}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error-message">❌ Invalid or expired code</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("← Back to Login", use_container_width=True, key="reset_back"):
        st.session_state.reset_step = 'request'
        st.session_state.reset_email = None
        st.session_state.show_reset_code = False
        st.session_state.generated_code = None
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN OCR APP
# ============================================

def main_app():
    # Logout button - Working with proper placement
    st.markdown(f'''
    <div class="logout-fixed">
        <button onclick="window.location.href='?logout=true'" style="background: {COLORS['primary']}; color: {COLORS['text-dark']}; border: none; border-radius: 40px; padding: 8px 20px; font-size: 0.8rem; font-weight: 600; cursor: pointer; font-family: 'Poppins', sans-serif;">
            🚪 Logout
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown(f"""
    <div class="welcome-card">
        <div class="welcome-title">👋 Welcome back, {st.session_state.username}!</div>
        <p style="font-size: 0.85rem; opacity: 0.8;">Ready to convert your handwritten Sinhala documents to digital text?</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-card"><div class="stat-number">85%+</div><div class="stat-label">Accuracy</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-card"><div class="stat-number">771</div><div class="stat-label">Samples</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-card"><div class="stat-number">104</div><div class="stat-label">Characters</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load Model
    with st.spinner("Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load OCR model")
        return
    
    # Main Content
    col_upload, col_result = st.columns(2)
    
    with col_upload:
        st.markdown('<div class="section-title">📤 Upload Document</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True)
            
            if st.button("🔍 Recognize Text", use_container_width=True):
                with st.spinner("Processing..."):
                    text, error = predict_text(image, processor, model, device)
                    if text:
                        st.session_state.predicted_text = text
                        st.session_state.prediction_time = datetime.now()
                        st.markdown('<div class="success-message">✅ Recognition complete!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error-message">❌ {error}</div>', unsafe_allow_html=True)
    
    with col_result:
        st.markdown('<div class="section-title">📝 Result</div>', unsafe_allow_html=True)
        
        if st.session_state.predicted_text:
            st.markdown(f'''
            <div class="result-card">
                <strong>Recognized Text:</strong><br><br>
                {st.session_state.predicted_text}
            </div>
            ''', unsafe_allow_html=True)
            st.caption(f"Recognized at: {st.session_state.prediction_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button("💾 Download TXT", data=txt_data, file_name="ocr_result.txt", use_container_width=True)
        else:
            st.markdown(f'''
            <div class="result-card">
                <strong>No Result Yet</strong><br><br>
                <span style="color: #888;">Upload an image and click "Recognize Text"</span>
            </div>
            ''', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

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
