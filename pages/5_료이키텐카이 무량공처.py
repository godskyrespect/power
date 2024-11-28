import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi

st.set_page_config(page_title='료이키 텐카이', page_icon='♨️')
# MongoDB 연결 준비
uri = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['recommendations_db']
collection = db['recommendations']

documents = list(collection.find({}))
st.markdown("""
    <style>
    h3 {
        color: teal;
        font-size: 36px;
    }
    </style>
""", unsafe_allow_html=True)

def show_recommendations(select):
    st.subheader(f'"{select}"')    
    text = select.replace("🎓", "")
    recommendations = next((item["recommend_reason"] for item in documents if item["_id"] == text), None)
    st.write(recommendations)
           
st.title('우리 학교 수업')
search_query = st.text_input('검색할 내용을 입력하세요:', placeholder='수업명을 입력하세요')
st.write('여기는 우리 학교 수업 페이지입니다.')
st.divider()

st.header('울학교 선배님들의 추천 ✨')
st.caption('GPT-4o 활용 추천',
    help='인공지능 GPT-4o로 기존의 리뷰의 일부를 분석해 수업을 추천합니다.')

rec = list(collection.find({}, {'_id' : 0, 'recommend_text': 1}))
text = [item["recommend_text"] for item in rec]
text = [f'🎓{txt}' for txt in text]
selection = st.pills(f'수업 추천 키워드', text, selection_mode='single')

if selection:
    with st.container(border=True):
     show_recommendations(selection)          


