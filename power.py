import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import hashlib

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["auth_demo"]  # 데이터베이스 이름 설정
users_collection = db["users"]  # 유저 정보를 저장할 컬렉션

# 비밀번호 해싱 함수
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 유저 인증 함수
def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and user["password"] == hash_password(password):
        return True
    return False

# 유저 존재 여부 확인
def user_exists(username):
    return users_collection.find_one({"username": username}) is not None

# 유저 등록 함수
def register_user(username, password):
    users_collection.insert_one({
        "username": username,
        "password": hash_password(password),
        "created_at": datetime.utcnow()
    })

# Streamlit 애플리케이션
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.sidebar.success(f"안녕하세요, {st.session_state.username}님!")
        st.sidebar.button("로그아웃", on_click=logout)
        st.write("로그인 상태입니다. 이제 글을 작성하거나 다른 기능을 추가할 수 있습니다.")
    else:
        st.sidebar.title("인증")
        choice = st.sidebar.radio("메뉴", ["로그인", "회원가입"])

        if choice == "로그인":
            login()
        elif choice == "회원가입":
            register()

# 로그인 기능
def login():
    st.title("로그인")
    username = st.text_input("아이디", key="login_username")
    password = st.text_input("비밀번호", type="password", key="login_password")
    if st.button("로그인"):
        if authenticate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"환영합니다, {username}님!")
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")

# 회원가입 기능
def register():
    st.title("회원가입")
    username = st.text_input("아이디", key="register_username")
    password = st.text_input("비밀번호", type="password", key="register_password")
    confirm_password = st.text_input("비밀번호 확인", type="password", key="confirm_password")
    if st.button("회원가입"):
        if not username or not password:
            st.error("아이디와 비밀번호를 모두 입력해주세요.")
        elif user_exists(username):
            st.error("이미 존재하는 아이디입니다.")
        elif password != confirm_password:
            st.error("비밀번호가 일치하지 않습니다.")
        else:
            register_user(username, password)
            st.success("회원가입이 완료되었습니다! 로그인하세요.")

# 로그아웃 기능
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

if __name__ == "__main__":
    main()
