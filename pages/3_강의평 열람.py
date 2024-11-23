import streamlit as st
from pymongo import MongoClient

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection_info = db["classes_info"]
collection_evaluations = db["classes_evaluations"]

# Streamlit 앱 시작
st.title("classes_evaluations 데이터 출력")

# MongoDB에서 데이터 가져오기
@st.cache_data
def get_evaluations():
    return list(collection_evaluations.find())

@st.cache_data
def get_class_info():
    return list(collection_info.find())

class_info_documents = get_class_info()
evaluations = get_evaluations()

# 과목명 목록 생성
subject_names = list(set(document.get('subject_name') for document in class_info_documents))
selected_subject = st.selectbox("과목을 선택하세요", subject_names, key="subject_select")

# 선택된 과목의 세부 과목명 목록 생성 및 출력
if selected_subject:
    filtered_documents = [document for document in class_info_documents if document.get('subject_name') == selected_subject]
    class_names = list(set(class_obj.get('class_name') for document in filtered_documents for class_obj in document.get('classes', []) if class_obj.get('class_name')))
    selected_class = st.selectbox("세부 과목명을 선택하세요", class_names, key="class_select")

    # 선택된 세부 과목명의 평가 데이터 출력
    if selected_class:
        filtered_evaluations = [evaluation for evaluation in evaluations if evaluation.get('class_name') == selected_class]
        if filtered_evaluations:
            for idx, evaluation in enumerate(filtered_evaluations):
                st.write(f"리뷰 {idx + 1}:")
                st.write(f"  과목명: {evaluation.get('subject_name', 'N/A')}")
                st.write(f"  세부 과목명: {evaluation.get('class_name', 'N/A')}")
                st.write(f"  교수님: {evaluation.get('professor', 'N/A')}")
                st.write(f"  평점: {evaluation.get('ratings', 'N/A')}")
                st.text_area("리뷰 내용", evaluation.get('review_text', 'N/A'), height=100, disabled=True)
                st.write("---")
        else:
            st.write("해당 세부 과목에 대한 평가가 없습니다.")

# 필요한 경우 MongoDB 연결 닫기
client.close()
