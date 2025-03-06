import os
import streamlit as st
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Load environment variables
load_dotenv()
os.environ["NVIDIA_API_KEY"] = os.getenv("NVIDIA_API_KEY")

# Initialize model
llm = ChatNVIDIA(model="meta/codellama-70b")

# Page Config
st.set_page_config(page_title="AI Code Assistant", page_icon="💻", layout="wide")

# Custom CSS for better UI
def add_custom_css():
    st.markdown(
        """
        <style>
            /* General Styles */
            body { background-color: #0e0e10; color: white; }
            .stTextInput > div > div > input {
                background-color: #1a1a1d;
                color: white;
                border-radius: 8px;
                border: 1px solid #333;
                padding: 10px;
            }
            .stChatMessage, .stChatMessage div {
                background-color: #3c3f46;
                border-radius: 3px;
                padding: 3px;
            }
            .stButton > button {
                background-color: #ff4757;
                color: white;
                border-radius: 5px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()

# Title Section
st.markdown(
    """
    <h1 style='text-align: center;'>💻 AI Code Assistant</h1>
    <p style='text-align: center;'>Your smart coding companion ✨</p>
    """,
    unsafe_allow_html=True,
)

# Sidebar - Chat History
st.sidebar.header("💾 Chat History")
if "messages" not in st.session_state or st.sidebar.button("🗑️ Clear Chat History"):
    st.session_state.messages = [{"role": "assistant", "content": "Hello! How can I assist you with coding today?"}]

# Chat Messages Display
chat_container = st.container()
for msg in st.session_state.messages:
    with chat_container:
        with st.chat_message(msg["role"].lower()):
            st.write(msg["content"])

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=['chat_history', 'question'],
    template="""
    You are a helpful assistant specialized in writing code in any programming language the user wants. 
    You always provide **fully functional code** with clear explanations.You can also explain any programming-related question in a very simple and intuitive way.
    Chat History:
    {chat_history}
    User Question: {question}
    Assistant:
    """
)

# Chain
chain = LLMChain(llm=llm, prompt=prompt_template)

# User Input Section
question = st.chat_input("Type your coding question here...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with chat_container:
        with st.chat_message("user"):
            st.write(question)
    
    chat_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    
    with st.spinner("Thinking..."):
        response = chain.run(chat_history=chat_history, question=question)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    with chat_container:
        with st.chat_message("assistant"):
            st.success(response)
