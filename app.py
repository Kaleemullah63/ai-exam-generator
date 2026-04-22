import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI Exam Generator")

st.title("AI Exam Generator")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

subject = st.text_input("Subject")
topics = st.text_input("Topics")

if st.button("Generate"):

```
prompt = "Generate exam paper for subject: " + subject + " topics: " + topics

try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    result = response.choices[0].message.content
    st.write(result)

except Exception as e:
    st.write("Error:", e)
```
