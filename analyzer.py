from collections import Counter

# =========================
# 1. 방문 목적 (고도화)
# =========================
def advanced_intent(text):
    text = str(text)

    # 직장인 점심
    if "점심" in text and "빠르게" in text:
        return "직장인 빠른 점심"

    # 일반 점심
    if "점심" in text:
        return "점심 식사"

    # 데이트
    if "데이트" in text or "분위기" in text:
        return "감성 데이트"

    # 카페 체류
    if "카페" in text or "오래" in text:
        return "장시간 체류"

    # 이동
    if "터미널" in text or "기다림" in text:
        return "이동 대기 소비"

    # 혼밥
    if "혼밥" in text:
        return "개인 식사"

    return "기타"


# =========================
# 2. 구조 키워드
# =========================
def structured_keywords(df):
    result = []

    for _, row in df.iterrows():
        text = str(row["text"])
        region = row.get("region", "unknown")

        intent = advanced_intent(text)

        result.append(f"{intent}-{region}")

    return Counter(result).most_common(30)


# =========================
# 3. 마케팅 추천
# =========================
def marketing_recommend(df):
    r = df["intent"].value_counts(normalize=True)

    out = []

    if r.get("점심 식사", 0) > 0.4:
        out.append("런치 메뉴 + 회전율 중심 광고 필요")

    if r.get("감성 데이트", 0) > 0.2:
        out.append("감성/데이트 광고 강화 필요")

    if r.get("장시간 체류", 0) > 0.15:
        out.append("음료/디저트 강화 필요")

    return out


# =========================
# 4. 광고 문구
# =========================
def ad_copy(df):
    r = df["intent"].value_counts(normalize=True)

    ads = []

    if r.get("점심 식사", 0) > 0.4:
        ads.append("✔ 빠르게 나오는 점심 파스타")

    if r.get("감성 데이트", 0) > 0.2:
        ads.append("✔ 신부동 감성 데이트 맛집")

    if r.get("장시간 체류", 0) > 0.15:
        ads.append("✔ 오래 머물기 좋은 카페 분위기")

    return ads
