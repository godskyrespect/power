import streamlit as st
from pymongo import MongoClient
import hashlib

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "학번" not in st.session_state:
    st.session_state.student_id = ""
if "이름" not in st.session_state:
    st.session_state.name = ""

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["user_database"]
users_collection = db["student"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(student_id, password):
    user = users_collection.find_one({"학번": student_id})
    if user and user["password"] == hash_password(password):
        return user
    return None

def register_user(student_id, password, name):
    users_collection.insert_one({
        "학번": student_id,
        "password": hash_password(password),
        "이름": name
    })

st.title("온양고등학교 2025 고교학점제 강의평가록")
tabs = st.tabs(["로그인", "회원가입"])

# 로그인 탭
with tabs[0]:
    st.header("로그인")
    student_id = st.text_input("학번", key="login_student_id")
    password = st.text_input("비밀번호", type="password", key="login_password")
    
    if st.button("로그인", key="login_button"):
        user = authenticate_user(student_id, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.student_id = student_id
            st.session_state.name = user["이름"]
            st.success(f"환영합니다, {student_id}{user['이름']}님!")
        else:
            st.error("학번 또는 비밀번호가 잘못되었습니다.")

# 회원가입 탭
with tabs[1]:
    st.header("회원가입")
    student_id = st.text_input("학번", key="register_student_id")
    password = st.text_input("비밀번호", type="password", key="register_password")
    confirm_password = st.text_input("비밀번호 확인", type="password", key="confirm_password")
    name = st.text_input("이름", key="register_name")

    if st.button("회원가입", key="register_button"):
        if not student_id or not password or not name:
            st.error("모든 필드를 입력해주세요.")
        elif users_collection.find_one({"학번": student_id}):
            st.error("이미 존재하는 학번입니다.")
        elif password != confirm_password:
            st.error("비밀번호가 일치하지 않습니다.")
        else:
            register_user(student_id, password, name)
            st.success("회원가입이 완료되었습니다! 로그인하세요.")
            
if st.session_state.logged_in:
    with st.sidebar:
        st.write(f" {st.session_state.student_id}")
        st.write(f" {st.session_state.name}")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.student_id = ""
            st.session_state.name = ""
            st.success("로그아웃되었습니다.")
