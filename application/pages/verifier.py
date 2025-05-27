import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate, displayPDF, hide_icons, hide_sidebar, remove_whitespaces
from connection import contract
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Academics Certificate System")

if "user" not in st.session_state or st.session_state.user != "Verifier":
    st.session_state.profile = "Verifier"
    switch_page("login")

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
    st.markdown("<h2 class='form-title'>Certificate Verification Portal</h2>", unsafe_allow_html=True)

    options = ("Verify Certificate using PDF", "View/Verify Certificate using Certificate ID")
    selected = st.selectbox("Verification Method", options, label_visibility="collapsed")

    if selected == options[0]:
        st.markdown("<div class='section-header'>Upload Certificate PDF</div>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload the PDF version of the certificate", 
                                        type="pdf",
                                        help="The certificate must be in PDF format and include all required information.")

        if uploaded_file is not None:
            with st.spinner("Analyzing certificate..."):
                bytes_data = uploaded_file.getvalue()
                with open("certificate.pdf", "wb") as file:
                    file.write(bytes_data)
                
                try:
                    # Extract certificate data
                    (uid, candidate_name, name, org_name, is_course) = extract_certificate("certificate.pdf")
                    
                    # Display certificate
                    st.markdown("<div class='section-header'>Certificate Preview</div>", unsafe_allow_html=True)
                    st.markdown("<div class='pdf-container'>", unsafe_allow_html=True)
                    displayPDF("certificate.pdf")
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Clean up temporary file
                    os.remove("certificate.pdf")
                    
                    # Calculate certificate ID
                    data_to_hash = f"{uid}{candidate_name}{name}{org_name}".encode('utf-8')
                    certificate_id = hashlib.sha256(data_to_hash).hexdigest()
                    
                    # Verify on blockchain
                    result = contract.functions.isVerified(certificate_id).call()
                    
                    st.markdown("<div class='section-header'>Verification Result</div>", unsafe_allow_html=True)
                    
                    if result:
                        st.markdown("""
                        <div class="success-message">
                            <p style="margin-bottom: 0.5rem; font-weight: 600; color: #047857 !important;">✓ Certificate Verified</p>
                            <p style="margin-bottom: 0;">This certificate is authentic and has been properly issued by the institution.</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display certificate details
                        if is_course:
                            st.markdown(f"""
                            <div style="padding: 1rem; background-color: #000000; border-radius: 8px; margin-top: 1rem;">
                                <p style="margin-bottom: 0.5rem; font-weight: 600;">Certificate Details:</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Certificate ID:</strong> {certificate_id}</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Student ID:</strong> {uid}</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Student Name:</strong> {candidate_name}</p>
                                <p style="margin-bottom: 0;"><strong>Course:</strong> {name}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="padding: 1rem; background-color: #000000; border-radius: 8px; margin-top: 1rem;">
                                <p style="margin-bottom: 0.5rem; font-weight: 600;">Certificate Details:</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Certificate ID:</strong> {certificate_id}</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Student ID:</strong> {uid}</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Student Name:</strong> {candidate_name}</p>
                                <p style="margin-bottom: 0;"><strong>Certificate:</strong> {name}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="error-message">
                            <p style="margin-bottom: 0.5rem; font-weight: 600; color: #be123c !important;">✗ Invalid Certificate</p>
                            <p style="margin-bottom: 0;">This certificate could not be verified. It may have been tampered with or was not issued by a recognized institution.</p>
                        </div>
                        """, unsafe_allow_html=True)
                except Exception as e:
                    st.markdown("""
                    <div class="error-message">
                        <p style="margin-bottom: 0.5rem; font-weight: 600; color: #be123c !important;">✗ Invalid Certificate</p>
                        <p style="margin-bottom: 0;">This certificate could not be processed. Please ensure you have uploaded a valid certificate PDF.</p>
                    </div>
                    """, unsafe_allow_html=True)

    elif selected == options[1]:
        st.markdown("<div class='section-header'>Verify by Certificate ID</div>", unsafe_allow_html=True)
        
        with st.form("Validate-Certificate"):
            certificate_id = st.text_input("Certificate ID", placeholder="Enter the certificate ID to verify")
            submit = st.form_submit_button("Verify Certificate")
            
            if submit:
                if not certificate_id:
                    st.error("Please enter a certificate ID")
                else:
                    try:
                        with st.spinner("Retrieving certificate from blockchain..."):
                            # Retrieve and display certificate
                            view_certificate(certificate_id)
                            
                            # Verify on blockchain
                            result = contract.functions.isVerified(certificate_id).call()
                            
                            if result:
                                st.markdown("""
                                <div class="success-message">
                                    <p style="margin-bottom: 0.5rem; font-weight: 600; color: #047857 !important;">✓ Certificate Verified</p>
                                    <p style="margin-bottom: 0;">This certificate is authentic and has been properly issued by the institution.</p>
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown("""
                                <div class="error-message">
                                    <p style="margin-bottom: 0.5rem; font-weight: 600; color: #be123c !important;">✗ Invalid Certificate</p>
                                    <p style="margin-bottom: 0;">This certificate could not be verified on the blockchain.</p>
                                </div>
                                """, unsafe_allow_html=True)
                    except Exception as e:
                        st.markdown("""
                        <div class="error-message">
                            <p style="margin-bottom: 0.5rem; font-weight: 600; color: #be123c !important;">✗ Invalid Certificate ID</p>
                            <p style="margin-bottom: 0;">The certificate ID you entered could not be found or is invalid.</p>
                        </div>
                        """, unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer" style="color: #1e2c4c;">Academics Certificate System</div>', unsafe_allow_html=True)


run()