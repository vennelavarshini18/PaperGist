from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import load_prompt
import re

load_dotenv()

st.set_page_config(page_title="Research Tool", page_icon="📘", layout="centered")

st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(135deg, #f9f9f9, #ffffff);
            padding: 20px;
            border-radius: 12px;
        }
        .stButton>button {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border-radius: 12px;
            height: 3em;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📘 Research Summarization Tool")
st.markdown("Generate structured, clear, and insightful research paper summaries.")

paper_input = st.text_input("🔎 Enter Research Paper Name or Topic")

col1, col2 = st.columns(2)
with col1:
    style_input = st.selectbox(
        "📝 Explanation Style",
        ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"]
    )
with col2:
    length_input = st.selectbox(
        "📏 Explanation Length",
        ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"]
    )

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.3
)

template = load_prompt('template.json')

def html_to_latex(text: str) -> str:
    text = re.sub(r"<sup>(.*?)</sup>", r"^{\1}", text)
    text = re.sub(r"<sub>(.*?)</sub>", r"_{\1}", text)
    text = text.replace("√", r"\sqrt{}")
    return text

def render_with_math(text):
    if "$" in text:
        parts = re.split(r"(\$\$.*?\$\$|\$.*?\$)", text)
        for part in parts:
            if part.startswith("$$") and part.endswith("$$"):
                st.latex(part[2:-2])
            elif part.startswith("$") and part.endswith("$"):
                st.latex(part[1:-1])
            else:
                st.markdown(part)
    else:
        converted = html_to_latex(text)
        st.markdown(converted)

if st.button("✨ Summarize Research Paper"):
    chain = template | model
    result = chain.invoke({
        'paper_input': paper_input,
        'style_input': style_input,
        'length_input': length_input
    })
    st.markdown("### 📄 Summary")
    render_with_math(result.content)