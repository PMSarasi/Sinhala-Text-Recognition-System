# ============================================
# SINHALA HANDWRITTEN OCR
# Clean Professional Design - Fully Working
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
BG_LIGHT = "#CBB8A0"
TEXT_DARK = "#4F3D35"
WHITE = "#FFFFFF"
ERROR = "#E53935"
SUCCESS = "#43A047"

# ============================================
# CSS
# ============================================

st.markdown(f"""
<style>
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Main background */
    .stApp {{
        background: linear-gradient(135deg, {BG_LIGHT} 0%, #E0D5C8 100%);
    }}
    
    /* Container */
    .main-container {{
        max-width: 1100px;
        margin: 0 auto;
        padding: 2rem;
    }}
    
    /* Headers */
    .main-title {{
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
    }}
    
    .main-subtitle {{
        text-align: center;
        font-size: 1rem;
        color: {TEXT_DARK};
        opacity: 0.7;
        margin-bottom: 2rem;
    }}
    
    /* Feature cards */
    .feature-grid {{
        display: flex;
        gap: 1.5rem;
        justify-content: center;
        margin-bottom: 2.5rem;
    }}
    
    .feature-item {{
        background: {WHITE};
        border-radius: 16px;
        padding: 1.2rem;
        text-align: center;
        flex: 1;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    
    .feature-icon {{
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }}
    
    .feature-title {{
        font-weight: 600;
        color: {TEXT_DARK};
        margin-bottom: 0.25rem;
    }}
    
    .feature-desc {{
        font-size: 0.75rem;
        color: {TEXT_DARK};
        opacity: 0.6;
    }}
    
    /* Auth card */
    .auth-card {{
        background: {WHITE};
        border-radius: 20px;
        padding: 2rem;
        max-width: 400px;
        margin: 0 auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }}
    
    .auth-title {{
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        color: {TEXT_DARK};
        margin-bottom: 1.5rem;
    }}
    
    /* Buttons */
    .stButton > button {{
        width: 100%;
        background: {PRIMARY};
        color: {TEXT_DARK};
        font-weight: 600;
        border: none;
        border-radius: 40px;
        padding: 0.6rem;
        transition: all 0.2s;
    }}
    
    .stButton > button:hover {{
        background: {PRIMARY_DARK};
        transform: translateY(-1px);
    }}
    
    /* Inputs */
    .stTextInput > div > div > input {{
        border-radius: 12px;
        border: 1px solid #ddd;
        padding: 10px 14px;
    }}
    
    /* Divider */
    .divider {{
        text-align: center;
        margin: 1.2rem 0;
        color: #aaa;
        font-size: 0.8rem;
    }}
    
    /* Messages */
    .success-msg {{
        background: #e8f5e9;
        color: #2e7d32;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-size: 0.85rem;
    }}
    
    .error-msg {{
        background: #ffebee;
        color: #c62828;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 1rem;
        font-size: 0.85rem;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid rgba(79,61,53,0.1);
        font-size: 0.7rem;
        color: {TEXT_DARK};
        opacity: 0.5;
    }}
    
    /* Logout button */
    .logout-btn {{
        position: fixed;
        top: 15px;
        right: 20px;
        background: {PRIMARY};
        color: {TEXT_DARK};
        border: none;
        border-radius: 30px;
        padding: 8px 18px;
        font-size: 0.8rem;
        font-weight: 600;
        cursor: pointer;
        z-index: 1000;
    }}
    
    .logout-btn:hover {{
        background: {PRIMARY_DARK};
    }}
    
    /* Welcome banner */
    .welcome-box {{
        background: linear-gradient(135deg, {PRIMARY}, {SECONDARY});
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
    }}
    
    .stats-row {{
        display: flex;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .stat-box {{
        background: {WHITE};
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        flex: 1;
    }}
    
    .stat-number {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {PRIMARY};
    }}
    
    .result-box {{
        background: {WHITE};
        border-radius: 12px;
        padding: 1rem;
        border-left: 3px solid {PRIMARY};
    }}
    
    hr {{
        margin: 1rem 0;
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

def reset_user_password(email, new_password):
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
# RESET
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
    
    st.markdown(f'<div class="main-title">📝 Sinhala Handwritten OCR</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="main-subtitle">Convert handwritten Sinhala documents to digital text with AI</div>', unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-item">
            <div class="feature-icon">🎯</div>
            <div class="feature-title">85%+ Accuracy</div>
            <div class="feature-desc">High recognition rate</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Fast</div>
            <div class="feature-desc">Results in seconds</div>
        </div>
        <div class="feature-item">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">Secure</div>
            <div class="feature-desc">Your data is private</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login form
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="auth-title">Welcome Back</div>', unsafe_allow_html=True)
    
    with st.form("login"):
        email_or_user = st.text_input("", placeholder="Email or Username")
        password = st.text_input("", type="password", placeholder="Password")
        
        if st.form_submit_button("Sign In"):
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
                st.markdown('<div class="error-msg">❌ Please fill all fields</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="divider">or</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Account", use_container_width=True):
            st.session_state.page = 'signup'
            st.rerun()
    with col2:
        if st.button("Forgot Password", use_container_width=True):
            st.session_state.page = 'forgot_password'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f'<div class="main-title">📝 Create Account</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="main-subtitle">Join us and start using Sinhala OCR</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="auth-title">Sign Up</div>', unsafe_allow_html=True)
    
    with st.form("signup"):
        email = st.text_input("", placeholder="Email Address")
        username = st.text_input("", placeholder="Username")
        password = st.text_input("", type="password", placeholder="Password (min 6 characters)")
        confirm = st.text_input("", type="password", placeholder="Confirm Password")
        
        if st.form_submit_button("Create Account"):
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
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown(f'<div class="main-title">🔐 Reset Password</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="main-subtitle">We\'ll help you get back into your account</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    
    if st.session_state.reset_step == 'request':
        st.markdown(f'<div class="auth-title">Forgot Password?</div>', unsafe_allow_html=True)
        
        with st.form("reset_request"):
            email = st.text_input("", placeholder="Email Address")
            
            if st.form_submit_button("Send Reset Code"):
                if email:
                    if email_exists(email):
                        token = generate_token(email)
                        st.session_state.reset_email = email
                        st.session_state.reset_step = 'verify'
                        st.markdown(f'<div class="success-msg">✅ Your reset code: <strong>{token}</strong><br>Use this code to reset your password.</div>', unsafe_allow_html=True)
                        st.rerun()
                    else:
                        st.markdown('<div class="error-msg">❌ Email not found</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="error-msg">❌ Please enter your email</div>', unsafe_allow_html=True)
    
    elif st.session_state.reset_step == 'verify':
        st.markdown(f'<div class="auth-title">Reset Password</div>', unsafe_allow_html=True)
        st.markdown(f'<p style="text-align:center; font-size:0.8rem;">Email: {st.session_state.reset_email}</p>', unsafe_allow_html=True)
        
        with st.form("reset_verify"):
            code = st.text_input("", placeholder="6-Digit Code")
            new_password = st.text_input("", type="password", placeholder="New Password (min 6)")
            confirm = st.text_input("", type="password", placeholder="Confirm Password")
            
            if st.form_submit_button("Reset Password"):
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
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN APP
# ============================================

def main_app():
    # Logout button
    st.markdown(f'<button onclick="window.location.href=\'?logout=true\'" class="logout-btn">🚪 Logout</button>', unsafe_allow_html=True)
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome
    st.markdown(f"""
    <div class="welcome-box">
        <strong style="font-size: 1.2rem;">👋 Welcome, {st.session_state.username}!</strong>
        <p style="margin-top: 5px; font-size: 0.85rem;">Upload a handwritten Sinhala image to get digital text</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("""
    <div class="stats-row">
        <div class="stat-box"><div class="stat-number">85%+</div><div>Accuracy</div></div>
        <div class="stat-box"><div class="stat-number">771</div><div>Samples</div></div>
        <div class="stat-box"><div class="stat-number">104</div><div>Characters</div></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load model
    with st.spinner("Loading OCR model..."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("Failed to load model")
        return
    
    # Two columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Upload")
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
                        st.success("✅ Done!")
                    else:
                        st.error(f"Error: {error}")
    
    with col2:
        st.markdown("### 📝 Result")
        
        if st.session_state.predicted_text:
            st.markdown(f"""
            <div class="result-box">
                <strong>Recognized Text:</strong><br><br>
                {st.session_state.predicted_text}
            </div>
            """, unsafe_allow_html=True)
            st.caption(f"Time: {st.session_state.prediction_time.strftime('%H:%M:%S')}")
            
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button("💾 Download", data=txt_data, file_name="result.txt", use_container_width=True)
        else:
            st.info("Upload an image and click Recognize")
    
    st.markdown('<div class="footer">© 2026 Sinhala Handwritten OCR | Powered by TrOCR</div>', unsafe_allow_html=True)
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
