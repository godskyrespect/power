import json
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from openai import OpenAI
import streamlit as st 
import config

# OpenAI 연결 설정 ====================================
client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

# 학과정보 파일 로드 ===================================
file_path = './text.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 검색으로 사용할 내용 추출 =============================
doc_list = [item['학과소개'] for item in data]

## 1. FAISS를 이용한 질의와 유사한 내용을 벡터 검색하는 함수(get:검색할 내용, return: 검색된 faiss문서)
def search(query):
    embedding = OpenAIEmbeddings(api_key=st.secrets.OPENAI_API_KEY)
    faiss_vectorstore = FAISS.from_texts(
        doc_list, embedding, metadatas=[{"source": i} for i in range(len(doc_list))]
    )
    faiss_retriever = faiss_vectorstore.as_retriever(search_kwargs={"k":3})

    faiss_docs = faiss_retriever.invoke(query)

    return faiss_docs

## 2. 프롬프트에 따른 LLM결과 출력하는 함수(get: 프롬프트, return: streamlit에 맞는 대답)
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

## 3. 부적절한 표현이 있으면 1을 출력하는 함수(get: 질문, return: 부적절한표현인 경우 1)
def slang_detector(query):
    messages = [{
        "role": "system",
        "content": "당신은 사용자가 욕설, 성적인 표현, 인종차별발언, 등 적절하지 않은 표현이 있는지 확인해야 합니다. 만약 해당 표현이 있다면 1이라고 대답하세요."
    },{
        "role": "user",
        "content": query
    }
    ]
    response = client.chat.completions.create(model=st.session_state["openai_model"], messages=messages)
    answer = response.choices[0].message.content
    if answer == '1':
        return 1

## 4. 질문과 검색된 내용으로 프롬프트를 작성하는 함수(get: 질문, docs: 학과정보문서, return: 프롬프트)
def prompt_generator(query, docs):
    prompt = f"""
    당신은 고등학교 학생들의 진로설계를 도와주는 친절한 어시스턴트 입니다. 
    당신이 해야 할 일은 사용자가 자신의 꿈이나 진로와 관련된 질문을 하면 질문을 기반으로 한 검색된 자료를 모두 인용하여 답변을 생성해야 합니다.
    Step1의 조건을 확인하고 Step2를 수행하세요.
    Step1: 만약 질문에 욕, 성적인 표현, 차별적인 발언, 학과 추천과 관련없는 질문(ex. 나 예뻐?)이 포함되어 있다면 해당 내용에 대해 답변을 할 수 없다고 하세요.
    질문이 단어로 되어 있거나 2개의 단어 이하의 문장으로 되어있다면 너무 짧아서 잘 모르겠다 라고 답변하세요.
    질문 : {query}

    Step2: 검색된 자료에는 다음과 같은 내용이 있습니다. : 학과이름, 학과소개, 학과주요교과목, 학과관련 고등학교 선택과목, 학과관련 추천 도서
    학과를 알려줄 때는 아래에 있는 문서 내용을 고등학생에게 소개하는 방식으로 설명해 주세요.
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

## Streamlit 사이트 코드 ============================
st.info("이 페이지에서는 AI한테 내가 원하는 대학교 학과에 대해서만 물어볼 수 있어요!", icon="🎅")
st.title("🤖 진로 설계 도우미")
col1, col2 = st.columns([8, 2])
with col1:
    st.markdown("도우미 AI(가칭)은 실수를 할 수 있습니다. 중요한 정보는 선생님과 같이 확인하세요.")
    st.write("**질문 예시** : OO학과에 대한 정보를 자세하게 알려줘.")

with col2:
    if st.button("대화 지우기"):
        st.session_state.messages.clear()
        st.rerun()

# 1. 생성형AI 모델 불러오기
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

# 2. 대화를 지속하기 위한 LIST생성하기
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. 역할에 맞는 메시지창 표시하기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])   

# 4. 입력창을 만들고 검색기능 구현하기
if prompt := st.chat_input('무엇을 도와드릴까요?'):
    with st.chat_message('user'):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 부적절한 표현에 대한 경고 메시지
    if slang_detector(prompt) == 1:
        st.toast('적절하지 못한 표현은 자제하세요.', icon='🚨')

    # FAISS 검색기를 이용한 문서 내용
    retrived = [doc for doc in search(prompt)]

    #질문에 대한 ASSISTANT에 대한 응답
    with st.chat_message('assistant'):
        answer = prompt_generator(prompt, retrived)
        response = st.write_stream(answer)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    
