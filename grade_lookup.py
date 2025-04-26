import os
import streamlit as st
import pandas as pd
from datetime import date

# ——— 접속 만료일 설정 ———
EXPIRE_DATE = date(2025, 4, 30)

# ——— 0) 만료일 체크 ———
today = date.today()
if today > EXPIRE_DATE:
    st.error(f"이 성적 조회 시스템은 {EXPIRE_DATE} 이후로 접속이 불가합니다.")
    st.stop()

# ——— 1) 데이터 불러오기 (인코딩 폴백 + zfill) ———
@st.cache_data
def load_data():
    for enc in ("utf-8-sig", "utf-8", "cp949"):
        try:
            df = pd.read_csv("scores.csv", dtype=str, encoding=enc)
            df["password"] = df["password"].astype(str).str.zfill(5)
            return df
        except UnicodeDecodeError:
            continue
    st.error("scores.csv 파일을 읽는 중 인코딩 오류가 발생했습니다.")
    st.stop()

df = load_data()

# ——— 2) submissions 디렉터리 준비 ———
SUBMISSION_DIR = "submissions"
os.makedirs(SUBMISSION_DIR, exist_ok=True)

# ——— 3) UI 헤더 ———
st.subheader("성적 조회")

# ——— 4) 입력 폼 ———
sid  = st.text_input("학번", max_chars=7)
name = st.text_input("이름")
pwd  = st.text_input("비밀번호", type="password", max_chars=5)

# ——— 5) 조회 버튼 & 처리 ———
if st.button("조회"):
    if not sid.isdigit():
        st.error("학번은 숫자만 입력해야 합니다.")
    elif not (pwd.isalnum() and len(pwd) == 5):
        st.error("비밀번호는 5자리여야 합니다.")
    else:
        match = df[
            (df["student_id"] == sid) &
            (df["name"]       == name) &
            (df["password"]   == pwd)
        ]
        if not match.empty:
            score_str = match.iloc[0]["score"]
            st.success(f"{name}({sid}) 학생의 성적은 **{score_str}점** 입니다.")
        else:
            st.error("입력하신 정보가 일치하지 않거나 등록된 사용자가 아닙니다.")
