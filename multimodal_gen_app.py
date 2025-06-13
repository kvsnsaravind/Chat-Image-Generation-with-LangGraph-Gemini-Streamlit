import streamlit as st
import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

from pyngrok import ngrok
public_url = ngrok.connect(8502).public_url
print(f"Public url :  {public_url}")

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------- Setup LangGraph Chatbot ----------------
memory = MemorySaver()
llm = ChatGroq(model="llama3-8b-8192", groq_api_key=GROQ_API_KEY)
tool = TavilySearchResults(max_results=2)
tools = [tool]
llm_with_tools = llm.bind_tools(tools)

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile(checkpointer=memory)

# ---------------- Setup Gemini Image Generation ----------------
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="AI Chat & Image Generator", page_icon="🤖")
st.title("🧠 Chatbot + 🎨 Image Generator")

# Option to select feature
mode = st.radio("Choose Mode", ["💬 Chatbot", "🖼️ Image Generation"], horizontal=True)

# --- Chatbot UI ---
if mode == "💬 Chatbot":
    if "messages" not in st.session_state:
        st.session_state.messages = []

    def stream_graph_updates(user_input: str):
        assistant_response = ""
        full_context = [{"role": role, "content": msg} for role, msg in st.session_state.messages]
        full_context.append({"role": "user", "content": user_input})

        with st.spinner("Generating response..."):
            for event in graph.stream({"messages": [{"role": "user", "content": user_input}]},
                                      {"configurable": {"thread_id": "1"}, "recall": True}):
                for value in event.values():
                    assistant_response = value["messages"][-1].content
        return assistant_response

    if prompt := st.chat_input("Ask me anything..."):
        st.session_state.messages.append(("user", prompt))
        response = stream_graph_updates(prompt)
        st.session_state.messages.append(("assistant", response))

    for role, message in st.session_state.messages:
        with st.chat_message(role):
            st.markdown(message)

# --- Image Generation UI ---
elif mode == "🖼️ Image Generation":
    image_prompt = st.text_input("Enter a prompt for image generation:")

    if st.button("Generate Image"):
        if not image_prompt:
            st.warning("Please enter a prompt.")
        else:
            try:
                with st.spinner("Generating image..."):
                    response = genai_client.models.generate_content(
                        model="gemini-2.0-flash-exp-image-generation",
                        contents=image_prompt,
                        config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])
                    )

                st.subheader("Generated Output:")
                for part in response.candidates[0].content.parts:
                    if part.text:
                        st.write(part.text)
                    elif part.inline_data:
                        image = Image.open(BytesIO(part.inline_data.data))
                        st.image(image)

            except Exception as e:
                st.error(f"An error occurred while generating the image: {e}")
