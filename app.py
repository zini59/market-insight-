import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="천안 상권 분석", layout="wide")

st.title("🍝 천안 상권 방문 분석")

# =========================
# 데이터 로드
# =========================
df = pd.read_csv("data/reviews.csv")

df["text"] = df["text"].fillna("")

# 🚨 region 강제 정리 (없으면 문제 생김)
if "region" not in df.columns:
    df["region"] = "천안 전체"

df["region"] = df["region"].fillna("천안 전체")

# =========================
# 🔥 핵심 키워드 생성
# =========================
def make_keywords(text):
    text = str(text)

    if any(w in text for w in ["점심", "식사", "맛집"]):
        return "🍝 점심/식사"

    if any(w in text for w in ["데이트", "분위기"]):
        return "💑 데이트"

    if any(w in text for w in ["혼밥"]):
        return "🍽 혼밥"

    if any(w in text for w in ["웨이팅"]):
        return "⏳ 웨이팅"

    return "📌 기타"


df["keyword"] = df["text"].apply(make_keywords)

# =========================
# 사이드바 (지역 필터 - 안전버전)
# =========================
st.sidebar.header("🔎 필터")

regions = ["전체"] + sorted(df["region"].dropna().unique().tolist())
region = st.sidebar.selectbox("지역", regions)

filtered_df = df.copy()

if region != "전체":
    filtered_df = filtered_df[filtered_df["region"] == region]

# =========================
# KPI
# =========================
col1, col2 = st.columns(2)

col1.metric("📊 전체 리뷰", len(df))
col2.metric("📍 필터 리뷰", len(filtered_df))

st.divider()

# =========================
# 그래프
# =========================
st.subheader("📊 키워드 분석")

kw = filtered_df["keyword"].value_counts().reset_index()
kw.columns = ["keyword", "count"]

fig = px.bar(
    kw,
    x="count",
    y="keyword",
    orientation="h",
    text="count"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# 리뷰 보기
# =========================
st.subheader("📝 리뷰 보기")

selected = st.selectbox("키워드 선택", filtered_df["keyword"].unique())

reviews = filtered_df[filtered_df["keyword"] == selected]["text"]

st.write(f"총 {len(reviews)}개")

for r in reviews:
    st.markdown(f"- {r}")

st.divider()

# =========================
# 전체 데이터
# =========================
st.subheader("📋 전체 데이터")

st.dataframe(filtered_df, use_container_width=True)
