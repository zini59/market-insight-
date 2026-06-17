import streamlit as st
import pandas as pd

from analyzer import (
    classify_intent,
    intent_detail,
    structured_keywords,
    marketing_recommend,
    ad_copy
)

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="상권 분석", layout="wide")

st.title("📊 천안 상권 방문 목적 분석")

# =========================
# 데이터 로드
# =========================
df = pd.read_csv("data/reviews.csv")

# =========================
# 분석 컬럼 생성
# =========================
df["intent"] = df["text"].apply(classify_intent)
df["detail"] = df["text"].apply(intent_detail)

# =========================
# 필터
# =========================
region = st.sidebar.selectbox(
    "지역",
    ["전체", "신부동", "불당동", "두정동", "쌍용동"]
)

if region != "전체":
    df = df[df["region"] == region]

# =========================
# KPI
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("전체 데이터", len(df))
col2.metric("식사 비율", f"{(df['intent']=='식사/점심').mean()*100:.1f}%")
col3.metric("데이트 비율", f"{(df['intent']=='데이트').mean()*100:.1f}%")

st.divider()

# =========================
# 방문 목적 분석
# =========================
st.subheader("📊 방문 목적 분포")
st.bar_chart(df["intent"].value_counts())

# =========================
# 세부 분석
# =========================
st.subheader("🧠 세부 방문 목적")
st.bar_chart(df["detail"].value_counts())

# =========================
# 마케팅 추천
# =========================
st.subheader("💰 마케팅 추천")

for r in marketing_recommend(df):
    st.write("👉", r)

# =========================
# 광고 문구
# =========================
st.subheader("✍️ 광고 문구")

for ad in ad_copy(df):
    st.write("✔", ad)

# =========================
# 데이터 보기
# =========================
st.subheader("📋 데이터")

st.dataframe(df)
