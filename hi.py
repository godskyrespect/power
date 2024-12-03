import streamlit as st

# 초기 상태 설정
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# 제목 설정
st.markdown("# 🏫 온양고등학교 2025\n### 고교학점제 강의평가록")

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
