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

def run():
    st.markdown("""
        <style>
        /* Global Reset with Modern Dark Theme */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%) !important;
            color: #f8fafc !important;
            min-height: 100vh;
        }

        /* Container for better responsiveness */
        .content-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem 1rem;
        }

        /* Main title with cyan accent */
        .main-title {
            text-align: center;
            font-size: 2.8rem;
            font-weight: 800
        }

        /* Subheading */
        .subheading {
            text-align: center;
            font-size: 1.3rem;
            color: #94a3b8;
            margin-bottom: 2rem;
            font-weight: 500;
        }

        /* Form container with dark glass effect */
        .form-container {
            background: rgba(30, 41, 59, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            padding: 3rem;
            margin-bottom: 2rem;
            max-width: 650px;
            margin-left: auto;
            margin-right: auto;
        }

        .form-title {
            font-size: 1.6rem;
            font-weight: 700;
            color: #06b6d4;
            margin-bottom: 1.5rem;
            text-align: center;
        }
        
        /* Enhanced text visibility */
        .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div,
        .stRadio, .stRadio label, .stRadio span, .stRadio div,
        .stCheckbox, .stCheckbox label, .stCheckbox span, .stCheckbox div,
        .stTextInput, .stTextInput label, .stTextInput span, .stTextInput div,
        .stButton, .stButton label, .stButton span, .stButton div,
        .stSubheader, label, p, span, div, h1, h2, h3, h4, h5, h6,
        .stSelectbox, .stSelectbox label, .stSelectbox span, .stSelectbox div {
            color: #f1f5f9 !important;
            font-weight: 500;
        }
        
        /* Dark Selectbox styling */
        .stSelectbox > div > div > div {
            border-radius: 12px !important;
            border: 2px solid #475569 !important;
            background: linear-gradient(145deg, #1e293b, #334155) !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease !important;
            color: #f1f5f9 !important;
        }
        
        .stSelectbox > div > div > div:hover {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.2) !important;
        }
        
        /* Modern Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
            border-bottom: 2px solid #475569;
            background: rgba(30, 41, 59, 0.6);
            border-radius: 12px 12px 0 0;
            padding: 0.5rem;
        }
        
        .stTabs [data-baseweb="tab"] {
            font-weight: 600;
            color: #94a3b8 !important;
            padding: 1rem 1.5rem !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            background: transparent !important;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(6, 182, 212, 0.1) !important;
            color: #06b6d4 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #06b6d4, #0891b2) !important;
            color: white !important;
            box-shadow: 0 4px 12px rgba(6, 182, 212, 0.4) !important;
        }
        
        /* Section headers */
        .section-header {
            font-size: 1.3rem;
            font-weight: 700;
            color: #06b6d4 !important;
            margin-top: 2rem;
            margin-bottom: 1rem;
            position: relative;
        }
        
        .section-header::after {
            content: '';
            position: absolute;
            bottom: -4px;
            left: 0;
            width: 50px;
            height: 3px;
            background: linear-gradient(135deg, #06b6d4, #0891b2);
            border-radius: 2px;
        }
        
        /* Enhanced Input fields */
        .stTextInput > label {
            font-weight: 600 !important;
            color: #f1f5f9 !important;
            font-size: 1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stTextInput > div > div > input {
            border-radius: 12px !important;
            border: 2px solid #475569 !important;
            padding: 1rem 1.25rem !important;
            color: #f1f5f9 !important;
            background: linear-gradient(145deg, #1e293b, #334155) !important;
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.3) !important;
            transition: all 0.3s ease !important;
            font-size: 1rem !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 0 3px rgba(6, 182, 212, 0.2), inset 0 2px 4px rgba(0,0,0,0.3) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #64748b !important;
        }
        
        /* Modern Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%) !important;
            color: white !important;
            font-weight: 700 !important;
            padding: 1rem 2rem !important;
            border-radius: 12px !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
            border: none !important;
            margin-top: 1.5rem !important;
            font-size: 1.1rem !important;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.3) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(6, 182, 212, 0.4) !important;
            background: linear-gradient(135deg, #0891b2 0%, #0e7490 100%) !important;
        }
        
        .stButton > button:active {
            transform: translateY(0) !important;
        }
        
        /* Enhanced Success/error messages */
        .stAlert {
            border-radius: 12px !important;
            padding: 1.25rem !important;
            margin-top: 1rem !important;
            border: none !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        }
        
        .stAlert[data-baseweb="notification"] {
            background: linear-gradient(135deg, #10b981, #059669) !important;
            color: white !important;
        }
        
        /* Enhanced Radio and Checkbox */
        .stRadio > label, .stCheckbox > label {
            font-weight: 600 !important;
            color: #f1f5f9 !important;
            margin-bottom: 0.75rem !important;
        }
        
        /* Radio button styling */
        .stRadio [role="radiogroup"] > label {
            background: rgba(30, 41, 59, 0.6) !important;
            border: 2px solid #475569 !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
            margin: 0.25rem 0 !important;
            transition: all 0.3s ease !important;
        }
        
        .stRadio [role="radiogroup"] > label:hover {
            border-color: #06b6d4 !important;
            background: rgba(6, 182, 212, 0.1) !important;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(30, 41, 59, 0.5);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #06b6d4, #0891b2);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #0891b2, #0e7490);
        }
        
        /* Footer */
        .footer {
            text-align: center;
            margin-top: 3rem;
            padding: 2rem 1rem;
            background: rgba(30, 41, 59, 0.4);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            color: #94a3b8;
            font-size: 0.9rem;
            border: 1px solid rgba(148, 163, 184, 0.2);
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
        }
        
        /* Metrics styling */
        .metric-container {
            background: rgba(30, 41, 59, 0.6);
            border: 1px solid rgba(148, 163, 184, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* Add subtle animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 5px rgba(6, 182, 212, 0.2);
            }
            50% {
                box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
            }
        }
        
        .form-container {
            animation: fadeInUp 0.6s ease-out;
        }
        
        .main-title {
            animation: glow 3s ease-in-out infinite;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2.2rem;
                padding-bottom: 2rem;
            }
            
            .form-container {
                padding: 2rem 1.5rem;
                margin: 1rem;
            }
            
            .stTabs [data-baseweb="tab-list"] {
                gap: 0.5rem;
            }
            
            .stTabs [data-baseweb="tab"] {
                padding: 0.75rem 1rem !important;
                font-size: 0.9rem;
            }
        }
        
        /* Fix for white text in dark theme */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
        .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #06b6d4 !important;
        }
        
        /* Dataframe styling */
        .stDataFrame {
            background: rgba(30, 41, 59, 0.8) !important;
            border-radius: 12px !important;
            overflow: hidden !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div  class='main-title'><h1>ACADEMICS CERTIFICATE SYSTEM</h1><p class='subheading'>Secure verification of academic certificates</p></div>", unsafe_allow_html=True)
    st.markdown("<h2 class='form-title'>Welcome Back!!</h2>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Select account type:</div>", unsafe_allow_html=True)

    st.markdown("<hr style='margin: 20px 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)

    if 'profile' not in st.session_state:
        st.session_state.profile = "Institute"

    with st.form("login_form", clear_on_submit=False):
        st.markdown("<div class='section-header'>Login Information</div>", unsafe_allow_html=True)
        
        profile_type = st.radio(
            "Account Type",
            ["Institute", "Verifier"],
            index=0 if st.session_state.profile == "Institute" else 1,
            horizontal=True,
            label_visibility="collapsed"
        )

        st.session_state.profile = profile_type
        
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
                        st.session_state.user = "Institute"
                        switch_page("institute")
                    else:
                        st.error("Invalid credentials!")
                else:
                    result = login(email, password)
                    if result == "success":
                        st.success("Login successful! Redirecting to your dashboard...")
                        st.session_state.user = "Verifier"
                        switch_page("verifier")
                    else:
                        st.error("Invalid credentials!")

    st.markdown("<div class='register-link'><span style='color: #1e2c4c;'>Don't have an account yet?</span> <a href='javascript:void(0);' onclick='window.location.href=\"register\"' style='color: #1e40af; font-weight: 600;'>Register here</a></div>", unsafe_allow_html=True)

    if st.button("New user? Register now", key="register_button"):
        switch_page("register")


    st.markdown('<div class="footer" style="color: #1e2c4c;">Academics Certificate System</div>', unsafe_allow_html=True)

run()