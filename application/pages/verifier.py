import streamlit as st
import os
import hashlib
from utils.cert_utils import extract_certificate
from utils.streamlit_utils import view_certificate, displayPDF, hide_icons, hide_sidebar, remove_whitespaces
from connection import contract

st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Academics Certificate System")
# hide_icons()
# hide_sidebar()
# remove_whitespaces()

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
    .stSubheader, label, p, span, div, h1, h2, h3, h4, h5, h6,
    .stFileUploader, .stFileUploader label, .stFileUploader span, .stFileUploader div {
        color: #1e2c4c !important;
    }
    
    /* Selectbox styling with specific fixes for dropdown items */
    .stSelectbox > div > div > div {
        color: #1e2c4c !important;
        border-radius: 6px !important;
        border: 1px solid #cbd5e0 !important;
        background-color: #f8fafc !important;
    }
    
    /* Critical fix for dropdown options */
    .stSelectbox [data-baseweb="select"] ul li,
    .stSelectbox [data-baseweb="select"] ul li span,
    .stSelectbox [data-baseweb="select"] ul li div,
    .stSelectbox [data-baseweb="select"] [role="listbox"],
    .stSelectbox [data-baseweb="select"] [role="option"],
    [data-baseweb="select"] ul,
    [data-baseweb="select"] ul li,
    [data-baseweb="select"] ul li *,
    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] ul li,
    [data-baseweb="popover"] ul li * {
        background-color: white !important;
        color: #1e2c4c !important;
    }
    
    /* Hover state for dropdown items */
    .stSelectbox [data-baseweb="select"] ul li:hover,
    .stSelectbox [data-baseweb="select"] [role="option"]:hover,
    [data-baseweb="select"] ul li:hover,
    [data-baseweb="popover"] ul li:hover {
        background-color: #e2e8f0 !important;  
    }
    
    /* File uploader styling */
    .stFileUploader > div > label {
        font-weight: 500 !important;
        color: #1e2c4c !important;
        font-size: 1rem !important;
    }
    
    .stFileUploader > div > div {
        border-radius: 6px !important;
        border: 1px dashed #cbd5e0 !important;
        background-color: #f8fafc !important;
        padding: 1.5rem !important;
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
    
    /* Success/error message styling */
    .stAlert {
        border-radius: 8px !important;
        padding: 1rem !important;
        margin-top: 1rem !important;
    }
    
    .success-message {
        padding: 1rem;
        background-color: #ecfdf5;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 4px solid #10b981;
    }

    .error-message {
        padding: 1rem;
        background-color: #fff1f2;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 4px solid #e11d48;
    }
    
    /* PDF display container */
    .pdf-container {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        background-color: white;
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
st.markdown("<p class='subheading'>Verify the authenticity of academic certificates</p>", unsafe_allow_html=True)

st.markdown("<div class='form-container'>", unsafe_allow_html=True)
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
                (uid, candidate_name, course_name, org_name) = extract_certificate("certificate.pdf")
                
                # Display certificate
                st.markdown("<div class='section-header'>Certificate Preview</div>", unsafe_allow_html=True)
                st.markdown("<div class='pdf-container'>", unsafe_allow_html=True)
                displayPDF("certificate.pdf")
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Clean up temporary file
                os.remove("certificate.pdf")
                
                # Calculate certificate ID
                data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
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
                    st.markdown(f"""
                    <div style="padding: 1rem; background-color: #f8fafc; border-radius: 8px; margin-top: 1rem;">
                        <p style="margin-bottom: 0.5rem; font-weight: 600;">Certificate Details:</p>
                        <p style="margin-bottom: 0.25rem;"><strong>Certificate ID:</strong> {certificate_id}</p>
                        <p style="margin-bottom: 0.25rem;"><strong>Student ID:</strong> {uid}</p>
                        <p style="margin-bottom: 0.25rem;"><strong>Student Name:</strong> {candidate_name}</p>
                        <p style="margin-bottom: 0;"><strong>Course:</strong> {course_name}</p>
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
st.markdown('</div>', unsafe_allow_html=True)  
st.markdown('</div>', unsafe_allow_html=True) 