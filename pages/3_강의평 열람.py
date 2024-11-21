import streamlit as st
from pymongo import MongoClient

if not st.session_state.logged_in:
    st.warning("로그인 후에 강의평 작성 및 열람 페이지에 접속할 수 있습니다.")
    st.stop()
    
# MongoDB Connection
client = MongoClient("mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")  # MongoDB Atlas 연결 주소
db = client["lecture_evaluation"]
collection = db["evaluations"]

# Streamlit App to Display Lecture Evaluations
def main():
    st.title("Lecture Evaluations")

    # Fetching all evaluations from MongoDB
    evaluations = list(collection.find())

    if evaluations:
        for eval in evaluations:
            st.subheader(f"Lecture: {eval['lecture_name']}")
            st.text(f"Professor: {eval['professor_name']}")
            st.text(f"Rating: {eval['rating']}/5")
            st.text_area("Evaluation Content", eval['evaluation_content'], height=100, disabled=True)
            st.markdown("---")
    else:
        st.info("No evaluations available yet.")

if __name__ == "__main__":
    main()
