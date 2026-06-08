# ============================================
# SINHALA HANDWRITTEN OCR WEB APP
# Professional UI with seamless authentication
# ============================================

import streamlit as st
from PIL import Image
import io
from datetime import datetime
import os
import time

# Import modules
from auth import register_user, login_user, generate_reset_code, verify_reset_code, reset_password
from ocr_app import load_ocr_model, predict_text

# Page configuration
st.set_page_config(
    page_title="Sinhala Handwritten OCR",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS FOR PROFESSIONAL LOOK
# ============================================

st.markdown("""
<style>
    /* Main container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card style for forms */
    .auth-card {
        background: white;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        max-width: 450px;
        margin: 0 auto;
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Header styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    
    /* Result box */
    .result-box {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 1rem;
        border-left: 5px solid #667eea;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        transition: transform 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(102,126,234,0.4);
    }
    
    /* Logout button */
    .logout-btn {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        border: none;
        border-radius: 30px;
        padding: 8px 20px;
        cursor: pointer;
        font-weight: 600;
        transition: transform 0.2s;
    }
    
    .logout-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(238,90,36,0.4);
    }
    
    /* Success message */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid #28a745;
    }
    
    /* Error message */
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid #dc3545;
    }
    
    /* Info message */
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-left: 4px solid #17a2b8;
    }
    
    /* Upload area */
    .upload-area {
        border: 2px dashed #667eea;
        border-radius: 15px;
        padding: 30px;
        text-align: center;
        background: #fafafa;
    }
    
    /* Welcome banner */
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'email' not in st.session_state:
    st.session_state.email = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'reset_email' not in st.session_state:
    st.session_state.reset_email = None
if 'reset_code_sent' not in st.session_state:
    st.session_state.reset_code_sent = False
if 'predicted_text' not in st.session_state:
    st.session_state.predicted_text = None
if 'prediction_time' not in st.session_state:
    st.session_state.prediction_time = None
if 'signup_success' not in st.session_state:
    st.session_state.signup_success = False
if 'signup_email' not in st.session_state:
    st.session_state.signup_email = None
if 'signup_username' not in st.session_state:
    st.session_state.signup_username = None

# ============================================
# LOGOUT FUNCTION
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
    st.markdown('<p class="main-header">📝 Sinhala Handwritten OCR</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Convert handwritten Sinhala documents to digital text</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.markdown("### 🔐 Welcome Back")
            st.markdown("Login to access your OCR dashboard")
            st.markdown("---")
            
            with st.form("login_form"):
                username_or_email = st.text_input("📧 Email or Username", placeholder="Enter your email or username")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    submitted = st.form_submit_button("🚀 Login", use_container_width=True)
                with col_b:
                    if st.form_submit_button("📝 Sign Up", use_container_width=True):
                        st.session_state.page = 'signup'
                        st.rerun()
                
                if submitted:
                    if not username_or_email or not password:
                        st.error("❌ Please fill all fields")
                    else:
                        success, result = login_user(username_or_email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = result['username']
                            st.session_state.email = result['email']
                            st.session_state.page = 'main'
                            st.rerun()
                        else:
                            st.error(f"❌ {result}")
            
            st.markdown("---")
            if st.button("🔑 Forgot Password?", use_container_width=True):
                st.session_state.page = 'forgot_password'
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SIGNUP PAGE (AUTO-LOGIN AFTER SIGNUP)
# ============================================

def signup_page():
    st.markdown('<p class="main-header">📝 Create Account</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Join us and start using OCR technology</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            st.markdown("### ✨ Create New Account")
            st.markdown("---")
            
            with st.form("signup_form"):
                email = st.text_input("📧 Email Address", placeholder="your@email.com")
                username = st.text_input("👤 Username", placeholder="3-20 characters (letters, numbers, underscore)")
                password = st.text_input("🔒 Password", type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("✓ Confirm Password", type="password", placeholder="Re-enter your password")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    submitted = st.form_submit_button("✅ Sign Up", use_container_width=True)
                with col_b:
                    if st.form_submit_button("← Back to Login", use_container_width=True):
                        st.session_state.page = 'login'
                        st.rerun()
                
                if submitted:
                    if not email or not username or not password:
                        st.error("❌ Please fill all fields")
                    elif password != confirm_password:
                        st.error("❌ Passwords do not match")
                    else:
                        success, message = register_user(email, username, password)
                        if success:
                            # Auto-login after successful signup
                            login_success, login_result = login_user(username, password)
                            if login_success:
                                st.session_state.logged_in = True
                                st.session_state.username = login_result['username']
                                st.session_state.email = login_result['email']
                                st.session_state.page = 'main'
                                st.success(f"✅ {message}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.success(f"✅ {message}. Please login.")
                                st.session_state.page = 'login'
                                st.rerun()
                        else:
                            st.error(f"❌ {message}")
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FORGOT PASSWORD PAGE
# ============================================

def forgot_password_page():
    st.markdown('<p class="main-header">🔐 Reset Password</p>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="auth-card">', unsafe_allow_html=True)
            
            if not st.session_state.reset_code_sent:
                st.markdown("### 🔑 Forgot Password?")
                st.markdown("Enter your email to receive a reset code")
                st.markdown("---")
                
                with st.form("forgot_form"):
                    email = st.text_input("📧 Email Address", placeholder="your@email.com")
                    submitted = st.form_submit_button("📨 Send Reset Code", use_container_width=True)
                    
                    if submitted:
                        if not email:
                            st.error("❌ Please enter your email")
                        else:
                            success, result = generate_reset_code(email)
                            if success:
                                st.session_state.reset_email = email
                                st.session_state.reset_code_sent = True
                                st.success(f"✅ Reset code sent to {email}")
                                st.info("📱 Please check your email (or console) for the 6-digit code")
                                st.rerun()
                            else:
                                st.error(f"❌ {result}")
            else:
                st.markdown("### 🔐 Reset Your Password")
                st.markdown(f"Resetting for: **{st.session_state.reset_email}**")
                st.markdown("---")
                
                with st.form("reset_form"):
                    reset_code = st.text_input("📱 6-Digit Reset Code", placeholder="Enter the code")
                    new_password = st.text_input("🔒 New Password", type="password", placeholder="At least 6 characters")
                    confirm_password = st.text_input("✓ Confirm New Password", type="password", placeholder="Re-enter new password")
                    
                    submitted = st.form_submit_button("🔄 Reset Password", use_container_width=True)
                    
                    if submitted:
                        if not reset_code or not new_password:
                            st.error("❌ Please fill all fields")
                        elif new_password != confirm_password:
                            st.error("❌ Passwords do not match")
                        elif len(new_password) < 6:
                            st.error("❌ Password must be at least 6 characters")
                        else:
                            if verify_reset_code(st.session_state.reset_email, reset_code):
                                success, message = reset_password(st.session_state.reset_email, new_password)
                                if success:
                                    st.success(f"✅ {message}")
                                    st.session_state.reset_code_sent = False
                                    st.session_state.reset_email = None
                                    st.session_state.page = 'login'
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                            else:
                                st.error("❌ Invalid or expired reset code")
            
            st.markdown("---")
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.reset_code_sent = False
                st.session_state.reset_email = None
                st.session_state.page = 'login'
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN OCR APPLICATION
# ============================================

def main_app():
    # Logout button in top right
    st.markdown(f'''
    <button onclick="location.reload();" class="logout-btn" style="position: fixed; top: 20px; right: 20px; z-index: 1000; background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; border: none; border-radius: 30px; padding: 8px 20px; cursor: pointer; font-weight: 600;">
        🚪 Logout
    </button>
    ''', unsafe_allow_html=True)
    
    # Welcome banner
    st.markdown(f'''
    <div class="welcome-banner">
        <h2>👋 Welcome back, {st.session_state.username}!</h2>
        <p>Upload a handwritten Sinhala document image and get digital text in seconds.</p>
    </div>
    ''', unsafe_allow_html=True)
    
    # Load OCR model
    with st.spinner("🔄 Loading OCR model... Please wait."):
        processor, model, device = load_ocr_model()
    
    if processor is None:
        st.error("❌ Failed to load OCR model. Please check your setup.")
        return
    
    # Main UI
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 📤 Upload Document")
        st.markdown("Supported formats: PNG, JPG, JPEG")
        
        uploaded_file = st.file_uploader(
            "Choose an image...", 
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear image of handwritten Sinhala text"
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Uploaded Image", use_container_width=True)
            
            if st.button("🔍 Recognize Text", type="primary", use_container_width=True):
                with st.spinner("🧠 Analyzing image and recognizing text..."):
                    predicted_text, error = predict_text(image, processor, model, device)
                    if predicted_text:
                        st.session_state.predicted_text = predicted_text
                        st.session_state.prediction_time = datetime.now()
                        st.success("✅ Recognition completed successfully!")
                    else:
                        st.error(f"❌ Error: {error}")
    
    with col2:
        st.markdown("### 📝 Recognition Result")
        
        if st.session_state.predicted_text:
            result_text = st.session_state.predicted_text
            st.markdown(f'''
            <div class="result-box">
                <strong>📄 Recognized Text:</strong><br><br>
                <span style="font-size: 1.2rem; line-height: 1.6;">{result_text}</span>
            </div>
            ''', unsafe_allow_html=True)
            
            st.caption(f"🕐 Recognized at: {st.session_state.prediction_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            col_copy, col_download = st.columns(2)
            with col_copy:
                if st.button("📋 Copy Text", use_container_width=True):
                    st.code(result_text)
                    st.success("✅ Text copied!")
            with col_download:
                txt_file = io.BytesIO(result_text.encode('utf-8'))
                st.download_button(
                    "💾 Download as TXT", 
                    data=txt_file, 
                    file_name=f"ocr_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 
                    use_container_width=True
                )
        else:
            st.info("👈 Upload an image and click 'Recognize Text' to see results here")
            
            # Show example
            st.markdown("---")
            st.markdown("### 📖 Example Output")
            st.markdown("""
            <div class="result-box">
                <strong>Sample Output:</strong><br><br>
                <span style="color: #888;">පුරුෂ</span><br>
                <span style="color: #888;">නීල් රූපසිංහ</span><br>
                <span style="color: #888;">සහෝදරයා</span>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #888; padding: 20px;">'
        '<p>Powered by <strong>TrOCR</strong> | Fine-tuned on <strong>SinOCR Dataset</strong></p>'
        '<p>© 2026 Sinhala Handwritten OCR | All Rights Reserved</p>'
        '</div>',
        unsafe_allow_html=True
    )

# ============================================
# PAGE ROUTING
# ============================================

# Handle logout via URL param
import streamlit as st

# Check for logout in query params
query_params = st.query_params
if 'logout' in query_params:
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
