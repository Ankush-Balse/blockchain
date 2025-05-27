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
    /* Global Reset with Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #334155 100%) !important;
        color: #f8fafc !important;
        min-height: 100vh;
    }

    body {
        font-family: 'Segoe UI', 'Roboto', sans-serif;
        margin: 0;
        padding: 0;
    }

    /* Container */
    .content-container {
        max-width: 1440px;
        margin: 0 auto;
        padding: 1rem;
    }

    /* Titles */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        color: #06b6d4;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
        text-transform: uppercase;
    }

    .subheading {
        text-align: center;
        font-size: 1.5rem;
        color: #94a3b8;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Role Card */
    .role-card {
        background-color: rgba(30, 41, 59, 0.8);
        border: 1px solid #475569;
        border-radius: 8px;
        padding: 0;
        margin-bottom: 20px;
        overflow: hidden;
        height: 100%;
        display: flex;
        flex-direction: column;
        transition: all 0.3s ease;
        color: #f1f5f9;
    }

    .role-card:hover {
        border-color: #06b6d4;
        box-shadow: 0 8px 16px rgba(6, 182, 212, 0.2);
        transform: translateY(-5px);
    }

    .role-header {
        background-color: #1e293b;
        padding: 15px;
        font-size: 1.5rem;
        font-weight: 600;
        color: #06b6d4;
        text-align: center;
        border-bottom: 1px solid #334155;
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

    .role-content img {
        display: block !important;
        margin: 0 auto !important;
        max-width: 100% !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: #06b6d4 !important;
        color: #0f172a !important;
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
        background-color: #0891b2 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 8px rgba(6, 182, 212, 0.3) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        margin-top: 3rem;
        margin-bottom: 1rem;
        color: #94a3b8;
        font-size: 0.85rem;
    }

    /* Text Visibility Fix */
    .stMarkdown, .stMarkdown p, .stMarkdown span, .stMarkdown div,
    .stRadio, .stRadio label, .stRadio span, .stRadio div,
    .stCheckbox, .stCheckbox label, .stCheckbox span, .stCheckbox div,
    .stTextInput, .stTextInput label, .stTextInput span, .stTextInput div,
    .stButton, .stButton label, .stButton span, .stButton div,
    .stSubheader, label, p, span, div, h1, h2, h3, h4, h5, h6,
    .stSelectbox, .stSelectbox label, .stSelectbox span, .stSelectbox div {
        color: #f1f5f9 !important;
    }

    /* Hide Streamlit default UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-18e3th9 {padding-top: 0;}
    .css-1d391kg {padding-top: 1rem;}
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