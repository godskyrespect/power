import streamlit as st
from pymongo import MongoClient

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection = db["classes_info"]

# Streamlit 앱 시작
st.title("에브리타임 데이터 크롤링(미완성)")

@st.cache_data
def get_documents():
    return list(collection.find())

documents = get_documents()

# 과목명 목록 생성
subjects = list(set(document.get('subject_name') for document in documents))
selected_subject = st.selectbox("과목을 선택하세요", subjects)

# 선택된 과목의 세부 과목명 목록 생성
if selected_subject:
    filtered_documents = [document for document in documents if document.get('subject_name') == selected_subject]
    classes = list(set(review.get('classes') for document in filtered_documents for review in document.get('reviews', []) if review.get('classes')))
    selected_class = st.selectbox("세부 과목명을 선택하세요", classes)

    # 선택된 세부 과목명의 데이터 출력
    if selected_class:
        for document in filtered_documents:
            reviews = document.get('reviews', [])
            for idx, review_obj in enumerate(reviews):
                if review_obj.get('classes') == selected_class:
                    st.write(f"리뷰 {idx + 1}:")
                    st.write(f"  과목 코드: {review_obj.get('class_id')}")
                    st.write(f"  과목명(세부): {review_obj.get('classes')}")
                    st.write(f"  교수님: {review_obj.get('professor')}")
                    st.write(f"  리뷰 내용: {review_obj.get('reviews', [])}")
                    st.write("---")

# 필요한 경우 MongoDB 연결 닫기
client.close()
