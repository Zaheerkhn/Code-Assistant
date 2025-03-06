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
st.set_page_config(
    page_title="Code Assistant",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for improved UI
st.markdown("""
<style>
    /* Main container styling */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        background-color: #1a1d23;
    }
    
    /* User input styling */
    .stTextInput input {
        background-color: #1a1d23 !important;
        color: white !important;
        border-radius: 8px;
        padding: 12px;
        border: 1px solid #2d333b !important;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: #161b22 !important;
        border-right: 1px solid #2d333b;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #238636;
        color: white;
        border-radius: 6px;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #2ea043;
        transform: scale(1.02);
    }
    
    /* Code block styling */
    pre {
        background-color: #161b22 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        border: 1px solid #2d333b !important;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0e1117;
    }
    ::-webkit-scrollbar-thumb {
        background: #2d333b;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("""
<div style="text-align: center; padding: 2rem 0;">
    <h1 style="margin-bottom: 0.5rem;">💻 Code Assistant</h1>
    <p style="color: #848d97;">Your AI-powered coding companion</p>
</div>
""", unsafe_allow_html=True)

# Prompt template with chat history
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

prompt = PromptTemplate(input_variables=['chat_history', 'question'], template=prompt_template)

# Chain
chain = LLMChain(llm=llm, prompt=prompt)

# Chat History Management
st.sidebar.header("💾 Chat History")
if "messages" not in st.session_state or st.sidebar.button("🗑️ Clear History", type="primary"):
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Hello! I can solve any coding problem for you. What would you like me to work on today?"
    }]

# Display Chat Messages
chat_container = st.container()
with chat_container:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"].lower()):
            st.markdown(msg["content"])  # Changed to markdown for better formatting

# User Input Handling
question = st.chat_input("Ask your coding question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    
    with chat_container:
        with st.chat_message("user"):
            st.markdown(question)  # Changed to markdown for consistency
    
    # Prepare chat history
    chat_history = "\n".join(
        f"{msg['role'].capitalize()}: {msg['content']}" 
        for msg in st.session_state.messages
    )
    
    # Generate response with error handling
      with st.spinner("Generating professional response..."):
            response = chain.run(chat_history=chat_history, question=question)
            st.session_state.messages.append({"role": "assistant", "content": response})
    
      with st.chat_message("assistant"):
            st.markdown(response)  # Changed from st.write to st.markdown
