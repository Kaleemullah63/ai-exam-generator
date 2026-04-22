import streamlit as st
from openai import OpenAI

# Page setup

st.set_page_config(page_title="AI Exam Generator")

st.title("AI Exam Paper Generator")

# Load API key

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Inputs

subject = st.text_input("Enter Subject")
topics = st.text_input("Enter Topics")

# Button

if st.button("Generate Exam Paper"):

```
# Create prompt
prompt = "Generate an exam paper for subject: " + subject + " with topics: " + topics

try:
    # API call
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    st.success("Exam Generated Successfully")
    st.write(result)

except Exception as e:
    st.error("Error: " + str(e))
```
