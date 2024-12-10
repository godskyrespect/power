import streamlit as st
import base64
# 초기 상태 설정
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
    
st.set_page_config(page_title="공주고등학교 2025", page_icon="🏫")
st.snow()
st.sidebar.image("image.png", use_container_width=True)
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
        <h1>🏫 공주고등학교 2025</h1>
        <h3>고교학점제 도우미 사이트</h3>
    </div>
    """, unsafe_allow_html=True)

# st.markdown("""
#     <style>
#     body {
#         background-image: url('https://postfiles.pstatic.net/MjAyNDEyMTFfNjAg/MDAxNzMzODQ5MDIzNTc2.FXc5bjL9__B7jrwuP-IJa_nH6vI6er7flonBnXxPv9wg.Lwp-tERloyR0Tp2rsdnA4VNHg3hIKzpD55ePLlgczfkg.JPEG/image1.jpg?type=w3840');
#         background-size: cover; /* 이미지를 화면에 맞추기 */
#         background-position: center; /* 이미지 중앙에 위치 */
#         background-repeat: no-repeat; /* 이미지 반복 제거 */
#     }
#     .stApp {
#         background-image: url('https://postfiles.pstatic.net/MjAyNDEyMTFfNjAg/MDAxNzMzODQ5MDIzNTc2.FXc5bjL9__B7jrwuP-IJa_nH6vI6er7flonBnXxPv9wg.Lwp-tERloyR0Tp2rsdnA4VNHg3hIKzpD55ePLlgczfkg.JPEG/image1.jpg?type=w3840');
#         background-size: cover; /* 이미지를 화면에 맞추기 */
#         background-position: center; /* 이미지 중앙에 위치 */
#         background-repeat: no-repeat; /* 이미지 반복 제거 */
#     }
#     </style>
#     """, unsafe_allow_html=True)




# 배경 이미지를 설정하는 함수
def set_background(image_path):
    # 로컬 이미지를 Base64로 변환
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_image}");
            background-size: cover; /* 이미지를 화면에 맞추기 */
            background-position: center; /* 이미지 중앙에 위치 */
            background-repeat: no-repeat; /* 이미지 반복 제거 */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

image_path = "image1.png"  # 이미지 경로를 변경하세요
set_background(image_path)


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
    .center-message {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin-top: -250px; /* 화면 중심에서 조금 위로 올리기 */
    }
    .message-box {
        background-color: rgba(128, 128, 128, 0.8); /* 회색 상자 배경 (투명도 80%) */
        color: white; /* 글자 색상 */
        padding: 15px; /* 상자 내부 여백 */
        border-radius: 10px; /* 상자 모서리 둥글게 */
        text-align: center; /* 텍스트 중앙 정렬 */
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 그림자 효과 */
        font-size: 20px; /* 글자 크기 */
        font-weight: bold;
    }
    </style>
    <a href="https://teachrevolution.streamlit.app/" target="_blank">
        <button class="fixed-button">교사용 관리 페이지로 이동하기</button>
    </a>
    <div class="center-message">
        <div class="message-box">
            🎅 안녕하세요! 튜토리얼 산타홀애비에요~. 왼쪽에서 로그인을 먼저 해보세요! 
        </div>
    </div>
    """, unsafe_allow_html=True)

if st.session_state.logged_in:
    st.sidebar.success(f"안녕하세요, {st.session_state.name}님!")
else:
    st.sidebar.info("로그인이 필요합니다.")
