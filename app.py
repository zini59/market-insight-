import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 페이지 설정
# =========================
st.set_page_config(page_title="상권 분석", layout="wide")

st.title("🍝 천안 상권 방문 분석")

# =========================
# 데이터 로드
# =========================
df = pd.read_csv("data/reviews.csv")

df["text"] = df["text"].fillna("")
df["region"] = df["region"].fillna("기타")

# =========================
# 🔥 app에서만 키워드 생성 (핵심)
# =========================
def make_keywords(text):
    text = str(text)

    if any(w in text for w in ["빠르게", "급하게", "점심"]):
        return "⚡ 빠른 점심"

    if any(w in text for w in ["데이트", "분위기", "감성"]):
        return "💑 데이트"

    if any(w in text for w in ["혼밥", "혼자"]):
        return "🍽 혼밥"

    if any(w in text for w in ["웨이팅", "기다림"]):
        return "⏳ 웨이팅"

    if any(w in text for w in ["가성비", "저렴"]):
        return "💰 가성비"

    return "📌 기타"


# =========================
# 키워드 컬럼 생성 (app에서만)
# =========================
df["keyword"] = df["text"].apply(make_keywords)

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
# 📊 가로 그래프 (완전 수정)
# =========================
st.subheader("📊 핵심 방문 키워드")

keyword_counts = df["keyword"].value_counts().reset_index()
keyword_counts.columns = ["keyword", "count"]

keyword_counts = keyword_counts.sort_values("count", ascending=True)

fig = px.bar(
    keyword_counts,
    x="count",
    y="keyword",
    orientation="h",
    text="count"
)

fig.update_layout(
    height=500,
    yaxis_title="",
    xaxis_title="빈도",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# 🔍 클릭 → 리뷰 보기 (app에서 해결)
# =========================
st.subheader("🔍 키워드별 리뷰 보기")

selected = st.selectbox("키워드 선택", df["keyword"].unique())

filtered_reviews = df[df["keyword"] == selected]["text"]

st.write(f"📝 총 {len(filtered_reviews)}개")

for r in filtered_reviews[:30]:
    st.markdown(f"• {r}")

st.divider()

# =========================
# 전체 데이터
# =========================
st.subheader("📋 전체 데이터")

st.dataframe(df, use_container_width=True)
