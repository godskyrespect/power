import streamlit as st
import pandas as pd
import altair as alt
from urllib.error import URLError
 
st.set_page_config(page_title="데이터프레임 분석", page_icon="📊")
 
st.markdown("# 농작물 총생산 데이터 분석 ")
st.sidebar.header("농작물 총생산 데이터 분석")
st.write(
    """농작물 총생산 데이터 분석. 1961~2007.
(다음 데이터를 참고함. [UN Data Explorer](http://data.un.org/Explorer.aspx).)"""
)
 
 
@st.cache_data
def get_UN_data():
    AWS_BUCKET_URL = "http://streamlit-demo-data.s3-us-west-2.amazonaws.com"
    df = pd.read_csv(AWS_BUCKET_URL + "/agri.csv.gz")
    return df.set_index("Region")
 
 
try:
    df = get_UN_data()
    countries = st.multiselect(
        "나라를 선택하시오.", list(df.index), ["China", "United States of America"]
    )
    if not countries:
        st.error("Please select at least one country.")
    else:
        data = df.loc[countries]
        data /= 1000000.0
        st.write("### 농작물 총생산 ($10억 달러 단위)", data.sort_index())
 
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=["index"]).rename(
            columns={"index": "year", "value": "Gross Agricultural Product ($B)"}
        )
        chart = (
            alt.Chart(data)
            .mark_area(opacity=0.3)
            .encode(
                x="year:T",
                y=alt.Y("Gross Agricultural Product ($B):Q", stack=None),
                color="Region:N",
            )
        )
        st.altair_chart(chart, use_container_width=True)
except URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )