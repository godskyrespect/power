import streamlit as st

# 초기 상태 설정
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
hide_github_icon = """
#GithubIcon {
  visibility: hidden;
}
"""
st.markdown(hide_github_icon, unsafe_allow_html=True)

# 제목 설정
st.markdown("""
    <style>
    .title-container {
        background-color: rgba(0, 0, 0, 0.6); /* 검은 배경 (투명도 60%) */
        color: white; /* 흰 글씨 */
        padding: 15px; /* 여백 추가 */
        border-radius: 10px; /* 모서리 둥글게 */
        text-align: center; /* 중앙 정렬 */
        max-width: 600px; /* 컨테이너 최대 너비 설정 */
        margin: 0 auto; /* 가운데 정렬을 위한 마진 설정 */
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.3); /* 부드러운 그림자 효과 */
    }
    </style>
    <div class="title-container">
        <h1>🏫 온양고등학교 2025</h1>
        <h3>고교학점제 강의평가록</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    body {
        background-image: url('https://lh3.googleusercontent.com/p/AF1QipPNcGXtel6eVAQ-5Zi6bePQ5CdzCCHQ3UBuzONO=s1360-w1360-h1020');
        background-size: cover; /* 이미지를 화면에 맞추기 */
        background-position: center; /* 이미지 중앙에 위치 */
        background-repeat: no-repeat; /* 이미지 반복 제거 */
    }
    .stApp {
        background-image: url('https://lh3.googleusercontent.com/p/AF1QipPNcGXtel6eVAQ-5Zi6bePQ5CdzCCHQ3UBuzONO=s1360-w1360-h1020');
        background-size: cover; /* 이미지를 화면에 맞추기 */
        background-position: center; /* 이미지 중앙에 위치 */
        background-repeat: no-repeat; /* 이미지 반복 제거 */
    }
    </style>
    """, unsafe_allow_html=True)

# HTML과 CSS를 이용해 우측 하단에 스타일이 적용된 버튼 배치
st.markdown("""
    <style>
    .fixed-button {
        position: fixed;
        bottom: 50px;
        right: 50px;
        background-color: #4CAF50; /* 녹색 배경 */
        color: white; /* 글자 색상 */
        border: none; /* 테두리 제거 */
        border-radius: 12px; /* 모서리를 둥글게 */
        padding: 12px 24px; /* 패딩 추가 */
        font-size: 16px; /* 글자 크기 */
        cursor: pointer; /* 커서를 포인터로 변경 */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 그림자 효과 */
        transition: all 0.3s ease; /* 부드러운 전환 효과 */
    }
    .fixed-button:hover {
        background-color: #45a049; /* 마우스 오버 시 배경색 변경 */
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.2); /* 마우스 오버 시 그림자 증가 */
    }
    </style>
    <a href="https://teachersite-3s3va6sj5zdegscdyqky3t.streamlit.app/" target="_blank">
        <button class="fixed-button">교사용 관리 페이지로 이동하기</button>
    </a>
    """, unsafe_allow_html=True)


if st.session_state.logged_in:
    st.sidebar.success(f"안녕하세요, {st.session_state.username}님!")
else:
    st.sidebar.info("로그인이 필요합니다.")
