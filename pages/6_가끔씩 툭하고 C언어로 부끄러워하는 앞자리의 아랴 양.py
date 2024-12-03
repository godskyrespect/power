import streamlit as st
from pymongo import MongoClient

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["highschool_db"]
collection = db["classes_info"]
classes_review_collection = db["classes_reviews"]
collection_evaluations = db["classes_evaluations"]

# Streamlit 앱 시작
st.title("에브리타임 데이터 크롤링(미완성)")

# MongoDB에서 데이터 가져오기
@st.cache_data
def get_documents():
    return list(collection.find())

@st.cache_data
def get_class_reviews():
    return list(classes_review_collection.find())


tabs1, tabs2 = st.tabs(["강의평", "강의평 작성"])
with tabs1:
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

with tabs2:
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

if st.session_state.logged_in:
    with st.sidebar:
        st.write(f" {st.session_state.student_id}")
        st.write(f" {st.session_state.name}")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.student_id = ""
            st.session_state.name = ""
            st.success("로그아웃되었습니다.")

                                
# 필요한 경우 MongoDB 연결 닫기
client.close()


if st.session_state.logged_in:
    with st.sidebar:
        st.write(f" {st.session_state.student_id}")
        st.write(f" {st.session_state.name}")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.student_id = ""
            st.session_state.name = ""
            st.success("로그아웃되었습니다.")
