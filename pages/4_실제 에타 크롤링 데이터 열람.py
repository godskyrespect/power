import streamlit as st
from pymongo import MongoClient

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection = db["classes_info"]

# Streamlit 앱 시작
st.title("에브리타임 데이터 크롤링(미완성)")

# MongoDB에서 데이터 가져오기
documents = collection.find()
subjects = list(set(document.get('subject') for document in documents))
selected_subject = st.selectbox("과목을 선택하세요", subjects)


# 선택된 과목의 데이터 출력
filtered_documents = list(collection.find({"subject": selected_subject}))

for document in filtered_documents:
    reviews_object = document.get('reviews', {})
    st.write(f"과목명: {document.get('subject')}")
    st.write(f"과목 코드: {reviews_object.get('class_id')}")
    st.write(f"과목명(세부): {reviews_object.get('classes')}")
    st.write(f"교수님: {reviews_object.get('professor')}")
    st.write(f"평점: {document.get('ratings')}")
    st.write("리뷰:")
    for idx, review in enumerate(reviews_object.get('reviews', [])):
        st.write(f"{idx + 1}. {review}")
    st.write("---")

# 필요한 경우 MongoDB 연결 닫기
client.close()
