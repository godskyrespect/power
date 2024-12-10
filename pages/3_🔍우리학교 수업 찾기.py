import numpy as np
import pandas as pd
import streamlit as st
from capstone import RequestApi
st.sidebar.image("image.png", use_container_width=True)
## 1. API주소 입력을 위한 한/영 변환
MAPPING_EN2KO = {
    "passion": "열정적인 교수님",
    "benefit": "유익한 수업",
    "helpful": "도움되는 수업",
    "easy": "꿀강",
    "gain": "얻어가는 수업"
}
MAPPING_KO2EN = {v: k for k, v in MAPPING_EN2KO.items()}

st.markdown("""
    <style>
    h3 {
        color: teal;
        font-size: 36px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

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

## 2. API호출(수업정보, 리뷰정보)
school_data = RequestApi("school/info")
ratings = RequestApi("school/ratings")
documents = RequestApi("recommend/recommends")

## 3. 추천 내용 API를 호출하는 함수(get: 추천키워드, return: 추천 API내용)
def get_recommendations(query_ko):
    query_en = MAPPING_KO2EN[query_ko]
    data = RequestApi(f"recommend/{query_en}")
    return data[0]
    
## 4. 수업별 담당 선생님을 알려주는 함수(get: 수업명, return: 선생님 이름)
def find_professor(class_name):
    data = school_data
    for cls in data:
        if cls["class_name"] == class_name:
            return cls["professor"]

## 5. 리뷰에서 별점만 반환하는 함수(get: 수업명(key), return: 별점(value))
def check_ratings(key):
    data = ratings
    for item in data:
        if key in item:
            return int(item[key])
    
## 6. 추천 내용을 정리해서 보여주는 함수(get: 수업 키워드)
def show_recommendations(select):
    text = select.replace("🎓", "")
    recs = get_recommendations(text)
    rec_reason = recs['recommend_reason']
    st.subheader(f'"{select}"') 
    st.write(rec_reason)
    
    st.divider()
    
    selection = [item['subject'] for item in recs['recommendations']]
    options = st.multiselect("표시하지 않을 교과를 선택하세요.", selection, placeholder="제외할 교과 선택")
    for rec in recs['recommendations']:
        subject = rec['subject']
        if subject in options:
            continue
        else:
            classes = rec['class']
            with st.container(border=True):
                st.header(f'{subject} 교과 추천')
                for idx, cls in enumerate(classes):
                    prof = find_professor(cls)
                    ratings = check_ratings(cls)
                    star = "⭐"
                    star_black = " ★ "
                    lists = f''' ∙  **{cls}** :gray[{prof}]  
                    {star*ratings}{star_black*(5-ratings)}'''
                    st.write(lists)

# Streamlit 앱 시작

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
  
st.info("이 페이지에서는 우리 학교에서 추천하는 수업을 보거나 검색할 수 있어요!", icon="🎅")

## Streamlit 화면 ======================================
st.title("🔍우리학교 수업 찾기")
search_query = st.text_input("🔍 찾고싶은 수업을 검색해보세요.", placeholder='수업명을 입력하세요. 예: 정보')
tab1, tab2 = st.tabs(["수업 검색", "추천 수업"])

## 수업을 검색하여 과목별 정보를 알려주는 탭
with tab1:
    matches = [item for item in school_data if item.get("class_name") == search_query]
    if matches:
        
        with st.container(border=True):
            st.title(f"📔{matches[0]['class_name']}")
            st.divider()
            st.write(f"**수업 코드** : {matches[0]['class_id']}")
            st.write(f"**담당 교사** : {matches[0]['professor']} 선생님")
            st.divider()
            st.header("과목 성취기준")
            achievements = matches[0]['achievements']
            achievement_list = achievements.split('", "')
            achievement_list[0] = achievement_list[0].lstrip('"')
            achievement_list[-1] = achievement_list[-1].rstrip('"')
            for idx, achievement in enumerate(achievement_list):
                st.write(f"{idx+1}. {achievement}")
            
          
    else:
        if search_query:
            st.error("검색된 강의가 없습니다", icon="❕")

## 키워드에 따른 추천 수업을 보여주는 탭
with tab2:
    st.header('울학교 선배님들의 추천 ✨')
    st.caption('GPT-4o 활용 추천',
               help='인공지능 GPT-4o로 기존의 리뷰의 일부를 분석해 수업을 추천합니다.')

    text = [doc['recommend_text'] for doc in documents]
    text = [f'🎓{txt}' for txt in text]
    selection = st.pills(f'수업 추천 키워드', text, selection_mode='single')
    
    if selection:
        with st.container(border=True):
            show_recommendations(selection)
    
    
    
    
