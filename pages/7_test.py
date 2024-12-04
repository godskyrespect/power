import streamlit as st 
import random
import time
from openai import OpenAI

# # st.chat_message 메시지 형태 띄우기  user: 사용자, assistant: GPT
# with st.chat_message("user"):
#     st.write("안녕하세여~")
    
# with st.chat_message("assistant"):
#     st.write("인간시대의 끝이 도래했다")
    
# # 채팅 입력기 만들기
# prompt = st.chat_input("아무거나 물어보세요.")
# if prompt:
#     with st.chat_message("user"):
#         st.write(f'{prompt}')

# def response_generator():
#     response = "hello my name is chatgpt clone"
#     for word in response.split():
#         yield word + " "
#         time.sleep(0.05)
        
    
# # 채팅 히스토리 초기화하기
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message['role']):
#         st.markdown(message['content'])
        
# # := 할당하고 값을 반환함., 사용자가 입력하고 화면에 기억하는 코드
# if prompt := st.chat_input("무엇을 도와드릴까요?"):
#     with st.chat_message('user'):
#         st.markdown(prompt)
#     st.session_state.messages.append({"role": "user", "content": prompt})
    
# #chatgpt를 통해서 나온 대답을 받습니다.
# response = f"Echo: {prompt}"

# # 챗봇 답변을 작성해 줍니다. 
# with st.chat_message("assistant"):
#     response = st.write_stream(response_generator())
# st.session_state.messages.append({"role": "assistant", "content": response})
key = st.text_input("Movie title", "Life of Brian")
st.title("🦾 CHATGPT 4o mini 따라함. 돈나가니깐 적당히 쓰세요.")
api_key = key

client = OpenAI(api_key=api_key)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
if prompt := st.chat_input('무엇을 도와드릴까요?'):
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message('assistant'):
        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = [{"role": m['role'], "content": m['content']} for m in st.session_state.messages],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
