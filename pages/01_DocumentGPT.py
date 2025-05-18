import time
import streamlit as st

st.title("DocumentGPT")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.write(st.session_state["messages"])

def send_message(message, role):
    with st.chat_message(role):
        st.write(message)
        st.session_state["message"].append({"message": message, "role": role})
    
message = st.chat_input("Send a message to the DocumentGPT")

if message:
    send_message(message, "human")
    time.sleep(2)
    send_message(f"You said {message}", "ai")