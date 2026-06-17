import requests

NAVER_ID = "YOUR_CLIENT_ID"
NAVER_SECRET = "YOUR_CLIENT_SECRET"

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

    return res.json()