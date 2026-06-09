# ============================================
# SINHALA HANDWRITTEN OCR
# Modern Glass Design - Professional UI
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
# MODERN COLOR SCHEME
# ============================================

COLORS = {
    "primary": "#4361EE",      # Modern blue
    "primary-dark": "#3A56D4",
    "secondary": "#7209B7",    # Purple accent
    "bg-gradient-start": "#667eea",
    "bg-gradient-end": "#764ba2",
    "white": "#FFFFFF",
    "text-dark": "#1A1A2E",
    "text-light": "#666666",
    "border": "#E0E0E0",
    "error": "#F56565",
    "success": "#48BB78",
    "card-bg": "rgba(255, 255, 255, 0.95)",
}

# ============================================
# CUSTOM CSS - Modern Glass Design
# ============================================

st.markdown(f"""
<style>
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main Background - Gradient like reference */
    .stApp {{
        background: linear-gradient(135deg, {COLORS['bg-gradient-start']} 0%, {COLORS['bg-gradient-end']} 100%);
        min-height: 100vh;
    }}
    
    /* Main Container */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }}
    
    /* ========== GLASS CARD ========== */
    .glass-card {{
        background: {COLORS['card-bg']};
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.3);
    }}
    
    /* ========== HEADER SECTION ========== */
    .header-section {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .logo-icon {{
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }}
    
    .main-title {{
        font-size: 2.2rem;
        font-weight: 700;
        color: {COLORS['white']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    
    .main-subtitle {{
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
    }}
    
    /* ========== FEATURE CARDS ========== */
    .features-row {{
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }}
    
    .feature-card {{
        background: {COLORS['card-bg']};
        border-radius: 16px;
        padding: 1rem 1.5rem;
        text-align: center;
        flex: 1;
        min-width: 150px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.2);
    }}
    
    .feature-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }}
    
    .feature-title {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {COLORS['text-dark']};
    }}
    
    /* ========== AUTH CARD ========== */
    .auth-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 500px;
    }}
    
    .auth-card {{
        background: {COLORS['card-bg']};
        border-radius: 28px;
        padding: 2rem;
        width: 100%;
        max-width: 440px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);
        border: 1px solid rgba(255,255,255,0.3);
    }}
    
    .auth-header {{
        text-align: center;
        margin-bottom: 1.8rem;
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
        color: {COLORS['text-light']};
    }}
    
    /* ========== FORM STYLES ========== */
    .form-group {{
        margin-bottom: 1rem;
    }}
    
    .input-label {{
        display: block;
        font-size: 0.75rem;
        font-weight: 600;
        color: {COLORS['text-dark']};
        margin-bottom: 0.3rem;
    }}
    
    /* Streamlit Input Override - Rounded like reference */
    .stTextInput > div > div > input {{
        width: 100%;
        padding: 12px 16px;
        font-size: 0.9rem;
        font-family: 'Inter', sans-serif;
        border: 1px solid {COLORS['border']};
        border-radius: 12px;
        background: white;
        transition: all 0.2s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {COLORS['primary']};
        outline: none;
        box-shadow: 0 0 0 3px rgba(67,97,238,0.1);
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: #B0B0B0;
        font-size: 0.85rem;
    }}
    
    /* Checkbox styling */
    .checkbox-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
    }}
    
    .remember-text {{
        font-size: 0.8rem;
        color: {COLORS['text-light']};
    }}
    
    .forgot-link {{
        font-size: 0.8rem;
        color: {COLORS['primary']};
        text-decoration: none;
        cursor: pointer;
    }}
    
    .forgot-link:hover {{
        text-decoration: underline;
    }}
    
    /* ========== BUTTONS ========== */
    .stButton > button {{
        width: 100%;
        padding: 12px 20px;
        font-size: 0.9rem;
        font-weight: 600;
        border: none;
        border-radius: 40px;
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        cursor: pointer;
        transition: all 0.2s ease;
        margin-top: 0.5rem;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(67,97,238,0.3);
    }}
    
    /* Secondary Button */
    .secondary-btn > button {{
        background: transparent;
        border: 2px solid {COLORS['primary']};
        color: {COLORS['primary']};
    }}
    
    .secondary-btn > button:hover {{
        background: {COLORS['primary']};
        color: white;
    }}
    
    /* ========== DIVIDER ========== */
    .divider {{
        text-align: center;
        margin: 1.5rem 0;
        position: relative;
    }}
    
    .divider::before {{
        content: "";
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 1px;
        background: {COLORS['border']};
    }}
    
    .divider span {{
        background: {COLORS['card-bg']};
        padding: 0 1rem;
        position: relative;
        font-size: 0.75rem;
        color: {COLORS['text-light']};
    }}
    
    /* ========== MESSAGES ========== */
    .success-message {{
        background: #C6F6D5;
        color: #276749;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }}
    
    .error-message {{
        background: #FED7D7;
        color: #C53030;
        padding: 10px 14px;
        border-radius: 12px;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }}
    
    /* ========== FOOTER ========== */
    .footer {{
        text-align: center;
        padding: 2rem 0 1rem;
        color: rgba(255,255,255,0.6);
        font-size: 0.7rem;
    }}
    
    /* ========== LOGOUT BUTTON ========== */
    .logout-btn {{
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(8px);
        color: white;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 40px;
        padding: 8px 20px;
        font-size: 0.8rem;
        font-weight: 500;
        cursor: pointer;
        z-index: 1000;
        transition: all 0.2s;
    }}
    
    .logout-btn:hover {{
        background: rgba(255,255,255,0.3);
    }}
    
    /* ========== DASHBOARD STYLES ========== */
    .welcome-card {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        color: white;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .stat-card {{
        background: {COLORS['card-bg']};
        border-radius: 16px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(8px);
    }}
    
    .stat-number {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {COLORS['primary']};
    }}
    
    .result-card {{
        background: {COLORS['card-bg']};
        border-radius: 16px;
        padding: 1rem;
        border-left: 3px solid {COLORS['primary']};
    }}
    
    .section-title {{
        font-size: 1rem;
        font-weight: 600;
        color: {COLORS['text-dark']};
        margin-bottom: 0.8rem;
    }}
    
    hr {{
        margin: 1rem 0;
        border: none;
        height: 1px;
        background: rgba(255,255,255,0.2);
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
    import re
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
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
    return False, "Invalid email/username or password"

def reset_user_password(email, new_password):
    if len(new_password) < 6:
        return False, "Password must be at least 6 characters"
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hash_pw(new_password), email))
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

# ============================================
# RESET FUNCTIONS
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
# LOGIN PAGE (Styled like reference)
# ============================================

def login_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="header-section">
        <div class="logo-icon">📝</div>
        <div class="main-title">Sinhala Handwritten OCR</div>
        <div class="main-subtitle">Convert handwritten Sinhala documents to digital text with AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Row
    st.markdown("""
    <div class="features-row">
        <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Card
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-icon">👋</div>
        <div class="auth-title">Login please</div>
        <div class="auth-subtitle">Enter your details to continue</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email_username = st.text_input("", placeholder="Input your user ID or Email", key="login_input")
        password = st.text_input("", type="password", placeholder="Input your password", key="login_password")
        
        # Remember me & Forgot Password row
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Remember me", key="remember")
        with col2:
            st.markdown(f'<div style="text-align: right;"><a class="forgot-link" href="?forgot=true">Forgot Password?</a></div>', unsafe_allow_html=True)
        
        if st.form_submit_button("LOG IN"):
            if email_username and password:
                success, result = login_user(email_username, password)
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
    
    # Signup button
    st.markdown(f'''
    <div style="text-align: center;">
        <p style="font-size: 0.8rem; color: {COLORS['text-light']};">Don't have an account?</p>
    </div>
    ''', unsafe_allow_html=True)
    
    if st.button("SIGNUP", key="signup_btn", use_container_width=True):
        st.session_state.page = 'signup'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE (Same Style)
# ============================================

def signup_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-section">
        <div class="logo-icon">📝</div>
        <div class="main-title">Sinhala Handwritten OCR</div>
        <div class="main-subtitle">Join us and start using Sinhala OCR technology</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="auth-header">
        <div class="auth-icon">✨</div>
        <div class="auth-title">Welcome!</div>
        <div class="auth-subtitle">Enter your details and start journey with us</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("signup_form"):
        email = st.text_input("", placeholder="Email Address", key="signup_email")
        username = st.text_input("", placeholder="Username", key="signup_username")
        password = st.text_input("", type="password", placeholder="Password (min 6 characters)", key="signup_password")
        confirm = st.text_input("", type="password", placeholder="Confirm Password", key="signup_confirm")
        
        if st.form_submit_button("SIGNUP"):
            if not email or not username or not password:
                st.markdown('<div class="error-message">❌ Please fill all fields</div>', unsafe_allow_html=True)
            elif password != confirm:
                st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
            else:
                success, msg = register_user(email, username, password)
                if success:
                    # Auto login after signup
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
    if st.button("← Back to Login", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE (Same Style)
# ============================================

def forgot_password_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header-section">
        <div class="logo-icon">🔐</div>
        <div class="main-title">Reset Password</div>
        <div class="main-subtitle">We'll help you get back into your account</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
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
            
            if st.form_submit_button("Send Reset Code"):
                if email:
                    if email_exists(email):
                        token = generate_token(email)
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
            <div class="auth-subtitle">Email: {st.session_state.reset_email}</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("reset_verify"):
            code = st.text_input("", placeholder="6-Digit Code", key="reset_code")
            new_password = st.text_input("", type="password", placeholder="New Password (min 6)", key="reset_new")
            confirm = st.text_input("", type="password", placeholder="Confirm Password", key="reset_confirm")
            
            if st.form_submit_button("Reset Password"):
                if code and new_password and confirm:
                    if new_password != confirm:
                        st.markdown('<div class="error-message">❌ Passwords do not match</div>', unsafe_allow_html=True)
                    elif len(new_password) < 6:
                        st.markdown('<div class="error-message">❌ Password must be at least 6 characters</div>', unsafe_allow_html=True)
                    else:
                        if verify_token(st.session_state.reset_email, code):
                            success, msg = reset_user_password(st.session_state.reset_email, new_password)
                            if success:
                                clear_token(st.session_state.reset_email)
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
    if st.button("← Back to Login", use_container_width=True):
        st.session_state.reset_step = 'request'
        st.session_state.reset_email = None
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN DASHBOARD (Same Style)
# ============================================

def main_app():
    # Logout button
    st.markdown(f'<button onclick="window.location.href=\'?logout=true\'" class="logout-btn">🚪 Logout</button>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown(f"""
    <div class="welcome-card">
        <h2 style="font-size: 1.3rem; margin-bottom: 0.25rem;">👋 Welcome back, {st.session_state.username}!</h2>
        <p style="font-size: 0.85rem; opacity: 0.9;">Upload a handwritten Sinhala image to get digital text</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card"><div class="stat-number">85%+</div><div style="font-size: 0.7rem;">Accuracy</div></div>
        <div class="stat-card"><div class="stat-number">771</div><div style="font-size: 0.7rem;">Samples</div></div>
        <div class="stat-card"><div class="stat-number">104</div><div style="font-size: 0.7rem;">Characters</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load OCR Model
    with st.spinner("Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load OCR model")
        return
    
    # Main Content
    col1, col2 = st.columns(2)
    
    with col1:
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
    
    with col2:
        st.markdown('<div class="section-title">📝 Result</div>', unsafe_allow_html=True)
        
        if st.session_state.predicted_text:
            st.markdown(f"""
            <div class="result-card">
                <strong>Recognized Text:</strong><br><br>
                {st.session_state.predicted_text}
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Time: {st.session_state.prediction_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button("💾 Download TXT", data=txt_data, file_name="ocr_result.txt", use_container_width=True)
        else:
            st.markdown("""
            <div class="result-card">
                <strong>No Result Yet</strong><br><br>
                <span style="color: #888;">Upload an image and click "Recognize Text"</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ROUTING
# ============================================

# Handle forgot password link
if 'forgot' in st.query_params:
    st.session_state.page = 'forgot_password'
    st.rerun()

# Handle logout
if 'logout' in st.query_params:
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
