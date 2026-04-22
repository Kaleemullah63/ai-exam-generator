import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Exam Generator", layout="wide")

st.title("AI Exam Assistant for Teachers")
st.subheader("Automated Exam Paper Generator using AI")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.sidebar.header("Input Details")

subject = st.sidebar.text_input("Subject", "Computer Science")
topics = st.sidebar.text_area("Topics (comma separated)", "OOP, Data Structures, DBMS")

difficulty = st.sidebar.selectbox("Difficulty Level", ["Easy", "Medium", "Hard"])

mcq_count = st.sidebar.slider("Number of MCQs", 1, 20, 5)
short_count = st.sidebar.slider("Number of Short Questions", 1, 10, 3)
long_count = st.sidebar.slider("Number of Long Questions", 1, 5, 2)

def build_prompt():
    return (
        "You are an expert academic exam paper generator.\n\n"
        "Generate a complete exam paper with the following requirements:\n\n"
        "Subject: " + subject + "\n"
        "Topics: " + topics + "\n"
        "Difficulty Level: " + difficulty + "\n\n"
        "Instructions:\n"
        "- Generate MCQs with 4 options and correct answer\n"
        "- Add Bloom's Taxonomy level for each question\n"
        "- Generate short questions with answers\n"
        "- Generate long questions with detailed answers\n"
        "- Ensure academic correctness and no repetition\n\n"
        "Structure Output:\n"
        "Section A: MCQs\n"
        "Section B: Short Questions\n"
        "Section C: Long Questions\n"
        "Answer Key"
    )

def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

if st.sidebar.button("Generate Exam Paper"):

    if subject.strip() == "" or topics.strip() == "":
        st.warning("Please fill all required fields")

    else:
        with st.spinner("Generating exam paper..."):
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
