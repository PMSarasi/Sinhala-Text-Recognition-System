# SINHALA HANDWRITTEN OCR
# Beautiful Responsive Design - PC & Mobile Optimized
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
# COLORS - Modern & Fresh
# ============================================

PRIMARY = "#6366F1"
PRIMARY_DARK = "#4F46E5"
PRIMARY_LIGHT = "#818CF8"
SECONDARY = "#10B981"
BG_WHITE = "#FFFFFF"
BG_SOFT = "#F9FAFB"
TEXT_DARK = "#111827"
TEXT_GRAY = "#6B7280"
TEXT_LIGHT = "#9CA3AF"
SUCCESS = "#10B981"
ERROR = "#EF4444"
BORDER = "#E5E7EB"

# ============================================
# CSS - Beautiful & Responsive
# ============================================

st.markdown(f"""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {{visibility: hidden !important;}}
    footer {{visibility: hidden !important;}}
    header {{visibility: hidden !important;}}
    
    /* Remove default padding */
    .main .block-container {{
        padding: 0 !important;
        max-width: 100% !important;
    }}
    
    /* Main background */
    .stApp {{
        background: linear-gradient(135deg, {BG_SOFT} 0%, {BG_WHITE} 100%) !important;
    }}
    
    /* Container */
    .login-container {{
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.5rem;
    }}
    
    /* Card - Perfect proportions */
    .login-card {{
        max-width: 420px;
        width: 100%;
        margin: 0 auto;
        background: {BG_WHITE};
        border-radius: 32px;
        padding: 2rem;
        box-shadow: 0 20px 35px -10px rgba(0, 0, 0, 0.08);
        border: 1px solid {BORDER};
        transition: all 0.3s ease;
    }}
    
    /* Header section */
    .logo-section {{
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .logo-icon {{
        font-size: 3rem;
        margin-bottom: 0.75rem;
        display: inline-block;
    }}
    
    .logo-title {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
    }}
    
    .logo-subtitle {{
        font-size: 0.875rem;
        color: {TEXT_GRAY};
        line-height: 1.4;
    }}
    
    /* Auth header */
    .auth-header {{
        text-align: center;
        margin-bottom: 1.75rem;
    }}
    
    .auth-title {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {TEXT_DARK};
        margin-bottom: 0.25rem;
    }}
    
    .auth-subtitle {{
        font-size: 0.875rem;
        color: {TEXT_GRAY};
    }}
    
    /* Input wrapper - Perfect spacing */
    .input-wrapper {{
        margin-bottom: 1.25rem;
    }}
    
    .input-label {{
        display: block;
        font-size: 0.875rem;
        font-weight: 500;
        color: {TEXT_DARK};
        margin-bottom: 0.5rem;
    }}
    
    /* Custom input styling */
    .stTextInput > div {{
        margin-bottom: 0 !important;
    }}
    
    .stTextInput > div > div > input {{
        width: 100% !important;
        padding: 12px 16px !important;
        font-size: 0.95rem !important;
        border: 1.5px solid {BORDER} !important;
        border-radius: 16px !important;
        background: {BG_WHITE} !important;
        color: {TEXT_DARK} !important;
        transition: all 0.2s ease !important;
        box-sizing: border-box !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
        outline: none !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {TEXT_LIGHT} !important;
        font-size: 0.9rem;
    }}
    
    /* Checkbox styling */
    .stCheckbox {{
        margin: 1rem 0 1.25rem 0;
    }}
    
    .stCheckbox label {{
        color: {TEXT_GRAY} !important;
        font-size: 0.875rem !important;
        gap: 0.5rem;
    }}
    
    /* Button styling */
    .stButton > button {{
        width: 100%;
        background: {PRIMARY} !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 12px !important;
        border: none !important;
        border-radius: 16px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin-bottom: 0.5rem;
    }}
    
    .stButton > button:hover {{
        background: {PRIMARY_DARK} !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }}
    
    /* Link buttons */
    .link-buttons {{
        display: flex;
        gap: 0.75rem;
        margin-top: 0.5rem;
    }}
    
    .link-buttons .stButton {{
        flex: 1;
    }}
    
    .link-buttons .stButton > button {{
        background: transparent !important;
        color: {TEXT_GRAY} !important;
        border: 1.5px solid {BORDER} !important;
        padding: 10px !important;
        font-size: 0.875rem !important;
        box-shadow: none !important;
    }}
    
    .link-buttons .stButton > button:hover {{
        border-color: {PRIMARY} !important;
        color: {PRIMARY} !important;
        background: transparent !important;
        transform: none !important;
    }}
    
    /* Divider */
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.25rem 0;
        color: {TEXT_LIGHT};
        font-size: 0.75rem;
    }}
    
    .divider::before,
    .divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid {BORDER};
    }}
    
    .divider span {{
        margin: 0 0.75rem;
    }}
    
    /* Footer */
    .footer {{
        text-align: center;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid {BORDER};
        color: {TEXT_LIGHT};
        font-size: 0.7rem;
    }}
    
    /* Message styling */
    .success-msg {{
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        color: {SUCCESS};
        padding: 12px;
        border-radius: 16px;
        margin-bottom: 1rem;
        font-size: 0.875rem;
    }}
    
    .error-msg {{
        background: #FEF2F2;
        border: 1px solid #FECACA;
        color: {ERROR};
        padding: 12px;
        border-radius: 16px;
        margin-bottom: 1rem;
        font-size: 0.875rem;
    }}
    
    /* Responsive - Mobile */
    @media (max-width: 640px) {{
        .login-card {{
            padding: 1.5rem;
        }}
        .logo-title {{
            font-size: 1.25rem;
        }}
        .auth-title {{
            font-size: 1.25rem;
        }}
        .link-buttons {{
            flex-direction: column;
            gap: 0.5rem;
        }}
    }}
    
    /* Remove all form backgrounds */
    div[data-testid="stForm"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
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
# LOGIN PAGE - Beautiful & Responsive
# ============================================

def login_page():
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <div class="logo-section">
                <div class="logo-icon">📝</div>
                <div class="logo-title">Sinhala Handwritten OCR</div>
                <div class="logo-subtitle">Transform handwritten Sinhala into digital text</div>
            </div>
            
            <div class="auth-header">
                <div class="auth-title">Welcome Back</div>
                <div class="auth-subtitle">Sign in to continue your journey</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Email/Username
    st.markdown('<div class="input-wrapper"><label class="input-label">Email or Username</label></div>', unsafe_allow_html=True)
    email_or_user = st.text_input("", placeholder="Enter your email or username", key="login_email", label_visibility="collapsed")
    
    # Password
    st.markdown('<div class="input-wrapper"><label class="input-label">Password</label></div>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Enter your password", key="login_pass", label_visibility="collapsed")
    
    # Remember me
    remember = st.checkbox("Remember me", key="remember_me")
    
    # Sign In button
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
    
    # Link buttons
    st.markdown('<div class="link-buttons">', unsafe_allow_html=True)
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
    
    # Footer
    st.markdown(f"""
            <div class="footer">
                © 2025 Sinhala Handwritten OCR | Powered by TrOCR
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE
# ============================================

def signup_page():
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <div class="logo-section">
                <div class="logo-icon">📝</div>
                <div class="logo-title">Create Account</div>
                <div class="logo-subtitle">Join us and start your OCR journey</div>
            </div>
            
            <div class="auth-header">
                <div class="auth-title">Get Started</div>
                <div class="auth-subtitle">Create your free account</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Email
    st.markdown('<div class="input-wrapper"><label class="input-label">Email Address</label></div>', unsafe_allow_html=True)
    email = st.text_input("", placeholder="Enter your email", key="signup_email", label_visibility="collapsed")
    
    # Username
    st.markdown('<div class="input-wrapper"><label class="input-label">Username</label></div>', unsafe_allow_html=True)
    username = st.text_input("", placeholder="Choose a username", key="signup_user", label_visibility="collapsed")
    
    # Password
    st.markdown('<div class="input-wrapper"><label class="input-label">Password</label></div>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Create a password (min 6 characters)", key="signup_pass", label_visibility="collapsed")
    
    # Confirm Password
    st.markdown('<div class="input-wrapper"><label class="input-label">Confirm Password</label></div>', unsafe_allow_html=True)
    confirm = st.text_input("", type="password", placeholder="Confirm your password", key="signup_confirm", label_visibility="collapsed")
    
    # Create button
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
    
    # Back to login
    if st.button("← Back to Login", key="back_login", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown("""
    <div class="login-container">
        <div class="login-card">
            <div class="logo-section">
                <div class="logo-icon">🔐</div>
                <div class="logo-title">Reset Password</div>
                <div class="logo-subtitle">We'll help you get back in</div>
            </div>
            
            <div class="auth-header">
                <div class="auth-title">Create New Password</div>
                <div class="auth-subtitle">Enter your email and new password</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Email
    st.markdown('<div class="input-wrapper"><label class="input-label">Email Address</label></div>', unsafe_allow_html=True)
    email = st.text_input("", placeholder="Enter your registered email", key="reset_email", label_visibility="collapsed")
    
    # New Password
    st.markdown('<div class="input-wrapper"><label class="input-label">New Password</label></div>', unsafe_allow_html=True)
    new_password = st.text_input("", type="password", placeholder="Create new password (min 6 characters)", key="new_pass", label_visibility="collapsed")
    
    # Confirm Password
    st.markdown('<div class="input-wrapper"><label class="input-label">Confirm New Password</label></div>', unsafe_allow_html=True)
    confirm_password = st.text_input("", type="password", placeholder="Confirm your new password", key="confirm_pass", label_visibility="collapsed")
    
    # Reset button
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
                    st.markdown(f'<div class="success-msg">✅ {msg}</div>', unsafe_allow_html=True)
                    time.sleep(1.5)
                    st.session_state.page = 'login'
                    st.rerun()
                else:
                    st.markdown(f'<div class="error-msg">❌ {msg}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="error-msg">❌ Email not found</div>', unsafe_allow_html=True)
    
    # Back to login
    if st.button("← Back to Login", key="back_login_reset", use_container_width=True):
        st.session_state.page = 'login'
        st.rerun()
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN APP - Keep existing functionality
# ============================================

def main_app():
    # Simple header with logout
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"<h2 style='color: #111827;'>👋 Welcome, {st.session_state.username}!</h2>", unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", key="logout_btn"):
            logout()
    
    st.markdown("---")
    
    # Two columns for OCR functionality
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📤 Upload Image")
        uploaded = st.file_uploader("", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True)
            
            # Load OCR model (simplified for demo)
            if st.button("🔍 Recognize Text", use_container_width=True):
                st.info("OCR processing would happen here")
                st.session_state.predicted_text = "Sample recognized Sinhala text would appear here"
    
    with col2:
        st.markdown("### 📝 Recognized Text")
        if st.session_state.get('predicted_text'):
            st.success(st.session_state.predicted_text)
        else:
            st.info("Upload an image and click Recognize Text to see results")

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
