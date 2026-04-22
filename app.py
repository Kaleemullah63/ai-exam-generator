import streamlit as st
import openai

# ==============================

# PAGE CONFIG

# ==============================

st.set_page_config(
page_title="AI Exam Paper Generator",
page_icon="🧠",
layout="wide"
)

st.title("🧠 AI Assistant for Teachers")
st.subheader("📄 Exam Paper Generator")

# ==============================

# LOAD API KEY FROM SECRETS

# ==============================

openai.api_key = st.secrets["OPENAI_API_KEY"]

# ==============================

# INPUT FORM

# ==============================

st.sidebar.header("📌 Input Details")

subject = st.sidebar.text_input("Subject", "Computer Science")
topics = st.sidebar.text_area("Topics (comma separated)", "OOP, Data Structures")

difficulty = st.sidebar.selectbox(
"Difficulty Level",
["Easy", "Medium", "Hard"]
)

mcq_count = st.sidebar.slider("Number of MCQs", 1, 20, 5)
short_count = st.sidebar.slider("Short Questions", 1, 10, 3)
long_count = st.sidebar.slider("Long Questions", 1, 5, 2)

generate_btn = st.sidebar.button("🚀 Generate Exam Paper")

# ==============================

# PROMPT FUNCTION

# ==============================

def generate_prompt():
return f"""
You are an expert academic assistant and professional exam paper setter with deep knowledge of Bloom's Taxonomy.

Generate a COMPLETE exam paper.

Subject: {subject}
Topics: {topics}
Difficulty Level: {difficulty}
MCQs: {mcq_count}
Short Questions: {short_count}
Long Questions: {long_count}

INSTRUCTIONS:

* Create MCQs with 4 options and correct answer
* Add Bloom's taxonomy level
* Provide short and long answers
* Avoid repetition
* Ensure academic correctness

FORMAT:
Section A: MCQs
Section B: Short Questions
Section C: Long Questions
Answer Key

Make output clean and structured.
"""

# ==============================

# GENERATE RESPONSE

# ==============================

def get_ai_response(prompt):
try:
response = openai.ChatCompletion.create(
model="gpt-4o-mini",
messages=[
{"role": "system", "content": "You are a helpful academic assistant."},
{"role": "user", "content": prompt}
],
temperature=0.7
)

```
    return response.choices[0].message["content"]

except Exception as e:
    return f"❌ Error: {str(e)}"
```

# ==============================

# OUTPUT

# ==============================

if generate_btn:
if subject.strip() == "" or topics.strip() == "":
st.warning("⚠️ Please fill all fields")
else:
with st.spinner("⏳ Generating exam paper..."):
prompt = generate_prompt()
result = get_ai_response(prompt)

```
    st.success("✅ Exam Paper Generated!")

    st.text_area("📄 Output", result, height=600)

    st.download_button(
        label="⬇️ Download as Text File",
        data=result,
        file_name="exam_paper.txt",
        mime="text/plain"
    )
```
