from collections import Counter

# =========================
# 방문 목적 분석
# =========================
def classify_intent(text):
    text = str(text)

    if "점심" in text or "식사" in text or "맛집" in text:
        return "식사/점심"

    if "데이트" in text or "분위기" in text:
        return "데이트"

    if "카페" in text or "대기" in text:
        return "대기/카페"

    if "터미널" in text or "버스" in text:
        return "이동"

    return "기타"


# =========================
# 세부 목적 분석
# =========================
def intent_detail(text):
    text = str(text)

    if "빨리" in text or "급하게" in text:
        return "빠른 점심"

    if "감성" in text or "분위기" in text:
        return "감성 데이트"

    if "오래" in text or "카페" in text:
        return "장시간 체류"

    return "일반"


# =========================
# 패턴 분석
# =========================
def structured_keywords(df):
    result = []

    for _, row in df.iterrows():
        text = str(row["text"])
        region = row.get("region", "unknown")

        intent = classify_intent(text)
        detail = intent_detail(text)

        result.append(f"{intent}-{detail}-{region}")

    return Counter(result).most_common(30)


# =========================
# 마케팅 추천
# =========================
def marketing_recommend(df):
    r = df["intent"].value_counts(normalize=True)

    out = []

    if r.get("식사/점심", 0) > 0.4:
        out.append("런치 메뉴 강화 + 회전율 전략")

    if r.get("데이트", 0) > 0.2:
        out.append("감성/데이트 마케팅 강화")

    if r.get("대기/카페", 0) > 0.15:
        out.append("체류형 메뉴 강화")

    return out


# =========================
# 광고 문구 생성
# =========================
def ad_copy(df):
    r = df["intent"].value_counts(normalize=True)

    ads = []

    if r.get("식사/점심", 0) > 0.4:
        ads.append("15분 런치 파스타")

    if r.get("데이트", 0) > 0.2:
        ads.append("신부동 감성 데이트 맛집")

    if r.get("대기/카페", 0) > 0.15:
        ads.append("편하게 머무는 공간")

    return ads
