import streamlit as st
import os
import urllib.parse
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi


# MongoDB 연결 준비
username = urllib.parse.quote_plus(os.environ['MONGODB_USERNAME'])
password = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])
uri = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client['recommendations_db']
collection = db['recommendations']

review_data = list[collection.find({})]

# 사이드바를 통해 페이지 선택
def main():
    st.sidebar.title('Navigation')
    page = st.sidebar.selectbox('Go to', ['메인 페이지', '우리 학교 수업'])

    if page == '메인 페이지':
        show_main_page()
    elif page == '우리 학교 수업':
        show_school_classes_page()

# 메인 페이지 함수
def show_main_page():
    st.title('메인 페이지')
    st.header('헤더')
    st.write('여기는 메인 페이지의 샘플 콘텐츠입니다.')

# 우리 학교 수업 페이지 함수
def show_school_classes_page():
    st.title('우리 학교 수업')
    search_query = st.text_input('검색할 내용을 입력하세요:', placeholder='수업명을 입력하세요')
    st.write('여기는 우리 학교 수업 페이지입니다.')
    st.divider()
    
    st.header('울학교 선배님들의 추천 ✨')
    st.caption('GPT-4o 활용 추천',
               help='인공지능 GPT-4o로 기존의 리뷰의 일부를 분석해 수업을 추천합니다.')
    documents = list(collection.find({}, {'_id': 1, 'recommend_text': 1, 'recommend_reason': 1}))
    cols = st.columns(2)
    for idx, doc in enumerate(documents):
        col = cols[idx % 2]
        with col.container(border=True):
            text = doc['recommend_text']
            st.subheader(f'🎓 {text}')
            #st.write(doc['recommend_reason'])            

            

if __name__ == "__main__":
    main()
