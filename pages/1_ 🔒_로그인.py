import streamlit as st
from pymongo import MongoClient
import hashlib

st.set_page_config(page_title="로그인", page_icon="🔒")

# 세션 상태 초기화
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "name" not in st.session_state:
    st.session_state.name = ""
# 없앨 예정
st.info("로그인 창입니다. ID:10101, 비밀번호 : 1234", icon="🎅")
# MongoDB 연결 설정
MONGO_URI = "mongodb+srv://jsheek93:j103203j@cluster0.7pdc1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(MONGO_URI)
db = client["user_database"]
users_collection = db["student"]

# 비밀번호 해시 함수
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 사용자 인증 함수
def authenticate_user(student_id, password):
    user = users_collection.find_one({"학번": student_id})
    if user and user["password"] == hash_password(password):
        return user
    return None

# 사용자 등록 함수
def register_user(student_id, password, name):
    users_collection.insert_one({
        "학번": student_id,
        "password": hash_password(password),
        "이름": name
    })

# HTML 및 CSS 스타일 적용
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

# 페이지 제목
st.markdown('<h2 style="text-align: center;">온양고등학교 2025 고교학점제 수강신천 <span style="font-size: small;">교수님</span></h2>', unsafe_allow_html=True)
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
            st.success(f"환영합니다, {user['이름']}님!")
        else:
            st.error("학번 또는 비밀번호가 잘못되었습니다.")
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 사이드바에 사용자 정보 표시
if st.session_state.logged_in:
    with st.sidebar:
        st.write(f"학번: {st.session_state.student_id}")
        st.write(f"이름: {st.session_state.name}")
        if st.button("로그아웃"):
            st.session_state.logged_in = False
            st.session_state.student_id = ""
            st.session_state.name = ""
            st.success("로그아웃되었습니다.")
