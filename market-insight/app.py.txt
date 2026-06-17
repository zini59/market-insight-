import streamlit as st
import pandas as pd
from analyzer import classify_purpose, structured_keywords, extract_keywords

st.title("📊 상권 방문 구조 분석기")

df = pd.read_csv("data/reviews.csv")

# -----------------------
# 분석
# -----------------------
df["purpose"] = df["text"].apply(classify_purpose)

# -----------------------
# 1. 목적 분포
# -----------------------
st.subheader("📌 방문 목적")

st.bar_chart(df["purpose"].value_counts())

# -----------------------
# 2. 구조형 키워드
# -----------------------
st.subheader("📌 구조형 키워드 (핵심)")

structured = structured_keywords(df)

for k, v in structured:
    st.write(f"{k} : {v}")

# -----------------------
# 3. 일반 키워드
# -----------------------
st.subheader("📌 일반 키워드")

keywords = extract_keywords(df["text"].tolist())
st.write(keywords)