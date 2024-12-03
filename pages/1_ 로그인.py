import streamlit as st
from pymongo import MongoClient
import hashlib

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "이름" not in st.session_state:
    st.session_state.username = ""
if "학번" not in st.session_state:
    st.session_state.username = ""

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["user_database"]
users_collection = db["student"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True
    return False

def register_user(username, password, name, student_id):
    users_collection.insert_one({
        "username": username,
        "password": hash_password(password),
        "이름": name,
        "학번": student_id
    })

st.title("온양고등학교 2025 고교학점제 강의평가록")
tabs = st.tabs(["로그인", "회원가입"])


# 로그인 탭
with tabs[0]:
    st.header("로그인")
    username = st.text_input("아이디", key="login_username")
    password = st.text_input("비밀번호", type="password", key="login_password")
    
    if st.button("로그인", key="login_button"):
        user = authenticate_user(username, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.username = user["username"]
            st.session_state.이름 = user["이름"]
            st.session_state.학번 = user["학번"]
            st.success(f"환영합니다, {user['이름']}님! (학번: {user['학번']})")
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")

# 회원가입 탭
with tabs[1]:
    st.header("회원가입")
    username = st.text_input("아이디", key="register_username")
    password = st.text_input("비밀번호", type="password", key="register_password")
    confirm_password = st.text_input("비밀번호 확인", type="password", key="confirm_password")
    name = st.text_input("이름", key="register_name")
    student_id = st.text_input("학번", key="register_student_id")

    if st.button("회원가입", key="register_button"):
        if not username or not password or not name or not student_id:
            st.error("모든 필드를 입력해주세요.")
        elif users_collection.find_one({"username": username}):
            st.error("이미 존재하는 아이디입니다.")
        elif users_collection.find_one({"학번": student_id}):
            st.error("이미 존재하는 학번입니다.")
        elif password != confirm_password:
            st.error("비밀번호가 일치하지 않습니다.")
        else:
            register_user(username, password, name, student_id)
            st.success("회원가입이 완료되었습니다! 로그인하세요.")
