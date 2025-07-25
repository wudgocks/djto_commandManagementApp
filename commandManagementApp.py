import streamlit as st
import pandas as pd

# 엑셀 파일 경로
EXCEL_PATH = "임원지시사항 관리 파일.xlsx"

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

# 앱 제목 및 페이지 설정
st.set_page_config(page_title="임원 지시사항 대시보드", layout="wide")
st.title("📋 임원지시사항 추진현황 대시보드")

# 데이터 불러오기
df = pd.read_excel(EXCEL_PATH)

# 추진율 숫자 변환 및 등급 계산
df["추진율"] = pd.to_numeric(df["추진율"], errors='coerce')
df["등급"] = df["추진율"].apply(get_grade)

# 출력할 컬럼 순서 지정
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
st.caption("※ 추진율 수치는 엑셀 파일에서 입력 후 자동 반영됩니다.")
