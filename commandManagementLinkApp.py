import streamlit as st
import pandas as pd

# 구글스프레드시트 CSV URL (export 링크)
CSV_URL = "https://docs.google.com/spreadsheets/d/1oYf6b2LaSxP3u6GR8FF2_aNlg1JE8grZdhguzmfDl6w/export?format=csv"

# 등급 계산 함수
def get_grade(rate):
    try:
        rate = float(rate)
        if rate < 50:
            return '하'
        elif rate < 80:
            return '중'
        else:
            return '상'
    except:
        return '미입력'

# 등급 컬럼 색칠 함수
def highlight_grade_col(s):
    return ['background-color: green; color: white; font-weight: bold' if v == '상' else
            'background-color: orange; color: white; font-weight: bold' if v == '중' else
            'background-color: red; color: white; font-weight: bold' if v == '하' else ''
            for v in s]

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(CSV_URL)
    return df

st.set_page_config(page_title="임원 지시사항 대시보드", layout="wide")
st.title("📋 임원지시사항 추진현황 대시보드")

df = load_data()

# 추진율 숫자 변환 및 등급 계산
df["추진율"] = pd.to_numeric(df["추진율"], errors='coerce')
df["등급"] = df["추진율"].apply(get_grade)

# 출력할 컬럼 순서 지정 (구글시트 컬럼명과 맞는지 확인 필요)
columns_to_show = ["관리번호", "일시", "분류", "주요내용", "추진율", "등급"]
df_display = df[columns_to_show]

# 등급별 건수 요약
st.subheader("✅ 추진 등급별 현황 요약")
col1, col2, col3 = st.columns(3)
col1.metric("상 (80~100%)", (df["등급"] == "상").sum())
col2.metric("중 (50~79%)", (df["등급"] == "중").sum())
col3.metric("하 (0~49%)", (df["등급"] == "하").sum())

st.markdown("---")

# 등급별 필터링
selected_grade = st.selectbox("등급별로 보기", ["전체", "상", "중", "하"])
if selected_grade != "전체":
    df_display = df_display[df_display["등급"] == selected_grade]

# 스타일 적용 후 테이블 출력
st.subheader("📄 지시사항 목록")
st.dataframe(df_display.style.apply(highlight_grade_col, subset=["등급"]), use_container_width=True)

# 참고 안내
st.caption("※ 추진율 수치는 구글 스프레드시트에서 입력 후 자동 반영됩니다.")
