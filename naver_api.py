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

    # 오류 체크 (중요)
    if res.status_code != 200:
        return {"error": res.text}

    return res.json()