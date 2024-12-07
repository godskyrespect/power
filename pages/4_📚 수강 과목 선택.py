import streamlit as st
from pymongo import MongoClient
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
model = 'gpt-4o-mini'
def chatgpt_generate(query):
    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    },{
        "role": "user",
        "content": query
    }]
    response = client.chat.completions.create(model=model, messages=messages)
    answer = response.choices[0].message.content
    return answer

def prompt_generator(query):
    prompt = f"""
    당신의 역할은 JSON형태의 데이터가 주어지면 그에 맞는 조언을 해주어야 합니다. 
    데이터에는 학생의 성적, 교사의 피드백, 성취기준별 수행정도가 적혀있습니다. 이 데이터를 바탕으로 학생이 노력해야할 성취기준을 알려주세요. 그리고 교사의 피드백을 참고하여 적절한 조언을 적어주세요.

    데이터 : {query}
    """        
    answer = chatgpt_generate(prompt)
    return answer
    
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "name" not in st.session_state:
    st.session_state.name = ""

# 로그인 상태 확인 후 사이드바에 사용자 정보 표시
if st.session_state.logged_in:
    with st.sidebar:
        st.write(f"{st.session_state.student_id}")
        st.write(f"{st.session_state.name}")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.student_id = ""
            st.session_state.name = ""
            st.success("로그아웃되었습니다.")
if not st.session_state.logged_in:
    st.warning("로그인 해주세요.")
else:
    def main():
        st.title("📚 수강 과목 선택 페이지")
        student_id = st.session_state.student_id

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
                            grade = evaluation['성적등급']
                            feedback = evaluation['피드백']
                            st.markdown("## 📊 최종 평가 정보")
                            st.markdown(f"- **성적 등급**: {grade}")
                            st.markdown(f"- **피드백**: {feedback}")
                            st.write("## 📊 세부 평가 정보")
                            # DataFrame을 이용하여 성취 목표와 성적 등급을 출력
                            achievements_data = [
                                {"성취 목표": achievement['성취 목표'], "성적 등급": achievement['성적 등급']}
                                for achievement in evaluation["성취목표채점"]
                            ]
                            df = pd.DataFrame(achievements_data)
                            st.dataframe(df)

                            json_data = {
                                "성적 등급": grade,
                                "피드백": feedback,
                                "세부평가정보": achievements_data
                            }

                            summary = prompt_generator(json_data)
                            st.write("🤖 AI도우미의 정리 :")
                            st.write(f"{summary}")

                            
                        else:
                            st.error("해당 세부 강좌에 대한 평가 정보가 없습니다.")
            else:
                st.error("잘못된 학번입니다")

    if __name__ == "__main__":
        main()
