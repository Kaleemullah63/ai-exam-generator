import streamlit as st
from groq import Groq
from fpdf import FPDF
import PyPDF2
import tempfile

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Exam Generator",
    layout="wide",
    page_icon="🧠"
)

# -----------------------------
# CUSTOM CSS (Professional UI)
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
h1 {
    color: #2c3e50;
}
.sidebar .sidebar-content {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 AI Exam Assistant for Teachers")
st.caption("Generate Smart Exam Papers using AI + Your Course Material")

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------
# SIDEBAR CONFIG
# -----------------------------
st.sidebar.header("📘 Exam Configuration")

subject = st.sidebar.text_input("Subject", "Computer Science")
topics = st.sidebar.text_area("Topics", "OOP, DBMS, Data Structures")
difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

st.sidebar.markdown("---")

mcq_count = st.sidebar.slider("MCQs", 1, 20, 5)
short_count = st.sidebar.slider("Short Questions", 1, 10, 3)
long_count = st.sidebar.slider("Long Questions", 1, 5, 2)

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader("📄 Upload Course PDF", type=["pdf"])

# -----------------------------
# PDF TEXT EXTRACTION
# -----------------------------
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text[:4000]  # limit for token safety

# -----------------------------
# PROMPT BUILDER
# -----------------------------
def build_prompt(context_text=""):
    return f"""
You are an expert academic examiner.

Generate a complete exam paper in STRICT plain text format.

Subject: {subject}
Topics: {topics}
Difficulty: {difficulty}

Use the following study material (if provided):
{context_text}

MCQs: {mcq_count}
Short Questions: {short_count}
Long Questions: {long_count}

RULES:
- No asterisks (*)
- No bullet points
- No markdown
- Use numbered format only

FORMAT:
Section A: MCQs
Section B: Short Questions
Section C: Long Questions
Answer Key

Each MCQ must include:
1. Question
A. Option
B. Option
C. Option
D. Option
Correct Answer: X
"""

# -----------------------------
# GROQ CALL
# -----------------------------
def generate_exam(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------
# PDF GENERATOR (IMPROVED)
# -----------------------------
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=10)

    for line in text.split("\n"):
        pdf.multi_cell(0, 6, txt=line)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name

# -----------------------------
# MAIN TABS
# -----------------------------
tab1, tab2 = st.tabs(["📄 Generate Exam", "ℹ️ About"])

# -----------------------------
# TAB 1: GENERATION
# -----------------------------
with tab1:

    st.subheader("Generate Exam Paper")

    if st.button("🚀 Generate Exam Paper"):

        if subject.strip() == "" or topics.strip() == "":
            st.warning("Please fill all required fields")

        else:
            with st.spinner("Analyzing and generating exam..."):

                context = ""
                if uploaded_file:
                    context = extract_text_from_pdf(uploaded_file)

                prompt = build_prompt(context)
                result = generate_exam(prompt)

            st.success("✅ Exam Generated Successfully")

            st.text_area("Generated Paper", result, height=500)

            col1, col2 = st.columns(2)

            # TXT Download
            with col1:
                st.download_button(
                    "📥 Download TXT",
                    result,
                    file_name="exam.txt"
                )

            # PDF Download
            with col2:
                pdf_file = create_pdf(result)
                with open(pdf_file, "rb") as f:
                    st.download_button(
                        "📄 Download PDF",
                        f,
                        file_name="exam.pdf"
                    )

# -----------------------------
# TAB 2: ABOUT
# -----------------------------
with tab2:
    st.markdown("""
    ### 🎯 About This Project
    
    This AI-powered system helps teachers automatically generate exam papers.
    
    ### ✨ Features:
    - AI-generated MCQs, Short & Long Questions
    - Difficulty-based generation
    - PDF upload (context-aware exams)
    - Export to TXT & PDF
    
    ### 🤖 AI Model:
    - LLaMA 3 via Groq API
    
    ### 🚀 Future Improvements:
    - Urdu language support
    - Question validation
    - LMS integration
    """)
