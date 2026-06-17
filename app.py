import streamlit as st
import pandas as pd
import plotly.express as px

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
# 날짜 처리 (기간 필터)
# =========================
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    st.sidebar.subheader("📅 기간 선택")

    min_date = df["date"].min()
    max_date = df["date"].max()

    if pd.notnull(min_date) and pd.notnull(max_date):
        date_range = st.sidebar.date_input(
            "기간",
            [min_date, max_date]
        )

        if len(date_range) == 2:
            start, end = date_range
            df = df[(df["date"] >= pd.to_datetime(start)) &
                    (df["date"] <= pd.to_datetime(end))]

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
# 🔥 키워드 생성 (app 내부 처리)
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

    if any(w in text for w in ["재방문", "또", "자주"]):
        return "🔁 재방문"

    return "📌 기타"


df["keyword"] = df["text"].apply(make_keywords)

# =========================
# 📊 키워드 그래프 (가로)
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
    xaxis_title="빈도",
    yaxis_title="",
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# =========================
# 🔍 클릭 → 리뷰 보기
# =========================
st.subheader("🔍 키워드별 리뷰 보기")

selected = st.selectbox("키워드 선택", df["keyword"].unique())

filtered_reviews = df[df["keyword"] == selected]["text"]

st.write(f"📝 총 {len(filtered_reviews)}개 리뷰")

for r in filtered_reviews:
    st.markdown(f"• {r}")

st.divider()

# =========================
# 📋 전체 데이터
# =========================
st.subheader("📋 전체 데이터")

st.dataframe(df, use_container_width=True)
