import streamlit as st

def content():
    st.title("Welcome To Whatsapp chat Analyzer")
    st.write("Steps to use Application : ")
    st.write("Firstly you need to export your chat (Individual/Group)")
    st.write("1. open the chat")
    st.write("2. Tap More option")
    st.write("3. Tap on 'Without Media' (will bring more support soon for with media)")
    st.header("Please make sure that your whatsapp have 12-hour time format (We'll bring 24-hour time format support soon)")

    st.image("Images/guide_to_export_chat.jpg", caption="How to export chat")

