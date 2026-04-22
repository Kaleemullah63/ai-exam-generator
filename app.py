import streamlit as st
from groq import Groq

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI Exam Generator", layout="wide")

st.title("🧠 AI Exam Assistant for Teachers")
st.subheader("Automated Exam Paper Generator using Groq AI")

# -----------------------------
# GROQ CLIENT
# -----------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -----------------------------
# SIDEBAR INPUTS
# -----------------------------
st.sidebar.header("Exam Settings")

subject = st.sidebar.text_input("Subject", "Computer Science")
topics = st.sidebar.text_area("Topics (comma separated)", "OOP, DBMS, Data Structures")

difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

mcq_count = st.sidebar.slider("Number of MCQs", 1, 20, 5)
short_count = st.sidebar.slider("Number of Short Questions", 1, 10, 3)
long_count = st.sidebar.slider("Number of Long Questions", 1, 5, 2)

# -----------------------------
# PROMPT BUILDER (NO * OUTPUT)
# -----------------------------
def build_prompt():
    return (
        "You are an expert academic exam paper generator.\n\n"
        "Generate a complete exam paper in plain text ONLY.\n\n"
        "CRITICAL FORMATTING RULES:\n"
        "- Do NOT use asterisks (*)\n"
        "- Do NOT use bullet points\n"
        "- Do NOT use markdown\n"
        "- Use numbered format only\n\n"
        f"Subject: {subject}\n"
        f"Topics: {topics}\n"
        f"Difficulty Level: {difficulty}\n\n"
        f"MCQs: {mcq_count}\n"
        f"Short Questions: {short_count}\n"
        f"Long Questions: {long_count}\n\n"
        "STRUCTURE:\n"
        "Section A: Multiple Choice Questions (MCQs)\n"
        "Section B: Short Questions\n"
        "Section C: Long Questions\n"
        "Answer Key\n\n"
        "MCQ FORMAT EXAMPLE:\n"
        "1. Question text\n"
        "A. option\n"
        "B. option\n"
        "C. option\n"
        "D. option\n"
        "Correct Answer: B\n"
    )

# -----------------------------
# GROQ API CALL
# -----------------------------
def generate_exam(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# -----------------------------
# MAIN EXECUTION
# -----------------------------
if st.sidebar.button("Generate Exam Paper"):

    if subject.strip() == "" or topics.strip() == "":
        st.warning("Please fill all required fields in sidebar")

    else:
        with st.spinner("Generating exam paper using AI..."):

            prompt = build_prompt()
            result = generate_exam(prompt)

        st.success("Exam Paper Generated Successfully")

        st.text_area("Generated Exam Paper", result, height=600)

        st.download_button(
            label="Download Exam Paper",
            data=result,
            file_name="exam_paper.txt",
            mime="text/plain"
        )
