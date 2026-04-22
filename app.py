import streamlit as st
from openai import OpenAI

# ==============================

# SETUP

# ==============================

st.set_page_config(page_title="AI Exam Generator", layout="wide")

st.title("🧠 AI Assistant for Teachers")
st.subheader("📄 Exam Paper Generator")

# Load API Key

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

# PROMPT FUNCTION (NO ERROR VERSION)

# ==============================

def generate_prompt():
prompt = "You are an expert exam paper generator.\n\n"
prompt += f"Subject: {subject}\n"
prompt += f"Topics: {topics}\n"
prompt += f"Difficulty: {difficulty}\n"
prompt += f"MCQs: {mcq_count}\n"
prompt += f"Short Questions: {short_count}\n"
prompt += f"Long Questions: {long_count}\n\n"

```
prompt += "Create:\n"
prompt += "1. MCQs with 4 options and correct answer + Bloom level\n"
prompt += "2. Short questions with answers + Bloom level\n"
prompt += "3. Long questions with detailed answers + Bloom level\n\n"

prompt += "Format:\n"
prompt += "Section A: MCQs\n"
prompt += "Section B: Short Questions\n"
prompt += "Section C: Long Questions\n"
prompt += "Answer Key\n"

return prompt
```

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

```
except Exception as e:
    return f"Error: {e}"
```

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

    st.download_button(
        "Download",
        result,
        file_name="exam.txt"
    )
```
