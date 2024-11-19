import streamlit as st
from pymongo import MongoClient
from datetime import datetime
import hashlib

# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["auth_demo"]  # 데이터베이스 이름 설정
users_collection = db["users"]  # 유저 정보를 저장할 컬렉션
posts_collection = db["posts"]  # 글 정보를 저장할 컬렉션

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

# 글 작성 함수
def save_post(username, title, content):
    post = {
        "username": username,
        "title": title,
        "content": content,
        "created_at": datetime.utcnow()
    }
    posts_collection.insert_one(post)

# Streamlit 애플리케이션
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""

    if st.session_state.logged_in:
        st.sidebar.success(f"안녕하세요, {st.session_state.username}님!")
        if st.sidebar.button("로그아웃"):
            logout()

        st.title("Streamlit 글 작성 및 저장")
        menu = st.radio("메뉴 선택", ["글 작성하기", "글 목록 보기"])

        if menu == "글 작성하기":
            write_post()
        elif menu == "글 목록 보기":
            view_posts()
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

# 글 작성 기능
def write_post():
    st.header("글 작성하기")
    title = st.text_input("제목")
    content = st.text_area("내용")
    if st.button("저장하기"):
        if title and content:
            save_post(st.session_state.username, title, content)
            st.success("글이 성공적으로 저장되었습니다!")
        else:
            st.error("제목과 내용을 모두 입력해주세요.")

# 글 목록 보기 기능
def view_posts():
    st.header("저장된 글 목록")
    posts = posts_collection.find()
    for post in posts:
        st.subheader(post["title"])
        st.write(f"**작성자:** {post['username']}")
        st.write(post["content"])
        st.write(f"_작성일: {post['created_at']}_")
        st.write("---")

if __name__ == "__main__":
    main()
