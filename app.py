!pip install dotenv
from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image 
import pdf2image
import google.generativeai as genai
import json
import sys
import subprocess
import pkg_resources

# Load environment variables
load_dotenv()

# Configure Gemini AI
if 'GOOGLE_API_KEY' in st.secrets:
    genai.configure(api_key=st.secrets['GOOGLE_API_KEY'])
else:
    st.error("Please set up the GOOGLE_API_KEY in your Streamlit secrets")
    st.stop()

# Load and apply custom CSS
def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css not found. Some styling may be missing.")

# Custom CSS for card containers
def create_card(title, content):
    st.markdown(f"""
        <div class="css-card">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
    """, unsafe_allow_html=True)

# Initialize Streamlit page
st.set_page_config(
    page_title="Legal Document Review System",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
load_css()

# Function to check and install missing packages
def install_missing_packages():
    required_packages = {
        'reportlab': 'reportlab',
        'PyPDF2': 'PyPDF2'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            pkg_resources.get_distribution(package)
        except pkg_resources.DistributionNotFound:
            missing_packages.append(pip_name)
    
    if missing_packages:
        st.error("Missing required packages. Please run the following command in your Anaconda prompt:")
        installation_command = "conda install " + " ".join(missing_packages)
        st.code(installation_command)
        st.write("Or using pip:")
        pip_command = "pip install " + " ".join(missing_packages)
        st.code(pip_command)
        st.stop()

# Check for required packages
install_missing_packages()

def get_gemini_response(context, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([context, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Main App UI
st.markdown('<h1 style="text-align: center;">⚖️ Legal Document Review System</h1>', unsafe_allow_html=True)

# Introduction Card
create_card(
    "Welcome to Legal Document Analyzer",
    "This AI-powered system helps you analyze legal documents with precision and efficiency. Upload your document and get comprehensive insights instantly."
)

st.markdown("---")

# How to Use Section
with st.expander("How to Use This System", expanded=True):
    st.markdown("""
    ### System Capabilities
    1. **Document Analysis**: Upload legal documents in PDF format
    2. **Context Addition**: Provide additional information or specific questions
    3. **Comprehensive Review**: Get detailed analysis across multiple dimensions
    
    ### Process Flow
    1. Upload your document
    2. Add any specific context or questions
    3. Choose the type of analysis you need
    4. Review the AI-generated insights
    """)

# Create two columns for the inputs
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("Document Upload")
    uploaded_file = st.file_uploader("Upload Legal Document (PDF)...", type=["pdf"])
    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully")
    else:
        st.info("Please upload a PDF document to begin analysis")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="css-card">', unsafe_allow_html=True)
    st.subheader("Analysis Options")
    analysis_context = st.text_area(
        "Additional Context or Focus Areas (Optional)",
        placeholder="Example:\n- Specific types of sensitive information to look for\n- Particular sections to focus on\n- Types of legal clauses to analyze\n- Any specific concerns or requirements",
        help="This context will help guide the analysis of your document"
    )

st.markdown("---")

# Analysis Options Section
st.subheader("Choose Analysis Type")
st.markdown('<div class="analysis-options">', unsafe_allow_html=True)

# Create three columns for better button layout
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    submit1 = st.button("Document Overview", use_container_width=True)
    submit2 = st.button("Risk Assessment", use_container_width=True)

with btn_col2:
    submit3 = st.button("Terms Analysis", use_container_width=True)
    submit4 = st.button("Language Review", use_container_width=True)

with btn_col3:
    submit5 = st.button("Classification", use_container_width=True)
    submit6 = st.button("KPI Analysis", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# After the existing buttons in the columns section, add a new section for email generation
st.markdown("---")
st.subheader("Generate Summary Email")
submit_email = st.button("Generate Summary Email for Senior Review", use_container_width=True)

# Add the email generation prompt after the existing prompts
input_prompt_email = """
You are a Legal Document Review Assistant preparing a summary email for senior review. Create a professional email that includes:

SUBJECT: Legal Document Review Summary - [Document Type] Analysis

Dear Sir/Madam,

I hope this email finds you well. I have completed the initial review of the subject document and would like to bring the following points to your attention:

1. Document Overview:
   [Provide a 2-3 line summary of the document type and purpose]

2. Key Findings:
   [List the main findings in bullet points]

3. Critical Review Points:
   [Create a table with the following columns]
   | Priority | Issue/Red Flag | Risk Level | Recommended Action |
   |----------|---------------|------------|-------------------|
   [Fill with identified issues]

4. Time-Sensitive Items:
   [List any deadlines or time-critical elements]

5. Recommended Next Steps:
   [List 2-3 concrete actions needed]

Please review and provide your guidance on the above points, particularly regarding [mention 1-2 specific critical issues].

Best regards,
Legal Review Team

Note: Please find the detailed analysis attached to this email.

Format this email professionally and ensure all critical information is clearly presented.
"""

# Results Section
st.markdown("---")
st.subheader("Analysis Results")

# Analysis prompts
input_prompt1 = """
You are an experienced Legal Document Reviewer. Analyze this legal document and provide:
1. Document type and purpose
2. Key parties involved
3. Validity assessment
4. Main terms and conditions
5. Any immediate red flags or concerns
6. Overall compliance status

Present your analysis in a clear, structured format with sections and bullet points where appropriate.
"""

input_prompt2 = """
You are a Legal Risk Assessment Specialist. Review this document and provide:
1. Potential legal risks and exposure
2. Compliance with relevant laws and regulations
3. Missing clauses or provisions
4. Jurisdictional considerations
5. Recommended risk mitigation measures
6. Specific areas requiring immediate attention

Format your response with clear headers and prioritized recommendations.
"""

input_prompt3 = """
You are a Contract Analysis Expert. Examine this document and detail:
1. Key obligations for all parties
2. Critical deadlines and timelines
3. Payment terms and financial obligations
4. Termination conditions
5. Liability and indemnification clauses
6. Force majeure provisions
7. Dispute resolution mechanisms

Present your findings in a structured format with clear sections for each category.
"""

input_prompt4 = """
You are a Legal Language Clarity Expert. Review this document and provide:
1. Assessment of language clarity and readability
2. Identification of ambiguous terms or phrases
3. Analysis of defined terms and their consistency
4. Suggestions for improving clarity
5. Alternative phrasing for complex legal jargon
6. Overall document coherence evaluation

Structure your response with specific examples and suggested improvements.
"""

input_prompt5 = """
You are a Legal Document Classification Specialist. Analyze this document and provide:
1. Document classification and category
2. Industry-specific considerations
3. Standard vs. non-standard clauses
4. Comparison with similar document types
5. Best practices recommendations
6. Required follow-up actions
7. Storage and management recommendations

Present your analysis with clear categorization and actionable next steps.
"""

input_prompt6 = """
You are a Legal Document Analytics Expert. Analyze this document and provide key metrics and KPIs including:

1. Document Efficiency Metrics:
   - Document length and complexity score
   - Average clause length
   - Number of defined terms
   - Readability score (based on legal standards)

2. Risk and Compliance Metrics:
   - Risk exposure score (Low/Medium/High)
   - Compliance coverage percentage
   - Number of potential liability clauses
   - Number of safeguard clauses

3. Financial Implications:
   - Monetary obligations summary
   - Payment terms analysis
   - Financial risk exposure
   - Cost implications score

4. Time-Based Metrics:
   - Critical deadlines count
   - Average response time requirements
   - Renewal/termination notice periods
   - Timeline compliance score

5. Comparative Analysis:
   - Industry standard alignment score
   - Template similarity percentage
   - Deviation from standard metrics
   - Best practices alignment score

Present the analysis in a structured dashboard format with clear metrics, scores, and visual indicators where possible. Include brief explanations for each metric and any recommendations for improvement.
"""

# Add the email generation logic after the existing button handlers
if submit_email:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analysis_context, pdf_content, input_prompt_email)
        st.subheader("Summary Email for Senior Review")
        st.markdown("---")
        st.markdown(response)
        
        # Add a copy button for the email
        st.markdown("---")
        st.markdown("##### Copy Email to Clipboard")
        if st.button("Copy Email"):
            st.code(response)
            st.success("Email content copied to clipboard!")
    else:
        st.write("Please upload the legal document first")

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analysis_context, pdf_content, input_prompt1)
        st.subheader("Document Overview and Validity Analysis")
        st.write(response)
    else:
        st.write("Please upload the legal document")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analysis_context, pdf_content, input_prompt2)
        st.subheader("Risk Assessment and Compliance Analysis")
        st.write(response)
    else:
        st.write("Please upload the legal document")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analysis_context, pdf_content, input_prompt3)
        st.subheader("Contract Terms and Obligations Analysis")
        st.write(response)
    else:
        st.write("Please upload the legal document")

elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analysis_context, pdf_content, input_prompt4)
        st.subheader("Legal Language and Clarity Review")
        st.write(response)
    else:
        st.write("Please upload the legal document")

elif submit5:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analysis_context, pdf_content, input_prompt5)
        st.subheader("Document Classification and Recommendations")
        st.write(response)
    else:
        st.write("Please upload the legal document")

elif submit6:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(analysis_context, pdf_content, input_prompt6)
        st.subheader("Document KPIs and Metrics Analysis")
        st.write(response)
    else:
        st.write("Please upload the legal document")




