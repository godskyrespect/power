import streamlit as st
from pymongo import MongoClient

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection = db["classes_info"]
classes_review_collection = db["classes_reviews"]

# Streamlit 앱 시작
st.title("에브리타임 데이터 크롤링(미완성)")

# MongoDB에서 데이터 가져오기
@st.cache_data
def get_documents():
    return list(collection.find())

@st.cache_data
def get_class_reviews():
    return list(classes_review_collection.find())

documents = get_documents()
class_reviews_documents = get_class_reviews()

# 과목명 목록 생성
subjects = list(set(document.get('subject_name') for document in documents))
selected_subject = st.selectbox("과목을 선택하세요", subjects, key="subject_select")

# 선택된 과목의 세부 과목명 목록 생성 및 출력
if selected_subject:
    filtered_documents = [document for document in documents if document.get('subject_name') == selected_subject]
    classes = list(set(class_obj.get('class_name') for document in filtered_documents for class_obj in document.get('classes', []) if class_obj.get('class_name')))
    selected_class = st.selectbox("세부 과목명을 선택하세요", classes, key="class_select")

    # 선택된 세부 과목명의 데이터 출력
    if selected_class:
        for document in filtered_documents:
            classes = document.get('classes', [])
            for idx, class_obj in enumerate(classes):
                if class_obj.get('class_name') == selected_class:
                    st.write(f"리뷰 {idx + 1}:")
                    st.write(f"  과목 코드: {class_obj.get('class_id')}")
                    st.write(f"  세부 과목명: {class_obj.get('class_name')}")
                    st.write(f"  교수님: {class_obj.get('professor')}")
                    st.write(f"  평점: {class_obj.get('ratings')}")
                    st.write("---")

                    # classes_review DB에서 class_name으로 조인하여 리뷰 출력
                    class_name = class_obj.get('class_name')
                    if class_name:
                        review_found = False
                        for class_review in class_reviews_documents:
                            reviews = class_review.get('reviews', [])
                            for review in reviews:
                                if review.get('class_name') == class_name:
                                    st.write(f"리뷰 내용: {review.get('review_text')}")
                                    st.write("---")
                                
# 필요한 경우 MongoDB 연결 닫기
client.close()
