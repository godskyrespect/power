import streamlit as st
from pymongo import MongoClient

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection_evaluations = db["classes_evaluations"]
collection_classes_info = db["classes_info"]

# Streamlit 앱 시작
st.title("강의평 보기")

# MongoDB에서 데이터 가져오기
@st.cache_data
def get_evaluations():
    return list(collection_evaluations.find())

@st.cache_data
def get_classes_info():
    return list(collection_classes_info.find())

classes_info_documents = get_classes_info()
subject_names = list(set(doc.get('subject_name') for doc in classes_info_documents))
subject_name = st.selectbox("과목을 선택하세요", subject_names, key="subject_select")

# 선택된 과목의 세부 과목명 목록 생성
class_names = []
if subject_name:
    filtered_documents = [doc for doc in classes_info_documents if doc.get('subject_name') == subject_name]
    class_names = list(set(class_obj.get('class_name') for doc in filtered_documents for class_obj in doc.get('classes', [])))
    class_name = st.selectbox("세부 과목명을 선택하세요", class_names, key="class_select")

# 데이터 출력
evaluations = get_evaluations()
if evaluations:
    for idx, evaluation in enumerate(evaluations):
        if subject_name == evaluation.get('subject_name') and (not class_names or class_name == evaluation.get('class_name')):
            st.write(f"리뷰 {idx + 1}:")
            st.write(f"  과목명: {evaluation.get('subject_name', 'N/A')}")
            st.write(f"  세부 과목명: {evaluation.get('class_name', 'N/A')}")
            st.write(f"  교수님: {evaluation.get('professor', 'N/A')}")
            st.write(f"  평점: {evaluation.get('ratings', 'N/A')}")
            st.text_area("리뷰 내용", evaluation.get('review_text', 'N/A'), height=100, disabled=True)
            st.write("---")
else:
    st.write("데이터가 없습니다.")

# 필요한 경우 MongoDB 연결 닫기
client.close()
