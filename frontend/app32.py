import streamlit as st 
from api_client import stream_chat

message = st.text_input("메시지를 입력하세요.")
if st.button("전송") and message:
    collected = ""
    for token in stream_chat(message):
        collected += token
    
    st.markdown(collected) 
    
    