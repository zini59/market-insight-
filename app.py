import streamlit as st
import pandas as pd

from analyzer import (
    expand_keywords,
    keyword_to_reviews
)

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="천안 상권 분석", layout="wide")

st.title("🧁 천안 상권 방문 분석")

# =========================
# 데이터 로드
# =========================
df = pd.read_csv("data/reviews.csv")

# 안전 처리
df["text"] = df["text"].fillna("")

# =========================
# 사이드바 필터
# =========================
st.sidebar.header("🔎 필터")

region_list = ["전체"] + sorted(df["region"].dropna().unique().tolist())
region = st.sidebar.selectbox("지역 선택", region_list)

if region != "전체":
    df = df[df["region"] == region]

# =========================
# KPI
# =========================
col1, col2 = st.columns(2)

col1.metric("📊 전체 리뷰 수", len(df))
col2.metric("📍 분석 지역", region)

st.divider()

# =========================
# 핵심 키워드 분석
# =========================
st.subheader("📊 핵심 방문 키워드")

keyword_counts = expand_keywords(df)

st.bar_chart(keyword_counts)

st.caption("※ 키워드는 실제 리뷰 문장을 기반으로 추출됩니다")

st.divider()

# =========================
# 키워드 클릭 → 리뷰 보기
# =========================
st.subheader("🔍 키워드별 실제 리뷰 보기")

mapping = keyword_to_reviews(df)

selected = st.selectbox("키워드 선택", list(mapping.keys()))

st.write("")

reviews = mapping[selected]

st.write(f"📝 총 {len(reviews)}개 리뷰")

for review in reviews[:30]:
    st.markdown(f"• {review}")

st.divider()

# =========================
# 전체 데이터 보기
# =========================
st.subheader("📋 전체 데이터")

st.dataframe(df, use_container_width=True)
