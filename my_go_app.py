import streamlit as st
from src.llm_process.entity.llm_entity import LLMWrapper

# Initialize LLM
predictor = LLMWrapper()

# App Configuration
st.set_page_config(page_title="MYGO LLM Chat", page_icon="💬", layout="centered")
st.title("🤖 MYGO LLM Chat")
st.markdown("**欢迎来到 MYGO LLM! 来聊天并探索我的能力吧。**")

# Initialize Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar Instructions in Chinese
st.sidebar.title("关于这个应用")
st.sidebar.markdown(
    """
    本应用让你与 MYGO LLM 模型进行互动。
    - 在下方输入你的消息开始聊天。
    - 机器人会回复你 MYGO中的场景。
    """
)
st.sidebar.write("Made by [Quik Zi Hao](https://github.com/QuikZiHao/mygo_llm)")

# Chat Interface
st.subheader("💬 Chat")
chat_container = st.container()

# Input Section
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Your Message:", placeholder="Type something...")
    submitted = st.form_submit_button("Send")

# Process Input and Generate Response
if submitted and user_input.strip():
    with st.spinner("🤔 Thinking..."):
        try:
            response_text, response = predictor.speak(user_input)  

            # Append user message and model response to chat history
            st.session_state.chat_history.append({"sender": "user", "message": user_input})
            
            if hasattr(response, "show"):  # If response is a PIL image
                st.session_state.chat_history.append({"sender": "bot", "message": response_text, "image": response})
            elif isinstance(response, str):  # Text response
                st.session_state.chat_history.append({"sender": "bot", "message": response})
        except Exception as e:
            st.session_state.chat_history.append({"sender": "bot", "message": f"❌ An error occurred: {e}"})

# Display Chat History
for entry in st.session_state.chat_history:
    if entry["sender"] == "user":
        with chat_container:
            st.markdown(f"**👨‍🦰:** {entry['message']}")
    elif entry["sender"] == "bot":
        with chat_container:
            st.markdown(f"**🤖:**")
            if "image" in entry:  # Display image if it exists
                st.image(entry["image"], caption=entry["message"])

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** The LLM is capable of generating creative outputs. Experiment with different inputs!")
