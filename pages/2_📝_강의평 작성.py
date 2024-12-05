import streamlit as st
from pymongo import MongoClient
import json

st.set_page_config(
    page_title="📘 강의평 작성",
    page_icon="✏️"
)

st.title("📘 강의평 작성")
# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection = db["classes_info"]
classes_review_collection = db["classes_reviews"]

# Streamlit 앱 시작
st.title("강의평 작성")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "학번" not in st.session_state:
    st.session_state.student_id = ""
if "이름" not in st.session_state:
    st.session_state.name = ""
if not st.session_state.logged_in:
    st.warning("로그인 해주세요.")
else:
    # 탭 설정
    tabs = st.tabs(["강의평 작성", "강의평 열람"])

    # 강의평 작성 탭
    with tabs[0]:
        # 사용자로부터 classes_evaluations 입력 받기
        subject_names = list(collection.distinct("subject_name"))
        subject_name = st.selectbox("과목명", subject_names)

        # 선택된 과목에 해당하는 세부 과목명 목록 가져오기
        class_name = None
        professor = None
        if subject_name:
            filtered_documents = list(collection.find({"subject_name": subject_name}))
            class_names = list(set(class_obj["class_name"] for doc in filtered_documents for class_obj in doc.get("classes", [])))
            if class_names:
                class_name = st.selectbox("세부 과목명", class_names, key="class_select")

            # 선택된 세부 과목명에 해당하는 교수명 가져오기
            if class_name:
                filtered_documents = list(collection.find({"subject_name": subject_name}))
                professors = list(set(
                    class_obj["professor"]
                    for doc in filtered_documents
                    for class_obj in doc.get("classes", [])
                    if class_obj["class_name"] == class_name
                ))
                if professors:
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
            collection.insert_one(evaluation_data)
            st.success("classes_evaluations 데이터가 성공적으로 저장되었습니다.")

    # 강의평 열람 탭
    with tabs[1]:
        st.header("강의평 열람")

        # 사용자로부터 subject_name 선택
        subject_names = list(classes_review_collection.distinct("subject_name"))
        subject_name = st.selectbox("과목명", subject_names, key="subject_select_read")

        # 선택된 과목에 해당하는 세부 과목명 목록 가져오기
        class_name = None
        professor = None
        if subject_name:
            filtered_documents = list(classes_review_collection.find({"subject_name": subject_name}))
            reviews = [review for doc in filtered_documents for review in doc.get("reviews", [])]
            class_names = list(set(review.get("class_name") for review in reviews if "class_name" in review))
            if class_names:
                class_name = st.selectbox("세부 과목명", class_names, key="class_select_read")

            # 선택된 세부 과목명에 해당하는 교수명 가져오기
            if class_name:
                filtered_documents = list(collection.find({"subject_name": subject_name}))
                professors = list(set(
                    class_obj["professor"]
                    for doc in filtered_documents
                    for class_obj in doc.get("classes", [])
                    if class_obj["class_name"] == class_name
                ))
                if professors:
                    professor = st.selectbox("교수님", professors, key="professor_select_read")

        # 선택된 세부 과목명에 해당하는 리뷰와 평점 출력
        if class_name:
            filtered_reviews = [review for review in reviews if review.get("class_name") == class_name]
            if len(filtered_reviews) > 0:
                for review in filtered_reviews:
                    st.write(f"리뷰 내용: {review.get('review_text')}")
                    st.write(f"평점: {review.get('ratings')}")
                    st.write("---")
            else:
                st.write("리뷰가 없습니다. 소중한 리뷰를 달아주세요!")



if st.session_state.logged_in:
    with st.sidebar:
        st.write(f"학번: {st.session_state.student_id}")
        st.write(f"이름: {st.session_state.name}")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.student_id = ""
            st.session_state.name = ""
            st.success("로그아웃되었습니다.")
