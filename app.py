import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Exam Generator", layout="wide")

st.title("🧠 AI Exam Assistant for Teachers")
st.subheader("Automated Exam Paper Generator using AI")

# ------------------------------
# API KEY
# ------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ------------------------------
# INPUTS
# ------------------------------
st.sidebar.header("Exam Settings")

subject = st.sidebar.text_input("Subject", "Computer Science")
topics = st.sidebar.text_area("Topics (comma separated)", "OOP, DBMS, Data Structures")

difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

mcq_count = st.sidebar.slider("MCQs", 1, 20, 5)
short_count = st.sidebar.slider("Short Questions", 1, 10, 3)
long_count = st.sidebar.slider("Long Questions", 1, 5, 2)

# ------------------------------
# PROMPT BUILDER
# ------------------------------
def build_prompt():
    return (
        "You are an expert exam paper generator.\n\n"
        "Generate a complete exam paper.\n\n"
        f"Subject: {subject}\n"
        f"Topics: {topics}\n"
        f"Difficulty Level: {difficulty}\n\n"
        f"MCQs: {mcq_count}\n"
        f"Short Questions: {short_count}\n"
        f"Long Questions: {long_count}\n\n"
        "Requirements:\n"
        "- MCQs must have 4 options with correct answer\n"
        "- Include Bloom's Taxonomy level for each question\n"
        "- Short questions must include answers\n"
        "- Long questions must include detailed answers\n\n"
        "Format:\n"
        "Section A: MCQs\n"
        "Section B: Short Questions\n"
        "Section C: Long Questions\n"
        "Answer Key"
    )

# ------------------------------
# API CALL
# ------------------------------
def get_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"

# ------------------------------
# GENERATE BUTTON
# ------------------------------
if st.sidebar.button("Generate Exam Paper"):

    if subject.strip() == "" or topics.strip() == "":
        st.warning("Please fill in Subject and Topics")

    else:
        with st.spinner("Generating exam paper... please wait"):

            prompt = build_prompt()
            result = get_response(prompt)

        st.success("Exam Paper Generated Successfully")

        st.text_area("Generated Paper", result, height=600)

        st.download_button(
            label="Download Exam Paper",
            data=result,
            file_name="exam_paper.txt",
            mime="text/plain"
        )
