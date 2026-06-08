# ============================================
# SINHALA HANDWRITTEN OCR WEB APP
# Modern Glass Design - Honey Opal Sunset Theme
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

COLORS = {
    "primary": "#ECB914",
    "primary-light": "#F6D579",
    "primary-dark": "#9D8108",
    "bg-light": "#CBB8A0",
    "text-dark": "#4F3D35",
    "text-light": "#FFFFFF",
    "error": "#FF6B6B",
    "success": "#51CF66",
    "glass-bg": "rgba(255, 255, 255, 0.92)",
    "glass-border": "rgba(236, 185, 20, 0.3)",
}

# ============================================
# GLASS-MORPHISM CSS
# ============================================

st.markdown(f"""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Main container */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg-light']} 0%, #e8d5c0 100%);
        min-height: 100vh;
    }}
    
    .block-container {{
        padding: 1rem 3rem 2rem 3rem;
        max-width: 1300px;
        margin: 0 auto;
    }}
    
    /* ========== GLASS CARD STYLES ========== */
    .glass-card {{
        background: {COLORS['glass-bg']};
        backdrop-filter: blur(10px);
        border-radius: 32px;
        padding: 2rem;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        border: 1px solid {COLORS['glass-border']};
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 35px 60px -15px rgba(0,0,0,0.3);
    }}
    
    /* ========== HERO SECTION ========== */
    .hero-section {{
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease;
    }}
    
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-30px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    .hero-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['primary-dark']});
        color: {COLORS['text-dark']};
        padding: 0.25rem 1rem;
        border-radius: 50px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }}
    
    .hero-icon {{
        font-size: 4rem;
        margin-bottom: 0.5rem;
        animation: pulse 2s infinite;
    }}
    
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); }}
        50% {{ transform: scale(1.05); }}
    }}
    
    .hero-title {{
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {COLORS['text-dark']} 0%, {COLORS['primary-dark']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }}
    
    .hero-subtitle {{
        font-size: 1.1rem;
        color: {COLORS['text-dark']};
        opacity: 0.7;
        max-width: 600px;
        margin: 0 auto;
    }}
    
    /* ========== FEATURE CARDS ========== */
    .feature-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 3rem 0;
    }}
    
    .feature-card-glass {{
        background: {COLORS['glass-bg']};
        backdrop-filter: blur(8px);
        border-radius: 24px;
        padding: 1.8rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 1px solid {COLORS['glass-border']};
        cursor: pointer;
    }}
    
    .feature-card-glass:hover {{
        transform: translateY(-8px);
        background: rgba(255,255,255,0.96);
        border-color: {COLORS['primary']};
    }}
    
    .feature-icon-glass {{
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['primary-light']});
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        margin: 0 auto 1.2rem auto;
    }}
    
    .feature-title-glass {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {COLORS['text-dark']};
        margin-bottom: 0.5rem;
    }}
    
    .feature-desc-glass {{
        font-size: 0.85rem;
        color: {COLORS['text-dark']};
        opacity: 0.7;
        line-height: 1.4;
    }}
    
    /* ========== AUTH CARD ========== */
    .auth-card-glass {{
        background: {COLORS['glass-bg']};
        backdrop-filter: blur(12px);
        border-radius: 32px;
        padding: 2.5rem;
        max-width: 450px;
        margin: 0 auto;
        border: 1px solid {COLORS['glass-border']};
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
    }}
    
    .auth-header {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .auth-icon {{
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }}
    
    .auth-title {{
        font-size: 1.8rem;
        font-weight: 700;
        color: {COLORS['text-dark']};
        margin-bottom: 0.25rem;
    }}
    
    .auth-subtitle {{
        font-size: 0.85rem;
        color: {COLORS['text-dark']};
        opacity: 0.6;
    }}
    
    /* ========== INPUT FIELDS ========== */
    .input-group {{
        margin-bottom: 1.2rem;
    }}
    
    .input-label {{
        display: block;
        font-size: 0.8rem;
        font-weight: 500;
        color: {COLORS['text-dark']};
        margin-bottom: 0.4rem;
    }}
    
    .stTextInput > div > div > input {{
        border-radius: 16px;
        border: 1.5px solid #e0e0e0;
        padding: 12px 16px;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background: white;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        box-shadow: 0 0 0 4px rgba(236,185,20,0.15);
    }}
    
    /* ========== BUTTONS ========== */
    .btn-primary-glass {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary-dark']} 100%);
        color: {COLORS['text-dark']};
        border: none;
        border-radius: 50px;
        padding: 0.8rem 1.8rem;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
        margin-bottom: 1rem;
    }}
    
    .btn-primary-glass:hover {{
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(157,129,8,0.3);
        background: linear-gradient(135deg, {COLORS['primary-dark']} 0%, {COLORS['primary']} 100%);
    }}
    
    .btn-secondary-glass {{
        background: transparent;
        color: {COLORS['text-dark']};
        border: 2px solid {COLORS['primary']};
        border-radius: 50px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: all 0.3s ease;
    }}
    
    .btn-secondary-glass:hover {{
        background: {COLORS['primary']};
        color: {COLORS['text-dark']};
        transform: translateY(-2px);
    }}
    
    .btn-link {{
        background: transparent;
        border: none;
        color: {COLORS['primary-dark']};
        cursor: pointer;
        font-size: 0.85rem;
        font-weight: 500;
        text-decoration: underline;
        width: 100%;
        transition: all 0.3s ease;
    }}
    
    .btn-link:hover {{
        color: {COLORS['primary']};
    }}
    
    /* ========== DIVIDER ========== */
    .divider-glass {{
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
    }}
    
    .divider-glass::before,
    .divider-glass::after {{
        content: "";
        position: absolute;
        top: 50%;
        width: 42%;
        height: 1px;
        background: linear-gradient(90deg, transparent, {COLORS['primary']}, transparent);
    }}
    
    .divider-glass::before {{ left: 0; }}
    .divider-glass::after {{ right: 0; }}
    
    .divider-glass span {{
        background: {COLORS['glass-bg']};
        padding: 0 12px;
        color: {COLORS['text-dark']};
        opacity: 0.5;
        font-size: 0.8rem;
    }}
    
    /* ========== MESSAGES ========== */
    .success-message {{
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        color: #2e7d32;
        padding: 12px 16px;
        border-radius: 16px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        border-left: 4px solid #4caf50;
    }}
    
    .error-message {{
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        color: #c62828;
        padding: 12px 16px;
        border-radius: 16px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
        border-left: 4px solid #f44336;
    }}
    
    /* ========== FOOTER ========== */
    .footer-glass {{
        text-align: center;
        padding: 2rem 0 1rem 0;
        margin-top: 3rem;
        border-top: 1px solid rgba(79,61,53,0.1);
    }}
    
    .footer-text {{
        color: {COLORS['text-dark']};
        opacity: 0.5;
        font-size: 0.8rem;
    }}
    
    /* ========== LOGOUT BUTTON ========== */
    .logout-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, {COLORS['primary']}, {COLORS['primary-light']});
        color: {COLORS['text-dark']};
        border: none;
        border-radius: 50px;
        padding: 10px 24px;
        font-size: 0.85rem;
        font-weight: 600;
        cursor: pointer;
        z-index: 1000;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        backdrop-filter: blur(4px);
    }}
    
    .logout-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(157,129,8,0.3);
        background: linear-gradient(135deg, {COLORS['primary-dark']}, {COLORS['primary']});
        color: white;
    }}
    
    /* ========== MAIN APP STYLES ========== */
    .welcome-glass {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['primary-light']} 100%);
        border-radius: 24px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}
    
    .stat-glass {{
        background: {COLORS['glass-bg']};
        backdrop-filter: blur(4px);
        border-radius: 20px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid {COLORS['glass-border']};
        transition: all 0.3s ease;
    }}
    
    .stat-glass:hover {{
        transform: translateY(-3px);
        background: white;
    }}
    
    .result-glass {{
        background: {COLORS['glass-bg']};
        backdrop-filter: blur(4px);
        border-radius: 20px;
        padding: 1.5rem;
        border-left: 4px solid {COLORS['primary']};
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
# AUTHENTICATION FUNCTIONS
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
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    import bcrypt
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register_user(email, username, password):
    import re
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
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
    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">✨ AI-Powered OCR</div>
        <div class="hero-icon">📝</div>
        <div class="hero-title">Sinhala Handwritten OCR</div>
        <div class="hero-subtitle">Transform handwritten Sinhala documents into digital text with advanced AI technology</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card-glass">
            <div class="feature-icon-glass">🎯</div>
            <div class="feature-title-glass">High Accuracy</div>
            <div class="feature-desc-glass">85%+ character recognition accuracy with continuous improvement</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="feature-card-glass">
            <div class="feature-icon-glass">⚡</div>
            <div class="feature-title-glass">Lightning Fast</div>
            <div class="feature-desc-glass">Results in seconds with optimized AI processing</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="feature-card-glass">
            <div class="feature-icon-glass">🔒</div>
            <div class="feature-title-glass">Secure & Private</div>
            <div class="feature-desc-glass">Your data stays confidential and never shared</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Login Card
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="auth-card-glass">', unsafe_allow_html=True)
        st.markdown("""
        <div class="auth-header">
            <div class="auth-icon">🔐</div>
            <div class="auth-title">Welcome Back</div>
            <div class="auth-subtitle">Sign in to your account</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            email_or_username = st.text_input("", placeholder="Email or Username", key="login_email")
            password = st.text_input("", type="password", placeholder="Password", key="login_password")
            
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
                        st.markdown(f'<div class="error-message">❌ {result}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="divider-glass"><span>or</span></div>', unsafe_allow_html=True)
        
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Create Account", use_container_width=True, key="signup_btn"):
                st.session_state.page = 'signup'
                st.rerun()
        with col_b:
            if st.button("Forgot Password?", use_container_width=True, key="forgot_btn"):
                st.session_state.page = 'forgot_password'
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-glass">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">✨ Get Started</div>
        <div class="hero-icon">📝</div>
        <div class="hero-title">Create Account</div>
        <div class="hero-subtitle">Join us and start using Sinhala OCR technology</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="auth-card-glass">', unsafe_allow_html=True)
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
            
            if st.form_submit_button("Sign Up", use_container_width=True):
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
    
    st.markdown("""
    <div class="footer-glass">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown("""
    <div class="hero-section">
        <div class="hero-badge">🔐 Account Recovery</div>
        <div class="hero-icon">🔑</div>
        <div class="hero-title">Reset Password</div>
        <div class="hero-subtitle">We'll help you regain access to your account</div>
    </div>
    """, unsafe_allow_html=True)
    
    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown('<div class="auth-card-glass">', unsafe_allow_html=True)
        
        if st.session_state.reset_step == 'request':
            st.markdown("""
            <div class="auth-header">
                <div class="auth-icon">📧</div>
                <div class="auth-title">Forgot Password?</div>
                <div class="auth-subtitle">Enter your email to receive a reset code</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("reset_request"):
                email = st.text_input("", placeholder="Email Address", key="reset_email_input")
                
                if st.form_submit_button("Send Reset Code", use_container_width=True):
                    if email:
                        conn = sqlite3.connect('users.db')
                        c = conn.cursor()
                        c.execute("SELECT id FROM users WHERE email = ?", (email,))
                        user = c.fetchone()
                        conn.close()
                        
                        if user:
                            token = generate_reset_token(email)
                            st.session_state.reset_email = email
                            st.session_state.reset_step = 'verify'
                            st.markdown(f'<div class="success-message">✅ Reset code: <strong>{token}</strong><br>Please use this code to reset your password.</div>', unsafe_allow_html=True)
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
                <div class="auth-subtitle">Resetting for: {st.session_state.reset_email}</div>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("reset_verify"):
                code = st.text_input("", placeholder="6-Digit Reset Code", key="reset_code")
                new_password = st.text_input("", type="password", placeholder="New Password", key="reset_new")
                confirm = st.text_input("", type="password", placeholder="Confirm Password", key="reset_confirm")
                
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
            st.session_state.page = 'login'
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="footer-glass">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN OCR APP
# ============================================

def main_app():
    # Logout button
    st.markdown(f'''
    <button onclick="window.location.href='?logout=true'" class="logout-btn">
        🚪 Logout
    </button>
    ''', unsafe_allow_html=True)
    
    # Welcome Banner
    st.markdown(f'''
    <div class="welcome-glass">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin-bottom: 0.25rem;">👋 Welcome back, {st.session_state.username}!</h2>
        <p style="opacity: 0.8;">Ready to convert your handwritten Sinhala documents to digital text?</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Stats Section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="stat-glass"><div style="font-size: 2rem; font-weight: 800; color: {COLORS["primary"]};">85%+</div><div style="font-size: 0.8rem;">Accuracy</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="stat-glass"><div style="font-size: 2rem; font-weight: 800; color: {COLORS["primary"]};">771</div><div style="font-size: 0.8rem;">Training Samples</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="stat-glass"><div style="font-size: 2rem; font-weight: 800; color: {COLORS["primary"]};">104</div><div style="font-size: 0.8rem;">Characters</div></div>', unsafe_allow_html=True)
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Load OCR Model
    with st.spinner("Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load OCR model")
        return
    
    # Main Content
    col_upload, col_result = st.columns(2)
    
    with col_upload:
        st.markdown("### 📤 Upload Document")
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
        st.markdown("### 📝 Result")
        
        if st.session_state.predicted_text:
            st.markdown(f'''
            <div class="result-glass">
                <strong>Recognized Text:</strong><br><br>
                {st.session_state.predicted_text}
            </div>
            ''', unsafe_allow_html=True)
            st.caption(f"Recognized at: {st.session_state.prediction_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button("💾 Download TXT", data=txt_data, file_name="ocr_result.txt", use_container_width=True)
        else:
            st.markdown(f'''
            <div class="result-glass">
                <strong>No Result Yet</strong><br><br>
                <span style="color: #888;">Upload an image and click "Recognize Text"</span>
            </div>
            ''', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class="footer-glass">
        <div class="footer-text">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>
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
