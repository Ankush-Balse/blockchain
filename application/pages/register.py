import streamlit as st
from db.firebase_app import register
from streamlit_extras.switch_page_button import switch_page
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Academics Certificate System")
remove_whitespaces()

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
    
    /* Checkbox label styling */
    .stCheckbox > div > div > label {
        color: #1e2c4c !important;
        font-weight: 500 !important;
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
    
    /* Login link styling */
    .login-link {
        text-align: center;
        margin-top: 1.5rem;
        font-size: 0.95rem;
    }
    
    .login-link a {
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
st.markdown("<p class='subheading'>Secure verification for academic credentials</p>", unsafe_allow_html=True)

st.markdown("<div class='form-container'>", unsafe_allow_html=True)
st.markdown("<h2 class='form-title'>Create a New Account</h2>", unsafe_allow_html=True)

with st.form("registration_form", clear_on_submit=False):
    st.markdown("<div class='section-header'>Select account type:</div>", unsafe_allow_html=True)
    
    profile_type = st.radio(
        "Account Type",
        ["Institute", "Verifier"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if 'profile' not in st.session_state:
        st.session_state.profile = profile_type
    else:
        st.session_state.profile = profile_type
    
    st.markdown("<hr style='margin: 20px 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Account Information</div>", unsafe_allow_html=True)
    
    email = st.text_input(
        "Email Address", 
        placeholder="Enter your email address"
    )
    
    password = st.text_input(
        "Password", 
        type="password", 
        placeholder="Create a secure password (min. 8 characters)"
    )
    
    confirm_password = st.text_input(
        "Confirm Password", 
        type="password", 
        placeholder="Re-enter your password"
    )
    
    st.markdown("<div style='margin-top: 20px; margin-bottom: 20px; padding: 10px; background-color: #f1f5f9; border-radius: 5px; border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    terms_agree = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="terms_checkbox")
    st.markdown("</div>", unsafe_allow_html=True)
    
    submit_button = st.form_submit_button("Register Account")
    
    if submit_button:
        if not email or not password or not confirm_password:
            st.error("Please fill in all required fields")
        elif password != confirm_password:
            st.error("Passwords do not match")
        elif len(password) < 8:
            st.warning("Password should be at least 8 characters")
        elif not terms_agree:
            st.warning("Please agree to the Terms and Privacy Policy")
        else:
            result = register(email, password)
            if result == "success":
                st.success("Registration successful! Redirecting to your dashboard...")
                st.balloons()
                
                if st.session_state.profile == "Institute":
                    switch_page("institute")
                else:
                    switch_page("verifier")
            else:
                st.error(f"Registration failed: {result}")

st.markdown("<div class='login-link'><span style='color: #1e2c4c;'>Already have an account?</span> <a href='javascript:void(0);' onclick='window.location.href=\"login\"' style='color: #1e40af; font-weight: 600;'>Log in here</a></div>", unsafe_allow_html=True)

if st.button("Already have an account? Log in", key="login_button"):
    switch_page("login")

st.markdown('</div>', unsafe_allow_html=True)  

st.markdown('<div class="footer" style="color: #1e2c4c;">Academics Certificate System</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True) 