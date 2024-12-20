import config
import streamlit as st
import pandas as pd
from openai import OpenAI
from capstone import RequestApi


st.sidebar.image("image.png", use_container_width=True)

st.markdown("""
    <style>
        .container {
            max-width: 500px;
            margin: 0 auto;
            padding: 2rem;
            background-color: #f9f9f9;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .tab-content {
            padding: 1.5rem;
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 1rem;
        }
        .stButton > button {
            width: 100%;
            height: 3rem;
            border-radius: 5px;
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)
# OpenAI 연결 설정 ====================================
client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)

## 0. API호출(수업정보, 리뷰정보)
collection = RequestApi("school")
classes_review_collection = RequestApi("school/reviews")
student_collection = RequestApi("user/student")
evaluation_collection = RequestApi("teacher/evaluation")

## 1. 작성된 프롬프트를 LLM에 전달하고 응답을 받는 함수(get: 프롬프트)
def chatgpt_generate(query):
    messages = [{"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}]
    response = client.chat.completions.create(model="gpt-4o-mini", messages=messages)
    answer = response.choices[0].message.content
    return answer

## 2. 평가 데이터(JSON)을 포함하여 LLM에게 전달할 프롬프트를 생성하는 함수(get: 학생 평가 데이터.json)
def prompt_generator(grade, feedback, data):
    json_data = {
        "성적 등급": grade,
        "피드백": feedback,
        "세부평가정보": data
    }
    
    prompt = f"""
    당신의 역할은 JSON형태의 데이터가 주어지면 고등학생에게 그에 맞는 조언을 해주어야 합니다. 
    데이터에는 학생의 성적, 교사의 피드백, 성취기준별 수행정도가 적혀있습니다. 이 데이터를 바탕으로 학생이 노력해야할 성취기준을 알려주세요. 그리고 교사의 피드백을 참고하여 적절한 조언을 적어주세요.
    조언을 해줄 때에는 ~요. 형태로 끝나는 문장을 사용해야 하며 문단의 끝에는 이모티콘을 포함해야 합니다.
    데이터 : {json_data}
    """        
    answer = chatgpt_generate(prompt)
    return answer

## Streamlit 사이트 코드 ============================
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
        st.info("이 페이지에서는 나의 수업 평가에 대한 내용을 볼 수 있어요. 정보 과목을 검색해 보세요!", icon="🎅")
        st.title("📚 나의 수업 평가")
        student_id = st.session_state.student_id
        student_name = st.session_state.name

        if student_id:
            st.write(f"학생 이름: **{student_name}**")
            # classes_info 컬렉션에서 과목 정보 가져오기
            subject_names = [item.get("subject_name") for item in collection]
            selected_subject = st.selectbox("📖 수강 과목을 선택하세요:", subject_names, key="selected_subject")

            if selected_subject:
                # 선택된 과목에 대한 세부 강좌 정보 가져오기
                class_names = []
                for subject in collection:
                        if subject["subject_name"] == selected_subject:
                            classes = subject.get('classes')
                            for cls in classes:
                                class_names.append(cls['class_name'])
                            break

                selected_class = st.selectbox("📝 세부 강좌를 선택하세요:", class_names, key="selected_class")

                if selected_class:
                    # evaluation 컬렉션에서 세부 강좌에 맞는 정보 출력
                    for student in evaluation_collection:
                        if student["학번"] == student_id and student["수강강좌"] == selected_class:
                            evaluation = student
                            break
                        evaluation = None
                        
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

                        # ChatGPT를 이용한 수업 평가 요약 및 피드백
                        st.write("## 🤖 수업 평가 정리 :")
                        summary = prompt_generator(grade, feedback, achievements_data)
                        with st.container(border=True):
                            st.write(f"{summary}")
                        if st.button("평가 새로고침하기"):
                            st.rerun()
                                            
                    else:
                        st.error("해당 세부 강좌에 대한 평가 정보가 없습니다.")   


    if __name__ == "__main__":
        main()
