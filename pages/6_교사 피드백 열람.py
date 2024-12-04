import streamlit as st
from pymongo import MongoClient
import pandas as pd


# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
data = client["teacher_page"]
evaluation_collection = data["evaluation"]

db = client["highschool_db"]
collection = db["classes_info"]
classes_review_collection = db["classes_reviews"]
teacher_collection = db["teacher_page"]

user_db = client["user_database"]
student_collection = user_db["student"]

def main():
    st.title("📚 수강 과목 선택 페이지")
    student_id = st.text_input("🔍 학번을 입력하세요:", key="student_id")

    if student_id:
        # 학생 학번으로 학생 이름 조회
        student = student_collection.find_one({"학번": student_id})
        if student:
            st.write(f"학생 이름: **{student['이름']}**")
            # classes_info 컬렉션에서 과목 정보 가져오기
            subject_names = collection.distinct("subject_name")
            selected_subject = st.selectbox("📖 수강 과목을 선택하세요:", subject_names, key="selected_subject")

            if selected_subject:
                # 선택된 과목에 대한 세부 강좌 정보 가져오기
                classes = collection.find_one({"subject_name": selected_subject}).get("classes", [])
                class_names = [cls["class_name"] for cls in classes]
                selected_class = st.selectbox("📝 세부 강좌를 선택하세요:", class_names, key="selected_class")

                if selected_class:
                    # evaluation 컬렉션에서 세부 강좌에 맞는 정보 출력
                    evaluation = evaluation_collection.find_one({"학번": student_id, "수강강좌": selected_class})
                    if evaluation and evaluation['수강강좌'] == selected_class:
                        st.markdown("## 📊 최종 평가 정보")
                        st.markdown(f"- **성적 등급**: {evaluation['성적등급']}")
                        st.markdown(f"- **피드백**: {evaluation['피드백']}")
                        st.write("## 📊 세부 평가 정보")
                        # DataFrame을 이용하여 성취 목표와 성적 등급을 출력
                        achievements_data = [
                            {"성취 목표": achievement['성취 목표'], "성적 등급": achievement['성적 등급']}
                            for achievement in evaluation["성취목표채점"]
                        ]
                        df = pd.DataFrame(achievements_data)
                        st.dataframe(df)
                    else:
                        st.error("해당 세부 강좌에 대한 평가 정보가 없습니다.")
        else:
            st.error("잘못된 학번입니다")

if __name__ == "__main__":
    main()
