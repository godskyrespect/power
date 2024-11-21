import streamlit as st
from pymongo import MongoClient

if not st.session_state.logged_in:
    st.warning("로그인 후에 강의평 작성 및 열람 페이지에 접속할 수 있습니다.")
    st.stop()

# MongoDB Connection
client = MongoClient("mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB Atlas 연결 주소
db = client["lecture_evaluation"]
collection = db["evaluations"]

# Streamlit App
def main():
    st.title("Lecture Evaluation Site")

    # Subject Selection
    subjects = ["과학", "수학", "정보", "미술"]
    selected_subject = st.selectbox("Select Subject", subjects, key="subject_select")

    # Lecture selection based on selected subject
    if selected_subject == "과학":
        lecture_options = ["물리학1", "화학1", "지구과학1", "생명과학1"]
    elif selected_subject == "수학":
        lecture_options = ["수학1", "미적분학1", "기하학1"]
    else:
        lecture_options = []

    # Adding a selectbox for lectures with unique key to refresh
    if lecture_options:
        lecture_name = st.selectbox("Select Lecture Name", lecture_options, key="lecture_select")
    else:
        lecture_name = selected_subject

    # Form for Lecture Evaluation
    with st.form("evaluation_form"):
        professor_name = st.text_input("Professor Name")
        rating = st.slider("Rating", 1.0, 5.0, 3.0, 0.5)
        evaluation_content = st.text_area("Evaluation Content")
        submit_button = st.form_submit_button("Submit")

        # When the form is submitted, store data in MongoDB
        if submit_button:
            if lecture_name and professor_name and evaluation_content:
                evaluation = {
                    "lecture_name": lecture_name,
                    "professor_name": professor_name,
                    "rating": rating,
                    "evaluation_content": evaluation_content
                }
                collection.insert_one(evaluation)
                st.success("Evaluation submitted successfully!")
            else:
                st.error("Please fill in all the fields.")

if __name__ == "__main__":
    main()
