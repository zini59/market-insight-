from collections import Counter
import re

STOPWORDS = ["은","는","이","가","을","를","에","에서","하다"]

# 1. 목적 분류 (상위)
def classify_purpose(text):
    text = str(text)

    if "점심" in text or "먹" in text or "식사" in text:
        return "점심"

    if "데이트" in text:
        return "데이트"

    if "카페" in text or "시간" in text or "대기" in text:
        return "대기"

    if "팝업" in text:
        return "팝업"

    return "기타"


# 2. 카테고리 분류 (중간)
def classify_category(text):
    text = str(text)

    if "파스타" in text or "리조또" in text:
        return "파스타"

    if "카페" in text:
        return "카페"

    if "레스토랑" in text or "이탈리안" in text:
        return "레스토랑"

    if "터미널" in text:
        return "터미널"

    return "기타"


# 3. 키워드 구조 생성
def structured_keywords(df):
    results = []

    for _, row in df.iterrows():
        text = str(row["text"])

        purpose = classify_purpose(text)
        category = classify_category(text)
        place = row.get("region", "unknown")

        results.append(f"{purpose}-{category}-{place}")

    return Counter(results).most_common(30)


# 4. 일반 키워드 (보조)
def extract_keywords(texts):
    words = []

    for t in texts:
        tokens = re.findall(r'\w+', str(t))
        words.extend([w for w in tokens if w not in STOPWORDS])

    return Counter(words).most_common(20)