# SINHALA HANDWRITTEN OCR
# Premium Design - Warm Orange/Coral Theme
# Complete Production Code
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
# COLORS - Warm Orange/Coral Theme (From Reference Image)
# ============================================

PRIMARY = "#FF6B35"
PRIMARY_DARK = "#E85D2C"
PRIMARY_LIGHT = "#FF8A5C"
PRIMARY_ULTRA_LIGHT = "#FFF3EE"
SECONDARY = "#2D3436"
BG_WHITE = "#FFFFFF"
BG_SOFT = "#F8F9FA"
TEXT_DARK = "#1A1A2E"
TEXT_GRAY = "#6C6C6C"
TEXT_LIGHT = "#B0B0B0"
SUCCESS = "#00B894"
ERROR = "#FF4757"
BORDER = "#E8E8E8"
INPUT_BG = "#F8F8F8"

# ============================================
# COMPLETE CSS - Matching Reference Image Design
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
    
    /* Main background - Soft gradient */
    .stApp {{
        background: linear-gradient(135deg, #FFF5F0 0%, #FFFFFF 50%, #FFF8F3 100%) !important;
    }}
    
    /* ========== AUTH PAGES STYLES ========== */
    .auth-wrapper {{
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1.5rem;
    }}
    
    .auth-card {{
        max-width: 460px;
        width: 100%;
        background: {BG_WHITE};
        border-radius: 32px;
        padding: 40px 36px;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.08);
        border: 1px solid {BORDER};
        transition: all 0.3s ease;
    }}
    
    /* Logo Section */
    .logo-section {{
        text-align: center;
        margin-bottom: 32px;
    }}
    
    .logo-icon {{
        font-size: 52px;
        margin-bottom: 12px;
        display: inline-block;
    }}
    
    .logo-title {{
        font-size: 24px;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 6px;
        letter-spacing: -0.3px;
    }}
    
    .logo-subtitle {{
        font-size: 13px;
        color: {TEXT_GRAY};
        line-height: 1.4;
    }}
    
    /* Auth Header */
    .auth-header {{
        text-align: center;
        margin-bottom: 32px;
    }}
    
    .auth-title {{
        font-size: 28px;
        font-weight: 700;
        color: {TEXT_DARK};
        margin-bottom: 6px;
    }}
    
    .auth-subtitle {{
        font-size: 14px;
        color: {TEXT_GRAY};
    }}
    
    /* Form Groups */
    .form-group {{
        margin-bottom: 20px;
    }}
    
    .input-label {{
        display: block;
        font-size: 13px;
        font-weight: 600;
        color: {TEXT_DARK};
        margin-bottom: 8px;
    }}
    
    /* Custom Input with Icon Support */
    .stTextInput {{
        position: relative;
    }}
    
    .stTextInput > div {{
        margin-bottom: 0 !important;
    }}
    
    .stTextInput > div > div > input {{
        width: 100% !important;
        padding: 14px 16px 14px 44px !important;
        font-size: 14px !important;
        border: 1.5px solid {BORDER} !important;
        border-radius: 14px !important;
        background: {INPUT_BG} !important;
        color: {TEXT_DARK} !important;
        transition: all 0.2s ease !important;
        font-family: inherit !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1) !important;
        background: {BG_WHITE} !important;
        outline: none !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: {TEXT_LIGHT} !important;
        font-size: 13px;
    }}
    
    /* Add icons to inputs using pseudo-elements */
    [data-testid="stTextInput"] {{
        position: relative;
    }}
    
    /* Email icon */
    [data-testid="stTextInput"]:nth-of-type(1)::before {{
        content: "✉️";
        position: absolute;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 100;
        font-size: 16px;
        pointer-events: none;
    }}
    
    /* Password icon */
    [data-testid="stTextInput"]:nth-of-type(2)::before {{
        content: "🔒";
        position: absolute;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 100;
        font-size: 16px;
        pointer-events: none;
    }}
    
    /* Checkbox styling */
    .stCheckbox {{
        margin: 20px 0 24px 0;
    }}
    
    .stCheckbox label {{
        color: {TEXT_GRAY} !important;
        font-size: 13px !important;
        gap: 8px;
    }}
    
    .stCheckbox label span {{
        font-size: 13px !important;
    }}
    
    /* Primary Button */
    .stButton > button {{
        width: 100%;
        background: {PRIMARY} !important;
        color: white !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 14px !important;
        border: none !important;
        border-radius: 14px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
        margin-bottom: 0;
        letter-spacing: 0.5px;
    }}
    
    .stButton > button:hover {{
        background: {PRIMARY_DARK} !important;
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(255, 107, 53, 0.25);
    }}
    
    /* Link Buttons Row */
    .link-row {{
        display: flex;
        gap: 12px;
        margin-top: 16px;
    }}
    
    .link-row .stButton {{
        flex: 1;
    }}
    
    .link-row .stButton > button {{
        background: transparent !important;
        color: {TEXT_GRAY} !important;
        border: 1.5px solid {BORDER} !important;
        padding: 12px !important;
        font-size: 13px !important;
        box-shadow: none !important;
    }}
    
    .link-row .stButton > button:hover {{
        border-color: {PRIMARY} !important;
        color: {PRIMARY} !important;
        background: {PRIMARY_ULTRA_LIGHT} !important;
        transform: none !important;
        box-shadow: none !important;
    }}
    
    /* Divider */
    .divider {{
        display: flex;
        align-items: center;
        text-align: center;
        margin: 24px 0;
        color: {TEXT_LIGHT};
        font-size: 12px;
    }}
    
    .divider::before,
    .divider::after {{
        content: '';
        flex: 1;
        border-bottom: 1px solid {BORDER};
    }}
    
    .divider span {{
        margin: 0 12px;
    }}
    
    /* Footer */
    .auth-footer {{
        text-align: center;
        margin-top: 32px;
        padding-top: 24px;
        border-top: 1px solid {BORDER};
        color: {TEXT_LIGHT};
        font-size: 11px;
    }}
    
    /* Message styling */
    .success-msg {{
        background: #E8F8F5;
        border: 1px solid #A8E6CF;
        color: {SUCCESS};
        padding: 12px 16px;
        border-radius: 14px;
        margin-bottom: 20px;
        font-size: 13px;
    }}
    
    .error-msg {{
        background: #FEF2F2;
        border: 1px solid #FECACA;
        color: {ERROR};
        padding: 12px 16px;
        border-radius: 14px;
        margin-bottom: 20px;
        font-size: 13px;
    }}
    
    /* ========== MAIN APP STYLES ========== */
    .main-header {{
        background: {BG_WHITE};
        border-bottom: 1px solid {BORDER};
        padding: 16px 32px;
        position: sticky;
        top: 0;
        z-index: 100;
    }}
    
    .main-container {{
        padding: 32px;
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    .welcome-card {{
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%);
        border-radius: 24px;
        padding: 32px;
        color: white;
        margin-bottom: 32px;
    }}
    
    .welcome-title {{
        font-size: 28px;
        font-weight: 700;
        margin-bottom: 8px;
    }}
    
    .welcome-text {{
        font-size: 14px;
        opacity: 0.9;
    }}
    
    /* Stats Grid */
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 32px;
    }}
    
    .stat-card {{
        background: {BG_WHITE};
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 1px solid {BORDER};
        transition: all 0.2s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
    }}
    
    .stat-number {{
        font-size: 28px;
        font-weight: 700;
        color: {PRIMARY};
        margin-bottom: 6px;
    }}
    
    .stat-label {{
        font-size: 13px;
        color: {TEXT_GRAY};
    }}
    
    /* Glass Cards for Upload/Results */
    .glass-card {{
        background: {BG_WHITE};
        border-radius: 24px;
        padding: 28px;
        border: 1px solid {BORDER};
        height: 100%;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }}
    
    .card-title {{
        font-size: 20px;
        font-weight: 600;
        color: {TEXT_DARK};
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .upload-area {{
        border: 2px dashed {BORDER};
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        background: {INPUT_BG};
    }}
    
    .upload-area:hover {{
        border-color: {PRIMARY};
        background: {PRIMARY_ULTRA_LIGHT};
    }}
    
    .result-area {{
        background: {INPUT_BG};
        border-radius: 16px;
        padding: 20px;
        border-left: 4px solid {PRIMARY};
        min-height: 200px;
    }}
    
    .result-text {{
        font-size: 15px;
        line-height: 1.6;
        color: {TEXT_DARK};
        margin-top: 12px;
    }}
    
    .logout-btn {{
        background: transparent !important;
        color: {TEXT_GRAY} !important;
        border: 1.5px solid {BORDER} !important;
        padding: 8px 20px !important;
        border-radius: 12px !important;
        font-size: 13px !important;
    }}
    
    .logout-btn:hover {{
        border-color: {ERROR} !important;
        color: {ERROR} !important;
        background: transparent !important;
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .auth-card {{
            padding: 28px 20px;
        }}
        .auth-title {{
            font-size: 24px;
        }}
        .stats-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
        }}
        .main-container {{
            padding: 20px;
        }}
        .welcome-title {{
            font-size: 22px;
        }}
        .glass-card {{
            padding: 20px;
            margin-bottom: 20px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .stats-grid {{
            grid-template-columns: 1fr;
        }}
        .link-row {{
            flex-direction: column;
        }}
    }}
    
    /* Remove form backgrounds */
    div[data-testid="stForm"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    
    /* File uploader styling */
    .stFileUploader {{
        border: none !important;
        padding: 0 !important;
    }}
    
    .stFileUploader > div {{
        border: 2px dashed {BORDER} !important;
        border-radius: 16px !important;
        padding: 40px !important;
        background: {INPUT_BG} !important;
    }}
    
    .stFileUploader > div:hover {{
        border-color: {PRIMARY} !important;
        background: {PRIMARY_ULTRA_LIGHT} !important;
    }}
    
    /* Image styling */
    .stImage {{
        border-radius: 16px;
        overflow: hidden;
        margin-top: 20px;
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
                  password TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
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
# LOGIN PAGE - Exact Reference Design
# ============================================

def login_page():
    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="logo-section">
                <div class="logo-icon">📝</div>
                <div class="logo-title">Sinhala Handwritten OCR</div>
                <div class="logo-subtitle">Transform handwritten Sinhala into digital text</div>
            </div>
            
            <div class="auth-header">
                <div class="auth-title">Welcome Back!</div>
                <div class="auth-subtitle">Sign in to continue your journey</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Email/Username field with icon
    st.markdown('<div class="form-group"><label class="input-label">Email or Username</label></div>', unsafe_allow_html=True)
    email_or_user = st.text_input("", placeholder="Enter your email or username", key="login_email", label_visibility="collapsed")
    
    # Password field with icon
    st.markdown('<div class="form-group"><label class="input-label">Password</label></div>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Enter your password", key="login_pass", label_visibility="collapsed")
    
    # Remember me and Forgot Password row
    col1, col2 = st.columns(2)
    with col1:
        remember = st.checkbox("Remember me", key="remember_me")
    with col2:
        st.markdown(f'<div style="text-align: right; margin-top: 8px;"><a href="#" style="color: {PRIMARY}; text-decoration: none; font-size: 13px;" onclick="return false;">Forgot Password?</a></div>', unsafe_allow_html=True)
    
    # Sign In button
    if st.button("LOG IN →", key="signin_btn"):
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
    st.markdown('<div class="divider"><span>or</span></div>', unsafe_allow_html=True)
    
    # Sign Up button
    if st.button("CREATE NEW ACCOUNT", key="create_acc"):
        st.session_state.page = 'signup'
        st.rerun()
    
    # Footer
    st.markdown(f"""
            <div class="auth-footer">
                © 2025 Sinhala Handwritten OCR | Powered by TrOCR
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE - Matching Design
# ============================================

def signup_page():
    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="logo-section">
                <div class="logo-icon">📝</div>
                <div class="logo-title">Create Account</div>
                <div class="logo-subtitle">Join us and start your OCR journey</div>
            </div>
            
            <div class="auth-header">
                <div class="auth-title">Get Started!</div>
                <div class="auth-subtitle">Create your free account</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Email field
    st.markdown('<div class="form-group"><label class="input-label">Email Address</label></div>', unsafe_allow_html=True)
    email = st.text_input("", placeholder="Enter your email", key="signup_email", label_visibility="collapsed")
    
    # Username field
    st.markdown('<div class="form-group"><label class="input-label">Username</label></div>', unsafe_allow_html=True)
    username = st.text_input("", placeholder="Choose a username", key="signup_user", label_visibility="collapsed")
    
    # Password field
    st.markdown('<div class="form-group"><label class="input-label">Password</label></div>', unsafe_allow_html=True)
    password = st.text_input("", type="password", placeholder="Create a password (min 6 characters)", key="signup_pass", label_visibility="collapsed")
    
    # Confirm Password field
    st.markdown('<div class="form-group"><label class="input-label">Confirm Password</label></div>', unsafe_allow_html=True)
    confirm = st.text_input("", type="password", placeholder="Confirm your password", key="signup_confirm", label_visibility="collapsed")
    
    # Create Account button
    if st.button("SIGN UP →", key="create_btn"):
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
    
    # Divider
    st.markdown('<div class="divider"><span>already have an account?</span></div>', unsafe_allow_html=True)
    
    # Back to Login button
    if st.button("← BACK TO LOGIN", key="back_login"):
        st.session_state.page = 'login'
        st.rerun()
    
    # Footer
    st.markdown(f"""
            <div class="auth-footer">
                © 2025 Sinhala Handwritten OCR | Secure & Fast
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE - Matching Design
# ============================================

def forgot_password_page():
    st.markdown("""
    <div class="auth-wrapper">
        <div class="auth-card">
            <div class="logo-section">
                <div class="logo-icon">🔐</div>
                <div class="logo-title">Reset Password</div>
                <div class="logo-subtitle">We'll help you get back in</div>
            </div>
            
            <div class="auth-header">
                <div class="auth-title">Forgot Password?</div>
                <div class="auth-subtitle">Enter your email and create a new password</div>
            </div>
    """, unsafe_allow_html=True)
    
    # Email field
    st.markdown('<div class="form-group"><label class="input-label">Email Address</label></div>', unsafe_allow_html=True)
    email = st.text_input("", placeholder="Enter your registered email", key="reset_email", label_visibility="collapsed")
    
    # New Password field
    st.markdown('<div class="form-group"><label class="input-label">New Password</label></div>', unsafe_allow_html=True)
    new_password = st.text_input("", type="password", placeholder="Create new password (min 6 characters)", key="new_pass", label_visibility="collapsed")
    
    # Confirm Password field
    st.markdown('<div class="form-group"><label class="input-label">Confirm New Password</label></div>', unsafe_allow_html=True)
    confirm_password = st.text_input("", type="password", placeholder="Confirm your new password", key="confirm_pass", label_visibility="collapsed")
    
    # Reset button
    if st.button("RESET PASSWORD →", key="reset_btn"):
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
                st.markdown('<div class="error-msg">❌ Email not found in our system</div>', unsafe_allow_html=True)
    
    # Divider
    st.markdown('<div class="divider"><span>remember your password?</span></div>', unsafe_allow_html=True)
    
    # Back to Login button
    if st.button("← BACK TO LOGIN", key="back_login_reset"):
        st.session_state.page = 'login'
        st.rerun()
    
    # Footer
    st.markdown(f"""
            <div class="auth-footer">
                © 2025 Sinhala Handwritten OCR | Account Recovery
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN APP DASHBOARD - Matching Design
# ============================================

def main_app():
    # Header with logout
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown(f"""
        <div class="main-header" style="background: transparent; padding: 0 0 20px 0;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <span style="font-size: 28px;">📝</span>
                <span style="font-size: 20px; font-weight: 600; color: #1A1A2E;">Sinhala Handwritten OCR</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🚪 Logout", key="logout_btn", help="Logout from your account"):
            logout()
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Welcome Card
    st.markdown(f"""
    <div class="welcome-card">
        <div class="welcome-title">👋 Welcome back, {st.session_state.username}!</div>
        <div class="welcome-text">Ready to convert your handwritten Sinhala documents? Upload an image below to get started.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Grid
    st.markdown("""
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-number">85%+</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">771</div>
            <div class="stat-label">Training Samples</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">104</div>
            <div class="stat-label">Characters</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">⚡</div>
            <div class="stat-label">Real-time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load OCR Model
    try:
        from ocr_app import load_ocr_model, predict_text
        with st.spinner("🔄 Loading AI Model..."):
            processor, model, device = load_ocr_model()
        
        if processor is None:
            st.error("❌ Failed to load OCR model. Please check the model files.")
            return
    except ImportError:
        st.warning("⚠️ OCR module not found. Using demo mode.")
        processor, model, device = None, None, None
    
    # Two Column Layout for Upload and Results
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">
                <span>📤</span> Upload Image
            </div>
        """, unsafe_allow_html=True)
        
        uploaded = st.file_uploader(
            "Choose an image",
            type=['png', 'jpg', 'jpeg'],
            label_visibility="collapsed"
        )
        
        if uploaded:
            image = Image.open(uploaded)
            st.image(image, use_container_width=True, caption="Your uploaded image")
            
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
            <div class="upload-area">
                <div style="font-size: 48px; margin-bottom: 12px;">📸</div>
                <p style="color: #6C6C6C; margin-bottom: 4px;">Drag & drop or click to upload</p>
                <p style="font-size: 12px; color: #B0B0B0;">Supports PNG, JPG, JPEG</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <div class="card-title">
                <span>📝</span> Recognized Text
            </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.predicted_text:
            st.markdown(f"""
            <div class="result-area">
                <strong style="color: #FF6B35;">Output:</strong>
                <div class="result-text">
                    {st.session_state.predicted_text}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.prediction_time:
                st.caption(f"🕐 Processed at: {st.session_state.prediction_time.strftime('%I:%M:%S %p')}")
            
            # Download button
            txt_data = io.BytesIO(st.session_state.predicted_text.encode('utf-8'))
            st.download_button(
                "💾 Download as Text",
                data=txt_data,
                file_name="recognized_text.txt",
                use_container_width=True
            )
        else:
            st.markdown("""
            <div class="upload-area" style="border: none; background: #F8F8F8;">
                <div style="font-size: 48px; margin-bottom: 12px;">📄</div>
                <p style="color: #6C6C6C;">Upload an image and click<br>"Recognize Text" to see results</p>
                <p style="font-size: 12px; color: #B0B0B0;">Results will appear here</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown(f"""
    <div class="auth-footer" style="margin-top: 32px;">
        © 2025 Sinhala Handwritten OCR | Powered by TrOCR • Deep Learning • AI Innovation
    </div>
    """, unsafe_allow_html=True)
    
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
