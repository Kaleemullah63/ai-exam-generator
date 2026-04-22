import streamlit as st
from groq import Groq
from fpdf import FPDF

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Exam Generator", layout="wide")

st.title("🧠 AI Exam Assistant for Teachers")
st.subheader("Professional Exam Paper Generator (AI Powered)")

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------
# INPUT PANEL
# -----------------------------
st.sidebar.header("Exam Configuration")

subject = st.sidebar.text_input("Subject", "Computer Science")
topics = st.sidebar.text_area("Topics", "OOP, DBMS, Data Structures")
difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

mcq_count = st.sidebar.slider("MCQs", 1, 20, 5)
short_count = st.sidebar.slider("Short Questions", 1, 10, 3)
long_count = st.sidebar.slider("Long Questions", 1, 5, 2)

# -----------------------------
# PROMPT
# -----------------------------
def build_prompt():
    return f"""
You are an expert academic examiner.

Generate a complete exam paper in STRICT plain text format.

Subject: {subject}
Topics: {topics}
Difficulty: {difficulty}

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
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# -----------------------------
# PDF GENERATOR
# -----------------------------
def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for line in text.split("\n"):
        pdf.cell(200, 6, txt=line[:100], ln=True)

    pdf_output = "exam_paper.pdf"
    pdf.output(pdf_output)
    return pdf_output

# -----------------------------
# GENERATE BUTTON
# -----------------------------
if st.sidebar.button("Generate Exam Paper"):

    if subject.strip() == "" or topics.strip() == "":
        st.warning("Please fill all fields")

    else:
        with st.spinner("Generating exam paper..."):

            prompt = build_prompt()
            result = generate_exam(prompt)

        st.success("Exam Generated Successfully")

        st.text_area("Generated Paper", result, height=500)

        # -------------------------
        # DOWNLOAD TXT
        # -------------------------
        st.download_button(
            "Download TXT",
            result,
            file_name="exam.txt"
        )

        # -------------------------
        # DOWNLOAD PDF
        # -------------------------
        pdf_file = create_pdf(result)

        with open(pdf_file, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name="exam.pdf"
            )
