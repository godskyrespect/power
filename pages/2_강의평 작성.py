import streamlit as st
from pymongo import MongoClient
import json

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection = db["classes_info"]
collection_evaluations = db["classes_evaluations"]

# Streamlit 앱 시작
st.title("강의평 작성")


# 사용자로부터 classes_evaluations 입력 받기
subject_names = list(collection.distinct("subject_name"))
subject_name = st.selectbox("과목명", subject_names)

# 선택된 과목에 해당하는 세부 과목명 목록 가져오기
class_name = None
professor = None
if subject_name:
    filtered_documents = collection.find({"subject_name": subject_name})
    class_names = list(set(class_obj["class_name"] for doc in filtered_documents for class_obj in doc.get("classes", [])))
    class_name = st.selectbox("세부 과목명", class_names, key="class_select")

    # 선택된 세부 과목명에 해당하는 교수명 가져오기
    if class_name:
        filtered_documents = collection.find({"subject_name": subject_name, "classes.class_name": class_name})
        professors = list(set(
            class_obj["professor"]
            for doc in filtered_documents
            for class_obj in doc.get("classes", [])
            if class_obj["class_name"] == class_name
        ))
        professor = st.selectbox("교수님", professors, key="professor_select")

ratings = st.slider("평점", 1.0, 5.0, 3.0, 0.5)
review_text = st.text_area("리뷰 내용")
submit_button = st.button("저장하기")

# 입력된 classes_evaluations 데이터 처리
if submit_button and subject_name and class_name and professor:
    evaluation_data = {
        "subject_name": subject_name,
        "class_name": class_name,
        "professor": professor,
        "ratings": ratings,
        "review_text": review_text
    }
    collection_evaluations.insert_one(evaluation_data)
    st.success("classes_evaluations 데이터가 성공적으로 저장되었습니다.")

# 필요한 경우 MongoDB 연결 닫기
client.close()
