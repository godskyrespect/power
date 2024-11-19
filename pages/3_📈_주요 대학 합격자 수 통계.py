import streamlit as st
import time
import numpy as np

st.set_page_config(page_title="주요대학 합격수 통계", page_icon="📈")

st.markdown("서울대 합격자 수")
st.sidebar.header("서울대 합격자 수")
st.write(
    """우리학교 창립 이래 약 500년간 서울대 합격자 수 입니다."""
)

progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")