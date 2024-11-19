import streamlit as st

# 초기 상태 설정
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

st.title("온양고등학교 2025 고교학점제 강의평가록")
st.write("왼쪽 사이드바에서 페이지를 선택하세요.")

if st.session_state.logged_in:
    st.sidebar.success(f"안녕하세요, {st.session_state.username}님!")
else:
    st.sidebar.info("로그인이 필요합니다.")
