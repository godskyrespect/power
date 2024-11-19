import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

import streamlit as st
from pymongo import MongoClient
from datetime import datetime

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["my_database"]  # 데이터베이스 이름 설정
collection = db["posts"]    # 컬렉션 이름 설정

# Streamlit 웹 애플리케이션
def main():
    st.title("익명 게시판. 다양한 의견(아무거나!)을 작성해주세요! ")
    
    # 글 작성 폼
    st.header("글 작성하기")
    with st.form("글 작성"):
        title = st.text_input("제목")
        content = st.text_area("내용")
        author = st.text_input("작성자")
        submitted = st.form_submit_button("저장하기")
        
        if submitted:
            if title and content and author:
                # MongoDB에 데이터 저장
                post = {
                    "title": title,
                    "content": content,
                    "author": author,
                    "created_at": datetime.utcnow()
                }
                collection.insert_one(post)
                st.success("글이 성공적으로 저장되었습니다!")
            else:
                st.error("모든 필드를 작성해주세요.")
    
    # 저장된 글 목록 보기
    st.header("저장된 글 목록")
    posts = collection.find()
    for post in posts:
        st.subheader(post["title"])
        st.write(f"**작성자:** {post['author']}")
        st.write(post["content"])
        st.write(f"_작성일: {post['created_at']}_")
        st.write("---")

if __name__ == "__main__":
    main()
