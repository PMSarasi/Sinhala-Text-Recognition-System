# ============================================
# SINHALA HANDWRITTEN OCR
# Professional Complete Website - Final Version
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
# PROFESSIONAL COLOR SCHEME
# ============================================

COLORS = {
    "primary": "#4F46E5",      # Indigo
    "primary-dark": "#4338CA",
    "secondary": "#06B6D4",    # Cyan
    "success": "#10B981",      # Emerald
    "error": "#EF4444",        # Red
    "warning": "#F59E0B",      # Amber
    "dark": "#1F2937",         # Gray-800
    "light": "#F9FAFB",        # Gray-50
    "white": "#FFFFFF",
    "border": "#E5E7EB",
}

# ============================================
# CSS
# ============================================

st.markdown(f"""
<style>
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main Container */
    .main-container {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem;
    }}
    
    /* Header */
    .header {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .header-icon {{
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }}
    
    .header-title {{
        font-size: 2rem;
        font-weight: 700;
        color: {COLORS['dark']};
        margin-bottom: 0.25rem;
    }}
    
    .header-subtitle {{
        font-size: 0.9rem;
        color: {COLORS['dark']};
        opacity: 0.6;
    }}
    
    /* Feature Cards */
    .features {{
        display: flex;
        gap: 1rem;
        justify-content: center;
        margin-bottom: 2rem;
    }}
    
    .feature {{
        background: {COLORS['white']};
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        flex: 1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    .feature-icon {{
        font-size: 1.5rem;
        margin-bottom: 0.25rem;
    }}
    
    .feature-title {{
        font-size: 0.8rem;
        font-weight: 600;
        color: {COLORS['dark']};
    }}
    
    /* Auth Card */
    .auth-card {{
        background: {COLORS['white']};
        border-radius: 16px;
        padding: 2rem;
        max-width: 400px;
        margin: 0 auto;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
    }}
    
    .auth-title {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {COLORS['dark']};
        text-align: center;
        margin-bottom: 0.25rem;
    }}
    
    .auth-subtitle {{
        font-size: 0.8rem;
        color: {COLORS['dark']};
        opacity: 0.6;
        text-align: center;
        margin-bottom: 1.5rem;
    }}
    
    /* Form Elements */
    .stTextInput > div > div > input {{
        border-radius: 8px;
        border: 1px solid {COLORS['border']};
        padding: 8px 12px;
        font-size: 0.9rem;
    }}
    
    .stButton > button {{
        width: 100%;
        background: {COLORS['primary']};
        color: white;
        font-weight: 500;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        transition: all 0.2s;
    }}
    
    .stButton > button:hover {{
        background: {COLORS['primary-dark']};
    }}
    
    /* Links */
    .link {{
        color: {COLORS['primary']};
        text-decoration: none;
        font-size: 0.8rem;
        cursor: pointer;
    }}
    
    .link:hover {{
        text-decoration: underline;
    }}
    
    /* Divider */
    .divider {{
        text-align: center;
        margin: 1rem 0;
        color: {COLORS['dark']};
        opacity: 0.4;
        font-size: 0.7rem;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid {COLORS['border']};
        font-size: 0.7rem;
        color: {COLORS['dark']};
        opacity: 0.5;
    }}
    
    /* Dashboard */
    .welcome {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        color: white;
    }}
    
    .stats {{
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .stat {{
        background: {COLORS['white']};
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        flex: 1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    .stat-number {{
        font-size: 1.2rem;
        font-weight: 700;
        color: {COLORS['primary']};
    }}
    
    .result {{
        background: {COLORS['white']};
        border-radius: 12px;
        padding: 1rem;
        border-left: 3px solid {COLORS['primary']};
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    .section-title {{
        font-size: 0.9rem;
        font-weight: 600;
        color: {COLORS['dark']};
        margin-bottom: 0.5rem;
    }}
    
    /* Messages */
    .success {{
        background: #D1FAE5;
        color: #065F46;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }}
    
    .error {{
        background: #FEE2E2;
        color: #991B1B;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }}
    
    /* Logout Button */
    .logout {{
        position: fixed;
        top: 15px;
        right: 20px;
        background: {COLORS['white']};
        color: {COLORS['dark']};
        border: 1px solid {COLORS['border']};
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 0.8rem;
        cursor: pointer;
        z-index: 1000;
    }}
    
    .logout:hover {{
        background: {COLORS['light']};
    }}
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE
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
        return False, "Invalid email"
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return False, "Username 3-20 characters"
    if len(password) < 6:
        return False, "Password min 6 characters"
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ? OR username = ?", (email, username))
    if c.fetchone():
        conn.close()
        return False, "Email or username exists"
    
    c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
              (email, username, hash_pw(password)))
    conn.commit()
    conn.close()
    return True, "Registration successful"

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

def reset_password(email, new_password):
    if len(new_password) < 6:
        return False, "Password min 6 characters"
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
# SESSION
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
# OCR
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
    
    # Header
    st.markdown("""
    <div class="header">
        <div class="header-icon">📝</div>
        <div class="header-title">Sinhala Handwritten OCR</div>
        <div class="header-subtitle">Convert handwritten Sinhala documents to digital text with AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div class="features">
        <div class="feature">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">High Accuracy</div>
        </div>
        <div class="feature">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast Processing</div>
        </div>
        <div class="feature">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login Form
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Login please</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Enter your details to continue</div>', unsafe_allow_html=True)
    
    with st.form("login"):
        email_user = st.text_input("", placeholder="Input your user ID or Email")
        password = st.text_input("", type="password", placeholder="Input your password")
        
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("Remember me", key="remember")
        with col2:
            st.markdown(f'<div style="text-align: right;"><a class="link" href="?forgot=true">Forgot Password?</a></div>', unsafe_allow_html=True)
        
        if st.form_submit_button("LOG IN"):
            if email_user and password:
                success, result = login_user(email_user, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.username = result['username']
                    st.session_state.email = result['email']
                    st.session_state.page = 'main'
                    st.rerun()
                else:
                    st.markdown(f'<div class="error">{result}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error">Please fill all fields</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
    
    if st.button("SIGNUP", use_container_width=True):
        st.session_state.page = 'signup'
        st.rerun()
    
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
    <div class="header">
        <div class="header-icon">📝</div>
        <div class="header-title">Create Account</div>
        <div class="header-subtitle">Join us and start using Sinhala OCR</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown('<div class="auth-title">Sign Up</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Enter your details to create account</div>', unsafe_allow_html=True)
    
    with st.form("signup"):
        email = st.text_input("", placeholder="Email Address")
        username = st.text_input("", placeholder="Username")
        password = st.text_input("", type="password", placeholder="Password (min 6)")
        confirm = st.text_input("", type="password", placeholder="Confirm Password")
        
        if st.form_submit_button("SIGNUP"):
            if not email or not username or not password:
                st.markdown('<div class="error">Please fill all fields</div>', unsafe_allow_html=True)
            elif password != confirm:
                st.markdown('<div class="error">Passwords do not match</div>', unsafe_allow_html=True)
            else:
                success, msg = register_user(email, username, password)
                if success:
                    login_success, result = login_user(username, password)
                    if login_success:
                        st.session_state.logged_in = True
                        st.session_state.username = result['username']
                        st.session_state.email = result['email']
                        st.session_state.page = 'main'
                        st.rerun()
                    else:
                        st.markdown(f'<div class="success">{msg}. Please login.</div>', unsafe_allow_html=True)
                        st.session_state.page = 'login'
                        st.rerun()
                else:
                    st.markdown(f'<div class="error">{msg}</div>', unsafe_allow_html=True)
    
    if st.button("← Back to Login", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="header">
        <div class="header-icon">🔐</div>
        <div class="header-title">Reset Password</div>
        <div class="header-subtitle">We'll help you get back into your account</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.reset_step == 'request':
        st.markdown('<div class="auth-title">Forgot Password?</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-subtitle">Enter your email to receive reset code</div>', unsafe_allow_html=True)
        
        with st.form("reset_req"):
            email = st.text_input("", placeholder="Email Address")
            
            if st.form_submit_button("Send Reset Code"):
                if email:
                    if email_exists(email):
                        token = generate_token(email)
                        st.session_state.reset_email = email
                        st.session_state.reset_step = 'verify'
                        st.markdown(f'<div class="success">✅ Reset code: <strong>{token}</strong></div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="error">Email not found</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error">Please enter email</div>', unsafe_allow_html=True)
    
    elif st.session_state.reset_step == 'verify':
        st.markdown(f'<div class="auth-title">Reset Password</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="auth-subtitle">Email: {st.session_state.reset_email}</div>', unsafe_allow_html=True)
        
        with st.form("reset_verify"):
            code = st.text_input("", placeholder="6-Digit Code")
            new_password = st.text_input("", type="password", placeholder="New Password (min 6)")
            confirm = st.text_input("", type="password", placeholder="Confirm Password")
            
            if st.form_submit_button("Reset Password"):
                if code and new_password and confirm:
                    if new_password != confirm:
                        st.markdown('<div class="error">Passwords do not match</div>', unsafe_allow_html=True)
                    elif len(new_password) < 6:
                        st.markdown('<div class="error">Password min 6 characters</div>', unsafe_allow_html=True)
                    else:
                        if verify_token(st.session_state.reset_email, code):
                            success, msg = reset_password(st.session_state.reset_email, new_password)
                            if success:
                                clear_token(st.session_state.reset_email)
                                st.markdown(f'<div class="success">{msg}</div>', unsafe_allow_html=True)
                                st.session_state.reset_step = 'request'
                                st.session_state.reset_email = None
                                time.sleep(1)
                                st.session_state.page = 'login'
                                st.rerun()
                            else:
                                st.markdown(f'<div class="error">{msg}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown('<div class="error">Invalid or expired code</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error">Please fill all fields</div>', unsafe_allow_html=True)
    
    if st.button("← Back to Login", use_container_width=True):
        st.session_state.reset_step = 'request'
        st.session_state.reset_email = None
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN DASHBOARD
# ============================================

def main_app():
    # Logout button
    st.markdown(f'<button onclick="window.location.href=\'?logout=true\'" class="logout">🚪 Logout</button>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome
    st.markdown(f"""
    <div class="welcome">
        <h2 style="font-size: 1.2rem;">👋 Welcome, {st.session_state.username}!</h2>
        <p style="font-size: 0.8rem;">Upload a handwritten Sinhala image to get digital text</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
    <div class="stats">
        <div class="stat"><div class="stat-number">85%+</div><div>Accuracy</div></div>
        <div class="stat"><div class="stat-number">771</div><div>Samples</div></div>
        <div class="stat"><div class="stat-number">104</div><div>Characters</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load Model
    with st.spinner("Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load OCR model")
        return
    
    # Main
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
                        st.markdown('<div class="success">✅ Recognition complete!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="error">❌ {error}</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-title">📝 Result</div>', unsafe_allow_html=True)
        
        if st.session_state.predicted_text:
            st.markdown(f"""
            <div class="result">
                <strong>Recognized Text:</strong><br><br>
                {st.session_state.predicted_text}
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Time: {st.session_state.prediction_time.strftime('%H:%M:%S')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button("💾 Download TXT", data=txt_data, file_name="ocr_result.txt", use_container_width=True)
        else:
            st.markdown("""
            <div class="result">
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

if 'forgot' in st.query_params:
    st.session_state.page = 'forgot_password'
    st.rerun()

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
