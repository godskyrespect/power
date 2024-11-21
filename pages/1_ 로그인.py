import streamlit as st
from pymongo import MongoClient
import hashlib

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["auth_demo"]
users_collection = db["users"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True
    return False

def register_user(username, password):
    users_collection.insert_one({
        "username": username,
        "password": hash_password(password),
    })

st.title("로그인")

choice = st.selectbox("메뉴 선택", ["로그인", "회원가입"])

if choice == "로그인":
    username = st.text_input("아이디", key="login_username")
    password = st.text_input("비밀번호", type="password", key="login_password")
    if st.button("로그인"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"환영합니다, {username}님!")
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")
elif choice == "회원가입":
    username = st.text_input("아이디", key="register_username")
    password = st.text_input("비밀번호", type="password", key="register_password")
    confirm_password = st.text_input("비밀번호 확인", type="password", key="confirm_password")
    if st.button("회원가입"):
        if not username or not password:
            st.error("아이디와 비밀번호를 모두 입력해주세요.")
        elif users_collection.find_one({"username": username}):
            st.error("이미 존재하는 아이디입니다.")
        elif password != confirm_password:
            st.error("비밀번호가 일치하지 않습니다.")
        else:
            register_user(username, password)
            st.success("회원가입이 완료되었습니다! 로그인하세요.")
