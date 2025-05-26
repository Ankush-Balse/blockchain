import streamlit as st
from PIL import Image
from utils.streamlit_utils import hide_icons, hide_sidebar, remove_whitespaces
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Academics Certificate System")
# hide_icons()
# hide_sidebar()
remove_whitespaces()

st.markdown("""
    <style>
    /* Global Reset */
    .stApp {
        background-color: #f8f9fa !important;
        color: #212529 !important;
    }
    
    body {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        margin: 0;
        padding: 0;
    }
    
    /* Container for better responsiveness */
    .content-container {
        max-width: 1440px;
        margin: 0 auto;
        padding: 1rem;
    }
    
    /* Main title */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        color: #102040;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        text-transform: uppercase;
    }
    
    /* Subheading */
    .subheading {
        text-align: center;
        font-size: 1.5rem;
        color: #495057;
        margin-bottom: 3rem;
        font-weight: 400;
    }
    
    /* Custom role container styles */
    .role-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 0;
        margin-bottom: 20px;
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
    }
    
    .role-card:hover {
        border-color: #1a4b8c;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
        transform: translateY(-5px);
    }
    
    .role-header {
        background-color: #f8f9fa;
        padding: 15px;
        font-size: 1.5rem;
        font-weight: 600;
        color: #0d2240;
        text-align: center;
        border-bottom: 1px solid #dee2e6;
    }
    
    .role-content {
        padding: 25px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        flex-grow: 1;
        text-align: center;
    }
    

    .role-content > div {
        display: flex !important;
        justify-content: center !important;
        width: 100% !important;
        
    }
    
    /* Center-align images */
    .role-content img {
        display: block !important;
        margin: 0 auto !important;
        max-width: 100% !important;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #1a4b8c !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 16px 40px !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        margin-top: 30px !important;
        width: 80% !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    
    .stButton > button:hover {
        background-color: #0d3663 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15) !important;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-18e3th9 {padding-top: 0;}
    .css-1d391kg {padding-top: 1rem;}
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 1rem;
        color: #6c757d;
        font-size: 0.85rem;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="content-container">', unsafe_allow_html=True)

# Title section
st.markdown("<h1 class='main-title'>Academics Certificate System</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheading'>Select your role to continue</p>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

# Define roles
roles = [
    ("Institute", "../assets/ins_logo.png", "institute_btn", col1, 400),
    ("Verifier", "../assets/comp_logo.png", "verifier_btn", col2, 400)
]

for role_name, image_path, button_key, column, width in roles:
    with column:
        st.markdown(f"""
        <div class="role-card">
            <div class="role-header">{role_name}</div>
            <div class="role-content">
        """, unsafe_allow_html=True)
        
        with st.container():
            _, img_col, _ = st.columns([1, 10, 1])
            with img_col:
                logo = Image.open(image_path)
                st.image(logo, output_format="PNG", width=width)
        
        if st.button("Select Role", key=button_key):
            st.session_state.profile = role_name
            switch_page("login")
        
        st.markdown('</div></div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Academics Certificate System</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)