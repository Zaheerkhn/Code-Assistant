# AI Code Assistant

## 🚀 Overview

AI Code Assistant is a powerful AI-driven coding companion that helps developers by providing code suggestions, explanations, and answers to programming-related queries. Built using **Streamlit** and **NVIDIA AI Endpoints**, this assistant leverages **Meta's CodeLlama-70B** model to deliver intelligent coding assistance.

## 🎯 Features

-  **AI-Powered Code Assistance**: Get precise answers to coding questions.
-  **Interactive Chat Interface**: Engage with the assistant through a simple chat-based UI.
-  **Custom Theming**: Dark mode UI with a modern, developer-friendly design.
-  **Chat History**: Keep track of previous interactions and clear history when needed.
-  **Context-Aware Responses**: The assistant remembers previous messages in a session to provide better answers.

## 🏗️ Technologies Used

- **Python** 
- **Streamlit**  (Frontend UI)
- **LangChain**  (Prompt Engineering & LLM Handling)
- **NVIDIA NIM**  (LLM Model)
- **dotenv**  (Environment Variable Management)

## 📦 Installation

To set up and run the project locally, follow these steps:

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Zaheerkhn/Code-Assistant
cd ai-code-assistant
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the project directory and add:

```env
NVIDIA_API_KEY=your_nvidia_api_key_here
```

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

## 📌 Usage

1. Open the app in your browser.
2. Enter your coding question in the chat input.
3. Receive AI-generated responses tailored to your query.
4. View chat history in the sidebar.

## 🛠️ Customization

- Modify **CSS Styling** inside `add_custom_css()` function to change UI elements.
- Adjust **Prompt Engineering** inside `PromptTemplate` to refine AI responses.
- Integrate additional **LLM models** for broader AI capabilities.

## 📜 License

This project is licensed under the **Apache License 2.0**.

---

🎉 **Happy Coding!** 🎉

