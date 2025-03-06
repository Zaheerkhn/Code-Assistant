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

def add_custom_css():
    st.markdown(
        """
        <style>
            body { 
                background-color: #0e0e10; 
                color: white;
            }
            
            .stTextInput > div > div > input {
                background-color: #1a1a1d;
                color: white;
                border-radius: 8px;
                border: 1px solid #333;
                padding: 10px;
            }
            
            .stChatMessage, .stChatMessage div {
                background-color: #3c3f46;
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0;
            }
            
            .stButton > button {
                background-color: #ff4757;
                color: white;
                border-radius: 5px;
            }
            
            /* Code block styling without hover effects */
            .stCodeBlock pre {
                background-color: #1a1a1d !important;
                border-radius: 8px !important;
                border: 1px solid #333 !important;
                margin: 12px 0 !important;
                padding: 15px !important;
            }
            
            .stCodeBlock code {
                color: #f8f8f2 !important;
                font-family: 'Courier New', monospace !important;
                font-size: 14px !important;
                line-height: 1.6 !important;
            }
            
            .stCodeBlock button {
                background-color: #333 !important;
                color: white !important;
                border: 1px solid #666 !important;
                border-radius: 4px !important;
            }
            
            .stCodeBlock button:hover {
                background-color: #444 !important;
            }
            
            ::-webkit-scrollbar {
                width: 8px;
            }
            
            ::-webkit-scrollbar-track {
                background: #1a1a1d;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #3c3f46;
                border-radius: 4px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

add_custom_css()

# Title Section
st.markdown(
    """
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='margin-bottom: 10px;'>💻 AI Code Assistant</h1>
        <p style='color: #a0a0a0;'>Your smart coding companion ✨</p>
    </div>
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
            st.markdown(msg["content"])

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=['chat_history', 'question'],
    template="""
    You are an expert coding assistant that provides solutions in all programming languages.
    Always format code responses using Markdown with proper syntax highlighting:
    ```language
    // Your code here
    ```
    Provide clear explanations outside code blocks.
    
    Chat History:
    {chat_history}
    
    User Question: {question}
    
    Assistant Response:
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
            st.markdown(question)
    
    chat_history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    
    with st.spinner("🔍 Analyzing and generating solution..."):
        try:
            response = chain.run(chat_history=chat_history, question=question)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")
            response = "Sorry, I encountered an error. Please try again."
    
    with chat_container:
        with st.chat_message("assistant"):
            st.markdown(response)
