import streamlit as st
import pandas as pd
import plotly.express as px

from analyzer import (
    expand_keywords,
    keyword_to_reviews
)

# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="천안 상권 분석", layout="wide")

st.title("🍝 천안 상권 방문 분석")

# =========================
# 데이터 로드
# =========================
df = pd.read_csv("data/reviews.csv")

df["text"] = df["text"].fillna("")
df["region"] = df["region"].fillna("기타")

# =========================
# 사이드바 필터
# =========================
st.sidebar.header("🔎 필터")

regions = ["전체"] + sorted(df["region"].unique().tolist())
region = st.sidebar.selectbox("지역 선택", regions)

if region != "전체":
    df = df[df["region"] == region]

# =========================
# KPI
# =========================
col1, col2 = st.columns(2)

col1.metric("📊 리뷰 수", len(df))
col2.metric("📍 지역", region)

st.divider()

# =========================
# 키워드 분석 (가로 그래프)
# =========================
st.subheader("📊 핵심 방문 키워드")

keyword_counts = expand_keywords(df)

data = keyword_counts.reset_index()
data.columns = ["keyword", "count"]

data = data.sort_values("count", ascending=True).tail(10)

fig = px.bar(
    data,
    x="count",
    y="keyword",
    orientation="h",
    text="count"
)

fig.update_layout(
    height=500,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="빈도",
    yaxis_title=""
)

st.plotly_chart(fig, use_container_width=True)

st.caption("※ 리뷰 기반 자동 키워드 분석")

st.divider()

# =========================
# 키워드 클릭 → 리뷰 보기
# =========================
st.subheader("🔍 키워드별 리뷰 보기")

mapping = keyword_to_reviews(df)

selected = st.selectbox("키워드 선택", list(mapping.keys()))

reviews = mapping[selected]

st.write(f"📝 총 {len(reviews)}개 리뷰")

for r in reviews[:30]:
    st.markdown(f"• {r}")

st.divider()

# =========================
# 전체 데이터
# =========================
st.subheader("📋 전체 데이터")

st.dataframe(df, use_container_width=True)
