from collections import Counter
import re

# =========================
# 핵심 키워드 추출 (개선)
# =========================
def extract_keywords(text):
    text = str(text)

    keywords = []

    if any(w in text for w in ["빠르게", "급하게", "점심시간"]):
        keywords.append("⚡ 빠른 점심")

    if any(w in text for w in ["데이트", "분위기", "감성"]):
        keywords.append("💑 데이트 장소")

    if any(w in text for w in ["혼밥", "혼자"]):
        keywords.append("🍽 혼밥")

    if any(w in text for w in ["웨이팅", "기다림"]):
        keywords.append("⏳ 웨이팅")

    if any(w in text for w in ["가성비", "저렴"]):
        keywords.append("💰 가성비")

    if any(w in text for w in ["재방문", "또", "자주"]):
        keywords.append("🔁 재방문")

    if not keywords:
        keywords.append("📌 일반 방문")

    return keywords


# =========================
# 데이터 펼치기 (핵심)
# =========================
def expand_keywords(df):
    all_keywords = []

    for _, row in df.iterrows():
        text = str(row["text"])
        kws = extract_keywords(text)

        for k in kws:
            all_keywords.append(k)

    return Counter(all_keywords)


# =========================
# 리뷰 매핑 (클릭용)
# =========================
def keyword_to_reviews(df):
    mapping = {}

    for _, row in df.iterrows():
        text = str(row["text"])
        kws = extract_keywords(text)

        for k in kws:
            if k not in mapping:
                mapping[k] = []
            mapping[k].append(text)

    return mapping
