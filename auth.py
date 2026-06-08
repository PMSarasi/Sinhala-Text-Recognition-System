# ============================================
# AUTHENTICATION MODULE
# Handles user registration, login, password reset
# ============================================

import sqlite3
import bcrypt
import re
from datetime import datetime
import streamlit as st

# Database setup
def init_db():
    """Initialize SQLite database for users"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT UNIQUE NOT NULL,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create password reset table
    c.execute('''CREATE TABLE IF NOT EXISTS password_resets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT NOT NULL,
                  reset_code TEXT NOT NULL,
                  expires_at TIMESTAMP NOT NULL,
                  used INTEGER DEFAULT 0)''')
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_username(username):
    """Validate username (alphanumeric, 3-20 chars)"""
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None

def validate_password_strength(password):
    """Check password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    return True, ""

def register_user(email, username, password):
    """Register a new user"""
    # Validate inputs
    if not validate_email(email):
        return False, "Invalid email format"
    
    if not validate_username(username):
        return False, "Username must be 3-20 characters (letters, numbers, underscore)"
    
    valid, msg = validate_password_strength(password)
    if not valid:
        return False, msg
    
    # Check if user exists
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    c.execute("SELECT id FROM users WHERE email = ? OR username = ?", (email, username))
    if c.fetchone():
        conn.close()
        return False, "Email or username already exists"
    
    # Insert new user
    hashed_pw = hash_password(password)
    c.execute("INSERT INTO users (email, username, password) VALUES (?, ?, ?)",
              (email, username, hashed_pw))
    conn.commit()
    conn.close()
    
    return True, "Registration successful! Please login."

def login_user(username_or_email, password):
    """Authenticate user"""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    # Check by email or username
    c.execute("SELECT id, username, email, password FROM users WHERE email = ? OR username = ?",
              (username_or_email, username_or_email))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(password, user[3]):
        return True, {"id": user[0], "username": user[1], "email": user[2]}
    
    return False, "Invalid credentials"

def generate_reset_code(email):
    """Generate password reset code"""
    import random
    import string
    
    # Check if email exists
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE email = ?", (email,))
    if not c.fetchone():
        conn.close()
        return False, "Email not found"
    
    # Generate 6-digit code
    reset_code = ''.join(random.choices(string.digits, k=6))
    
    # Store reset code (expires in 1 hour)
    from datetime import datetime, timedelta
    expires_at = datetime.now() + timedelta(hours=1)
    
    # Invalidate old codes
    c.execute("UPDATE password_resets SET used = 1 WHERE email = ?", (email,))
    c.execute("INSERT INTO password_resets (email, reset_code, expires_at) VALUES (?, ?, ?)",
              (email, reset_code, expires_at))
    conn.commit()
    conn.close()
    
    return True, reset_code

def verify_reset_code(email, reset_code):
    """Verify password reset code"""
    from datetime import datetime
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''SELECT id FROM password_resets 
                 WHERE email = ? AND reset_code = ? AND expires_at > ? AND used = 0''',
              (email, reset_code, datetime.now()))
    valid = c.fetchone() is not None
    conn.close()
    
    return valid

def reset_password(email, new_password):
    """Reset user password"""
    valid, msg = validate_password_strength(new_password)
    if not valid:
        return False, msg
    
    hashed_pw = hash_password(new_password)
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_pw, email))
    # Mark reset codes as used
    c.execute("UPDATE password_resets SET used = 1 WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    
    return True, "Password reset successful"

# Initialize database
init_db()
