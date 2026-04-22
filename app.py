import streamlit as st
from openai import OpenAI

# ==============================

# CONFIG

# ==============================

st.set_page_config(page_title="AI Exam Generator", layout="wide")

st.title("🧠 AI Exam Paper Generator")

# ==============================

# API KEY

# ==============================

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# ==============================

# INPUTS

# ==============================

st.sidebar.header("Input Details")

subject = st.sidebar.text_input("Subject", "Computer Science")
topics = st.sidebar.text_area("Topics", "OOP, Data Structures")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

mcq_count = st.sidebar.slider("MCQs", 1, 20, 5)
short_count = st.sidebar.slider("Short Questions", 1, 10, 3)
long_count = st.sidebar.slider("Long Questions", 1, 5, 2)

generate = st.sidebar.button("Generate Paper")

# ==============================

# FUNCTION

# ==============================

def generate_prompt():
return (
"You are an expert exam paper generator.\n\n"
f"Subject: {subject}\n"
f"Topics: {topics}\n"
f"Difficulty: {difficulty}\n"
f"MCQs: {mcq_count}\n"
f"Short Questions: {short_count}\n"
f"Long Questions: {long_count}\n\n"
"Create:\n"
"1. MCQs with 4 options + correct answer + Bloom level\n"
"2. Short questions with answers + Bloom level\n"
"3. Long questions with detailed answers + Bloom level\n\n"
"Format:\n"
"Section A: MCQs\n"
"Section B: Short Questions\n"
"Section C: Long Questions\n"
"Answer Key\n"
)

# ==============================

# API CALL

# ==============================

def get_response(prompt):
try:
response = client.chat.completions.create(
model="gpt-4o-mini",
messages=[
{"role": "user", "content": prompt}
],
temperature=0.7
)
return response.choices[0].message.content
except Exception as e:
return f"Error: {e}"

# ==============================

# OUTPUT

# ==============================

if generate:
if subject.strip() == "" or topics.strip() == "":
st.warning("Please fill all fields")
else:
with st.spinner("Generating..."):
prompt = generate_prompt()
result = get_response(prompt)

```
    st.success("Exam Paper Generated")
    st.text_area("Output", result, height=500)

    st.download_button("Download", result, file_name="exam.txt")
```
