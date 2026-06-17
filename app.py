import streamlit as st
import pandas as pd

from analyzer import (
    classify_intent,
    intent_detail,
    structured_keywords,
    marketing_recommend,
    ad_copy,
    advanced_intent
)

from naver_api import naver_place_search

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="상권 분석 대시보드", layout="wide")

st.title("📊 상권 방문 목적 분석 시스템")
st.caption("지역 + 기간 + 방문 목적 기반 분석")

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
# 사이드바 필터
# =========================
st.sidebar.header("🔎 필터")

region = st.sidebar.selectbox("지역", ["전체", "신부동", "터미널"])
days = st.sidebar.slider("최근 N일 (미구현 데이터 기준)", 1, 30, 7)

kw1 = st.sidebar.text_input("키워드 1", "점심")
kw2 = st.sidebar.text_input("키워드 2", "파스타")

# =========================
# 지역 필터 (간단 버전)
# =========================
if region != "전체":
    df = df[df["region"] == region]

# =========================
# KPI
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("총 데이터", len(df))
col2.metric("식사 비율", f"{(df['intent']=='식사/점심').mean()*100:.1f}%")
col3.metric("데이트 비율", f"{(df['intent']=='데이트').mean()*100:.1f}%")
col4.metric("대기 비율", f"{(df['intent']=='대기/카페').mean()*100:.1f}%")

st.divider()

# =========================
# 탭 구조
# =========================
tab1, tab2, tab3 = st.tabs(["📌 방문 목적", "🧠 세부 분석", "📋 데이터"])

# -------------------------
# TAB 1
# -------------------------
with tab1:
    st.subheader("방문 목적 분포")
    st.bar_chart(df["intent"].value_counts())

# -------------------------
# TAB 2
# -------------------------
with tab2:
    st.subheader("세부 방문 목적")

    st.bar_chart(df["detail"].value_counts())

    st.subheader("📌 마케팅 추천")

    for r in marketing_recommend(df):
        st.write("👉", r)

    st.subheader("📌 광고 문구")

    for ad in ad_copy(df):
        st.write("✍️", ad)

# -------------------------
# TAB 3
# -------------------------
with tab3:
    st.subheader("원본 데이터")

    page = st.number_input("페이지", 1, 100, 1)
    size = 30

    start = (page - 1) * size
    end = start + size

    st.dataframe(df.iloc[start:end], use_container_width=True)

# =========================
# 키워드 구조 분석
# =========================
st.divider()

st.subheader("🔑 구조형 키워드 (상권 패턴)")

keywords = structured_keywords(df)

for k, v in keywords[:30]:
    st.write(f"**{k}** → {v}")
