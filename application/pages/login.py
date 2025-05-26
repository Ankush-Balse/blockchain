import streamlit as st
from db.firebase_app import login
from dotenv import load_dotenv
import os
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Academics Certificate System")
# hide_icons()
# hide_sidebar()
# remove_whitespaces()
load_dotenv()

st.markdown("""
    <style>
    /* Global Reset */
    .stApp {
        background-color: #f0f2f5 !important;
        color: #212529 !important;
    }

    /* Container for better responsiveness */
    .content-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem 1rem;
    }

    /* Main title */
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e2c4c;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    /* Subheading */
    .subheading {
        text-align: center;
        font-size: 1.2rem;
        color: #4a5568;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Form and Input Styles */
    .form-container {
        background-color: white;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 2.5rem;
        margin-bottom: 2rem;
        max-width: 650px;
        margin-left: auto;
        margin-right: auto;
    }

    .form-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e2c4c;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* ALL text content forced to visible color */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div,
    .stRadio, .stRadio label, .stRadio span, .stRadio div,
    .stCheckbox, .stCheckbox label, .stCheckbox span, .stCheckbox div,
    .stTextInput, .stTextInput label, .stTextInput span, .stTextInput div,
    .stButton, .stButton label, .stButton span, .stButton div,
    .stSubheader, label, p, span, div, h1, h2, h3, h4, h5, h6 {
        color: #1e2c4c !important;
    }
    
    /* Exceptions for button text */
    .stButton > button {
        color: white !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1e2c4c !important;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    /* Account type radio buttons enhancement */
    .stRadio > div > div > label {
        color: #1e2c4c !important;
        font-weight: 500 !important;
    }
    
    /* Input fields styling */
    .stTextInput > label {
        font-weight: 500 !important;
        color: #1e2c4c !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input {
        border-radius: 6px !important;
        border: 1px solid #cbd5e0 !important;
        padding: 0.75rem 1rem !important;
        color: #1a202c !important;
        background-color: #f8fafc !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1e40af !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 6px !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        border: none !important;
        margin-top: 1rem !important;
    }
    
    .stButton > button:hover {
        background-color: #1e3a8a !important;
        transform: translateY(-1px) !important;
    }
    
    /* Register link styling */
    .register-link {
        text-align: center;
        margin-top: 1.5rem;
        font-size: 0.95rem;
    }
    
    .register-link a {
        color: #1e40af !important;
        text-decoration: none;
        font-weight: 500;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        padding-bottom: 1rem;
        color: #4a5568;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>ACADEMICS CERTIFICATE SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheading'>Secure verification of academic certificates</p>", unsafe_allow_html=True)

st.markdown("<div class='form-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='form-title'>Welcome Back!!</h2>", unsafe_allow_html=True)

if 'profile' not in st.session_state:
    st.session_state.profile = "Verifier" 

st.markdown("<div class='section-header'>Select account type:</div>", unsafe_allow_html=True)
profile_type = st.radio(
    "Account Type",
    ["Institute", "Verifier"],
    index=0 if st.session_state.profile == "Institute" else 1,
    horizontal=True,
    label_visibility="collapsed"
)
st.session_state.profile = profile_type

st.markdown("<hr style='margin: 20px 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)

with st.form("login_form", clear_on_submit=False):
    st.markdown("<div class='section-header'>Login Information</div>", unsafe_allow_html=True)
    
    email = st.text_input(
        "Email Address", 
        placeholder="Enter your email address"
    )
    
    password = st.text_input(
        "Password", 
        type="password", 
        placeholder="Enter your password"
    )
    
    remember_me = st.checkbox("Remember me", key="remember_me")
    
    submit_button = st.form_submit_button("Login")
    
    if submit_button:
        if not email or not password:
            st.error("Please enter both email and password")
        else:
            if st.session_state.profile == "Institute":
                valid_email = os.getenv("institute_email")
                valid_pass = os.getenv("institute_password")
                if email == valid_email and password == valid_pass:
                    st.success("Login successful! Redirecting to your dashboard...")
                    switch_page("institute")
                else:
                    st.error("Invalid credentials!")
            else:
                result = login(email, password)
                if result == "success":
                    st.success("Login successful! Redirecting to your dashboard...")
                    switch_page("verifier")
                else:
                    st.error("Invalid credentials!")

st.markdown("<div class='register-link'><span style='color: #1e2c4c;'>Don't have an account yet?</span> <a href='javascript:void(0);' onclick='window.location.href=\"register\"' style='color: #1e40af; font-weight: 600;'>Register here</a></div>", unsafe_allow_html=True)

if st.button("New user? Register now", key="register_button"):
    switch_page("register")


st.markdown('<div class="footer" style="color: #1e2c4c;">cademics Certificate System</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) 