import streamlit as st
import pandas as pd

from analyzer import classify_intent, structured_keywords, classify_age
from utils import filter_region, filter_date, filter_multi

st.set_page_config(page_title="상권 분석", layout="wide")

# ======================
# 데이터
# ======================
df = pd.read_csv("data/reviews.csv")

df["intent"] = df["text"].apply(classify_intent)
df["age"] = df["text"].apply(classify_age)

# ======================
# 사이드바 필터
# ======================
st.sidebar.title("🔎 필터")

region = st.sidebar.selectbox("지역", ["전체","신부동","터미널"])
days = st.sidebar.slider("최근 N일", 1, 30, 7)

kw1 = st.sidebar.text_input("키워드 1", "점심")
kw2 = st.sidebar.text_input("키워드 2", "파스타")

# 필터 적용
df = filter_region(df, region)
df = filter_date(df, days)

filtered_df = filter_multi(df, [kw1, kw2])

# ======================
# 헤더
# ======================
st.title("📊 상권 방문 목적 분석 대시보드")
st.caption("지역 기반 소비 목적 + 키워드 분석")

# ======================
# KPI 카드
# ======================
col1, col2, col3, col4 = st.columns(4)

col1.metric("총 데이터", len(df))
col2.metric("식사 비율", f"{(df['intent']=='식사/점심').mean()*100:.1f}%")
col3.metric("데이트 비율", f"{(df['intent']=='데이트').mean()*100:.1f}%")
col4.metric("대기 비율", f"{(df['intent']=='대기/카페').mean()*100:.1f}%")

st.divider()

# ======================
# 탭 구조
# ======================
tab1, tab2, tab3 = st.tabs(["📌 방문 목적", "🔑 키워드", "📋 데이터"])

# ----------------------
# TAB 1: 목적 분석
# ----------------------
with tab1:
    st.subheader("방문 목적 비율")

    intent_count = df["intent"].value_counts()
    st.bar_chart(intent_count)

# ----------------------
# TAB 2: 구조형 키워드
# ----------------------
with tab2:
    st.subheader("핵심 구조 키워드")

    keywords = structured_keywords(df)

    for k, v in keywords[:30]:
        st.write(f"**{k}** : {v}")

# ----------------------
# TAB 3: 데이터
# ----------------------
with tab3:
    st.subheader("필터된 데이터 (30개)")

    page = st.number_input("페이지", 1, 100, 1)
    size = 30

    start = (page-1)*size
    end = start + size

    st.dataframe(filtered_df.iloc[start:end], use_container_width=True)
