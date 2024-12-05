import json
from langchain_community.retrievers import BM25Retriever
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import streamlit as st 
import random
import time
import config


client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

file_path = './text.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

doc_list = [item['학과소개'] for item in data]
    
def search(query):
    # bm25_retriever = BM25Retriever.from_texts(
    #     doc_list, metadatas=[{"source": 1}]*len(doc_list)
    # )
    # bm25_retriever.k = 3


    embedding = OpenAIEmbeddings(api_key=st.secrets.OPENAI_API_KEY)
    faiss_vectorstore = FAISS.from_texts(
        doc_list, embedding, metadatas=[{"source": i} for i in range(len(doc_list))]
    )
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k":3})

    # bm25_docs = bm25_retriever.invoke(query)
    faiss_docs = faiss_retriever.invoke(query)

    # print(bm25_docs)
    return faiss_docs

def chatgpt_generate(query):
    
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    },{
        "role": "user",
        "content": query
    }]
    response = client.chat.completions.create(model=st.session_state["openai_model"], messages=messages, stream=True)
    return response


def prompt_generator(query, docs):
    prompt = f"""
    당신은 고등학교 학생들의 진로설계를 도와주는 친절한 어시스턴트 입니다.
    당신이 해야 할 일은 사용자가 자신의 꿈이나 진로와 관련된 질문을 하면 질문을 기반으로 한 검색된 자료를 참고하여 답변을 생성해야 합니다.
    만약 질문에 욕, 성적인 표현, 차별적인 발언, 학과 추천과 관련없는 질문(ex. 나 예뻐?)이 포함되어 있다면 해당 내용에 대해 답변을 할 수 없다고 하세요.

    질문 : {query}
    검색된 자료에는 다음과 같은 내용이 있습니다. : 학과이름, 학과소개, 학과주요교과목, 학과관련 고등학교 선택과목, 학과관련 추천 도서
    
    아래에 있는 문서 내용을 바탕으로 학과에 대해서 고등학생에게 소개하는 방식으로 설명해 주세요.
    """
    for i in range(len(docs)):
        idx = docs[i].metadata['source']
        prompt += f"{data[idx]['학과명']}\n"
        prompt += f"학과 소개: {docs[i].page_content}\n"
        prompt += f"학과 관련 정보: {data[idx]['학과 관련 정보']}\n"
        prompt += f"고등학교 선택 과목: {data[idx]['학과 관련 고등학교 선택 과목']}\n"
        prompt += f"추천도서: {data[idx]['학과 관련 도서 추천']}\n"
        prompt += "\n"
        
    answer = chatgpt_generate(prompt)
    return answer

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



st.title("🤖 진로 설계 도우미")
st.write("도우미 AI(가칭)은 실수를 할 수 있습니다. 중요한 정보는 선생님과 같이 확인하세요.")

col1, col2 = st.columns([9, 1])
with col1:
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
        
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])   
with col2:
    if st.button("방귀"):
        st.session_state.messages.clear()

if prompt := st.chat_input('무엇을 도와드릴까요?'):
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    retrived = [doc for doc in search(prompt)]
    with st.chat_message('assistant'):
        answer = prompt_generator(prompt, retrived)
        response = st.write_stream(answer)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    
