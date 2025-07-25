import streamlit as st
import pandas as pd

# 구글시트 CSV URL
csv_url = "https://docs.google.com/spreadsheets/d/1oYf6b2LaSxP3u6GR8FF2_aNlg1JE8grZdhguzmfDl6w/export?format=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(csv_url)
    return df

st.title("📋 임원 지시사항 대시보드")
df = load_data()

# 표시: 전체 테이블
st.dataframe(df, use_container_width=True)

# 예시 필터링
status_filter = st.selectbox("진행상황 필터", options=["전체"] + df['진행상황'].dropna().unique().tolist())
if status_filter != "전체":
    df = df[df['진행상황'] == status_filter]

st.write("🔎 필터링 결과:")
st.dataframe(df, use_container_width=True)
