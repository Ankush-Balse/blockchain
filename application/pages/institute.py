import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
import hashlib
from utils.cert_utils import generate_certificate
from utils.streamlit_utils import view_certificate, hide_icons, hide_sidebar, remove_whitespaces
from connection import contract, w3
from PyPDF2 import PdfReader, PdfWriter
import qrcode
from PIL import Image
from streamlit_extras.switch_page_button import switch_page

if "user" not in st.session_state or st.session_state.user != "Institute":
    st.session_state.profile = "Institute"
    switch_page("login")

def run():
    def generate_qr_code(data):
        qr = qrcode.QRCode(
            version=1,
            box_size=6,
            border=2
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white").convert("RGB")
        return img

    st.set_page_config(layout="wide", initial_sidebar_state="collapsed", page_title="Academics Certificate System")
    # hide_icons()
    # hide_sidebar()
    # remove_whitespaces()
    load_dotenv()

    api_key = os.getenv("PINATA_API_KEY")
    api_secret = os.getenv("PINATA_API_SECRET")

    def upload_to_pinata(file_path, api_key, api_secret):
        pinata_api_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        headers = {
            "pinata_api_key": api_key,
            "pinata_secret_api_key": api_secret,
        }
        
        with open(file_path, "rb") as file:
            file_data = file.read()
            file_name = os.path.basename(file_path)
        
        files = {
            "file": (file_name, file_data, "application/pdf")
        }
        
        response = requests.post(pinata_api_url, headers=headers, files=files)
        
        result = json.loads(response.text)
        if "IpfsHash" in result:
            ipfs_hash = result["IpfsHash"]
            print(f"File uploaded to Pinata. IPFS Hash: {ipfs_hash}")
            return ipfs_hash
        else:
            print(f"Error uploading to Pinata: {result.get('error', 'Unknown error')}")
            return None

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

    st.markdown("<div class='main-title'><h1>ACADEMICS CERTIFICATE SYSTEM</h1><p class='subheading'>Secure management of academic certificates using blockchain</p></div>", unsafe_allow_html=True)

    st.markdown("<h2 class='form-title'>Certificate Management Portal</h2>", unsafe_allow_html=True)

    options = ("Generate Certificate", "Upload Certificate", "View Certificates")
    selected = st.selectbox("Select an action", options, label_visibility="collapsed")

    if selected == options[0]:
        st.markdown("<div class='section-header'>Create New Certificate</div>", unsafe_allow_html=True)
        
        with st.form("Generate-Certificate"):
            uid = st.text_input(label="Student UID", placeholder="Enter unique student ID")
            candidate_name = st.text_input(label="Student Name", placeholder="Enter student full name")
            course_name = st.text_input(label="Course Name", placeholder="Enter course title")
            org_name = st.text_input(label="Institution Name", placeholder="Enter institution name")
            
            submit = st.form_submit_button("Generate Certificate")
            
            if submit:
                if not uid or not candidate_name or not course_name or not org_name:
                    st.error("Please fill in all fields")
                else:
                    with st.spinner("Generating certificate and uploading to IPFS..."):
                        # Generate certificate file
                        pdf_file_path = "certificate.pdf"
                        institute_logo_path = "../assets/ins_logo.png"
                        generate_certificate(pdf_file_path, uid, candidate_name, course_name, org_name, institute_logo_path)
                        
                        # Upload the PDF to Pinata
                        ipfs_hash = upload_to_pinata(pdf_file_path, api_key, api_secret)
                        
                        # Clean up temporary file
                        os.remove(pdf_file_path)
                        
                        if ipfs_hash:
                            # Create unique certificate ID
                            data_to_hash = f"{uid}{candidate_name}{course_name}{org_name}".encode('utf-8')
                            certificate_id = hashlib.sha256(data_to_hash).hexdigest()
                            
                            # Store on blockchain
                            contract.functions.generateCertificate(
                                certificate_id, uid, candidate_name, course_name, org_name, ipfs_hash
                            ).transact({'from': w3.eth.accounts[0]})
                            
                            st.success(f"Certificate successfully generated!")

                            cert_qr_img = generate_qr_code(certificate_id)
                            ipfs_qr_img = generate_qr_code("https://ipfs.io/ipfs/"+ipfs_hash)

                            # Display results
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown("**Certificate ID QR Code:**")
                                st.image(cert_qr_img)

                            with col2:
                                st.markdown("**IPFS Hash QR Code:**")
                                st.image(ipfs_qr_img)

                            st.markdown(f"""
                            <div style="padding: 1rem; background-color: #000000; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #0369a1;">
                                <p style="margin-bottom: 0.5rem; font-weight: 600;"><h3>Certificate Details:</h3></p>
                                <p style="margin-bottom: 0.25rem;"><strong>Certificate ID:</strong> {certificate_id}</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Student:</strong> {candidate_name}</p>
                                <p style="margin-bottom: 0.25rem;"><strong>Course:</strong> {course_name}</p>
                                <p style="margin-bottom: 0;"><strong>IPFS Hash:</strong> {ipfs_hash}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.error("Failed to upload certificate to IPFS. Please try again.")
    elif selected == options[1]:
        st.markdown("<div class='section-header'>Upload Certificate PDF</div>", unsafe_allow_html=True)

        with st.form("Generate-Certificate"):
            uid = st.text_input(label="Student UID", placeholder="Enter unique student ID")
            candidate_name = st.text_input(label="Student Name", placeholder="Enter student full name")
            org_name = st.text_input(label="Institution Name", placeholder="Enter institution name")
            certificate_name = st.text_input(label="Certificate Name", placeholder="Enter certificate name")
            uploaded_file = st.file_uploader("Upload the PDF version of the certificate", 
                                            type="pdf",
                                            help="The certificate must be in PDF format and include all required information.")

            submit = st.form_submit_button("Upload Certificate")
            if submit:
                if not uid or not candidate_name or not org_name or not certificate_name:
                    st.error("Please fill in all fields")
                elif not uploaded_file:
                    st.error("Please upload the corresponding certificate")
                else:
                    with st.spinner("Analyzing certificate..."):
                        coverpage_file_path = "coverpage.pdf"
                        certificate_file_path = "certificate.pdf"
                        complete_file_path = "complete.pdf"

                        institute_logo_path = "../assets/ins_logo.png"
                        generate_certificate(coverpage_file_path, uid, candidate_name, certificate_name, org_name, institute_logo_path, False)

                        bytes_data = uploaded_file.getvalue()
                        with open(certificate_file_path, "ab") as file:
                            file.write(bytes_data)  

                        st.markdown("<div class='section-header'>Certificate Preview</div>", unsafe_allow_html=True)
                        st.markdown("<div class='pdf-container'>", unsafe_allow_html=True)
                        st.markdown("</div>", unsafe_allow_html=True)

                        coverpage_reader = PdfReader(coverpage_file_path)
                        certificate_reader = PdfReader(certificate_file_path)

                        writer = PdfWriter()
                        for page in coverpage_reader.pages:
                            writer.add_page(page)
                        for page in certificate_reader.pages:
                            writer.add_page(page)
                        
                        with open(complete_file_path, "wb") as complete_file:
                            writer.write(complete_file)
                        
                        ipfs_hash = upload_to_pinata(complete_file_path, api_key, api_secret)

                        os.remove(coverpage_file_path)
                        os.remove(certificate_file_path)
                        os.remove(complete_file_path)

                        if ipfs_hash:
                            # Create unique certificate ID
                            data_to_hash = f"{uid}{candidate_name}{certificate_name}{org_name}".encode('utf-8')
                            certificate_id = hashlib.sha256(data_to_hash).hexdigest()
                                    
                            # Store on blockchain
                            contract.functions.generateCertificate(
                                certificate_id, uid, candidate_name, certificate_name, org_name, ipfs_hash
                            ).transact({'from': w3.eth.accounts[0]})
                                    
                            st.success(f"Certificate successfully uploaded!")
                            cert_qr_img = generate_qr_code(certificate_id)
                            ipfs_qr_img = generate_qr_code("https://ipfs.io/ipfs/"+ipfs_hash)

                            # Display results
                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown("**Certificate ID QR Code:**")
                                st.image(cert_qr_img)

                            with col2:
                                st.markdown("**IPFS Hash QR Code:**")
                                st.image(ipfs_qr_img)
                            st.markdown(f"""
                                <div style="padding: 1rem; background-color: #000000; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #0369a1;">
                                    <p style="margin-bottom: 0.5rem; font-weight: 600; color: #000000;">Certificate Details:</p>
                                    <p style="margin-bottom: 0.25rem;"><strong>Certificate ID:</strong> {certificate_id}</p>
                                    <p style="margin-bottom: 0.25rem;"><strong>Student:</strong> {candidate_name}</p>
                                    <p style="margin-bottom: 0.25rem;"><strong>Certificate:</strong> {certificate_name}</p>
                                    <p style="margin-bottom: 0;"><strong>IPFS Hash:</strong> {ipfs_hash}</p>
                                </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.error("Failed to upload certificate to IPFS. Please try again.")

    else:
        st.markdown("<div class='section-header'>View Certificate</div>", unsafe_allow_html=True)
        
        with st.form("View-Certificate"):
            certificate_id = st.text_input("Certificate ID", placeholder="Enter the certificate ID to view")
            submit = st.form_submit_button("View Certificate")
            
            if submit:
                if not certificate_id:
                    st.error("Please enter a certificate ID")
                else:
                    result = contract.functions.isVerified(certificate_id).call()
                    if result:
                        try:
                            with st.spinner("Retrieving certificate from blockchain..."):
                                view_certificate(certificate_id)
                        except Exception as e:
                            st.error("Invalid Certificate ID or certificate not found!")
                            st.markdown(f"""
                            <div style="padding: 1rem; background-color: #000000; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #e11d48;">
                                <p style="margin-bottom: 0;">The certificate ID you entered could not be verified. Please check the ID and try again.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("Invalid Certificate ID or certificate not found!")
                        st.markdown(f"""
                            <div style="padding: 1rem; background-color: #000000; border-radius: 8px; margin-top: 1rem; border-left: 4px solid #e11d48;">
                                <p style="margin-bottom: 0;">The certificate ID you entered could not be verified. Please check the ID and try again.</p>
                            </div>
                            """, unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="footer" style="color: #1e2c4c;">Academics Certificate System.</div>', unsafe_allow_html=True)

run()