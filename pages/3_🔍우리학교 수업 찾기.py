import streamlit as st
import certifi
import requests
import time
import torch
import numpy as np
import pandas as pd
import streamlit as st


MAPPING_EN2KO = {
    "passion": "열정적인 교수님",
    "benefit": "유익한 수업",
    "helpful": "도움되는 수업",
    "easy": "꿀강",
    "gain": "얻어가는 수업"
}
MAPPING_KO2EN = {v: k for k, v in MAPPING_EN2KO.items()}

# MongoDB 연결 준비
#uri = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
#db = client['recommendations_db']
#collection = db['recommendations']

#documents = list(collection.find({}))
st.markdown("""
    <style>
    h3 {
        color: teal;
        font-size: 36px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)
##========================API LOAD=======================##
url_schoollist = "http://13.211.145.139:8000/school/info"
response_sl = requests.get(url_schoollist)
school_data = response_sl.json()

url_ratings = "http://13.211.145.139:8000/school/ratings"
response_rt = requests.get(url_ratings)
ratings = response_rt.json()

##======================API REQUEST======================##
def get_recommendations(query_ko):
    query_en = MAPPING_KO2EN[query_ko]
    print(query_en)
    url = f"http://13.211.145.139:8000/recommend/{query_en}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()[0]
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data

def get_documents():
    url = "http://13.211.145.139:8000/recommend/recommends"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Request failed with status code: {response.status_code}")

    return data

def find_professor(class_name):
    data = school_data
    for cls in data:
        if cls["class_name"] == class_name:
            return cls["professor"]

def check_ratings(key):
    data = ratings
    for item in data:
        if key in item:
            return int(item[key])
    
    
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


  
st.info("이 페이지에서는 우리 학교에서 추천하는 수업을 보거나 검색할 수 있어요!", icon="🎅")
# st.title('우리 학교 수업')
st.title("🔍우리학교 수업 찾기")
search_query = st.text_input("🔍 찾고싶은 수업을 검색해보세요.", placeholder='수업명을 입력하세요. 예: 정보')
tab1, tab2 = st.tabs(["수업 검색", "추천 수업"])
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
            #search_query2 = st.text_input("search", placeholder='수업명을 입력하세요', label_visibility='hidden')

with tab2:
    st.header('울학교 선배님들의 추천 ✨')
    st.caption('GPT-4o 활용 추천',
               help='인공지능 GPT-4o로 기존의 리뷰의 일부를 분석해 수업을 추천합니다.')
    
    
    documents = get_documents()
    text = [doc['recommend_text'] for doc in documents]
    text = [f'🎓{txt}' for txt in text]
    selection = st.pills(f'수업 추천 키워드', text, selection_mode='single')
    
    if selection:
        with st.container(border=True):
            show_recommendations(selection)
    
    
    
    
