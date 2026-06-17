from collections import Counter
import re

# =========================
# 1. 기본 방문 목적
# =========================
def classify_intent(text):
    text = str(text)

    if any(w in text for w in ["점심", "식사", "먹", "혼밥"]):
        return "식사/점심"

    if any(w in text for w in ["데이트", "분위기", "연인"]):
        return "데이트"

    if any(w in text for w in ["카페", "시간", "대기", "기다"]):
        return "대기/카페"

    if any(w in text for w in ["터미널", "버스", "잠깐"]):
        return "이동"

    if any(w in text for w in ["회식", "모임", "술"]):
        return "회식"

    return "기타"


# =========================
# 2. 세부 방문 목적
# =========================
def intent_detail(text):
    text = str(text)

    if any(w in text for w in ["빨리", "급하게", "짧게"]):
        return "빠른 점심"

    if any(w in text for w in ["데이트", "분위기", "감성"]):
        return "분위기 점심"

    if any(w in text for w in ["터미널", "버스", "잠깐"]):
        return "이동형 식사"

    return "일반"


# =========================
# 3. 구조형 키워드
# =========================
def structured_keywords(df):
    results = []

    for _, row in df.iterrows():
        text = str(row["text"])
        intent = classify_intent(text)
        detail = intent_detail(text)
        region = row.get("region", "unknown")

        results.append(f"{intent}-{detail}-{region}")

    return Counter(results).most_common(30)


# =========================
# 4. 마케팅 추천
# =========================
def marketing_recommend(df):
    intent_ratio = df["intent"].value_counts(normalize=True)

    result = []

    if intent_ratio.get("식사/점심", 0) > 0.4:
        result.append("런치세트 / 빠른 회전 강조")

    if intent_ratio.get("데이트", 0) > 0.2:
        result.append("분위기 / 감성 마케팅 강화")

    if intent_ratio.get("대기/카페", 0) > 0.15:
        result.append("체류형 메뉴 / 음료 강화")

    return result


# =========================
# 5. 광고 문구 생성
# =========================
def ad_copy(df):
    intent_ratio = df["intent"].value_counts(normalize=True)

    ads = []

    if intent_ratio.get("식사/점심", 0) > 0.4:
        ads.append("✔ 15분 안에 나오는 런치 파스타")

    if intent_ratio.get("데이트", 0) > 0.2:
        ads.append("✔ 신부동 감성 데이트 맛집")

    if intent_ratio.get("대기/카페", 0) > 0.15:
        ads.append("✔ 커피 한잔하기 좋은 공간")

    return ads
