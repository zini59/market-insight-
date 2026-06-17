import requests

NAVER_ID = "IcKmtQv41oAWPQDGUhNT"
NAVER_SECRET = "NUbkh9S03S"


def naver_place_search(query):
    url = "https://openapi.naver.com/v1/search/local.json"

    headers = {
        "X-Naver-Client-Id": NAVER_ID,
        "X-Naver-Client-Secret": NAVER_SECRET
    }

    params = {
        "query": query,
        "display": 10,
        "sort": "comment"
    }

    res = requests.get(url, headers=headers, params=params)

    if res.status_code != 200:
        return {"error": res.text}

    data = res.json()

    # 👉 필요한 정보만 정리해서 반환
    results = []

    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "address": item.get("address"),
            "category": item.get("category")
        })

    return results
