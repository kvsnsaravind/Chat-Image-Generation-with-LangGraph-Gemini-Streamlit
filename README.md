# Chat-Image-Generation-with-LangGraph-Gemini-Streamlit

An AI-powered Streamlit app that combines a conversational chatbot with image generation using LangGraph, Gemini, and GROQ LLMs.

# SmartGenie: AI Chat & Image Companion 🤖🎨

SmartGenie is a versatile AI-powered web application built with Streamlit that merges a context-aware chatbot and an image generator. It leverages LangGraph with GROQ's LLaMA3 model for natural conversations and integrates Gemini for dynamic image creation—all from a single interactive interface.

## 🚀 Features

- 💬 **Conversational Chatbot** using LangGraph + GROQ LLaMA3 + Tavily Search Tools
- 🖼️ **AI Image Generator** powered by Google Gemini
- 🔁 **Stateful Memory** with LangGraph’s MemorySaver
- 🌐 **Public URL** using pyngrok for local sharing
- 🔒 **Environment Variable Integration** using dotenv

---

## 🧰 Tech Stack

- **Frontend**: Streamlit
- **LLM**: [GROQ LLaMA3](https://groq.com/)
- **Image Gen**: [Google Gemini API](https://ai.google.dev/)
- **LangChain Graph**: [LangGraph](https://python.langchain.com/docs/langgraph/)
- **Search Tool**: Tavily
- **Deployment**: pyngrok (for local demo sharing)
- **Others**: dotenv, PIL

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```
git clone https://github.com/yourusername/smartgenie.git
cd smartgenie
````

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Create a `.env` File

Add your API keys in a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Run the App

```bash
streamlit run app.py
```

> On running, a public URL will be printed using `pyngrok`.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgments

* [LangChain & LangGraph](https://python.langchain.com/)
* [GROQ](https://groq.com/)
* [Google Gemini](https://ai.google.dev/)
* [Tavily](https://www.tavily.com/)
* [Streamlit](https://streamlit.io/)

---

## 🧠 Author

**Venkata Siva Naga Sai Aravind Kollipara**
*Connect with me on [LinkedIn](https://www.linkedin.com/in/aravind-kollipara/)*

