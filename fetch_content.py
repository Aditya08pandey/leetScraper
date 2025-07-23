import requests
from config import LEETCODE_SESSION, USER_AGENT

HEADERS = {
    "Content-Type": "application/json",
    "Referer":      "https://leetcode.com",
    "cookie":       f"LEETCODE_SESSION={LEETCODE_SESSION}",
    "User-Agent":   USER_AGENT
}

GRAPHQL_URL = "https://leetcode.com/graphql"
QUERY = """
query getQuestionDetail($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    content
    topicTags { name }
  }
}
"""

def fetch_content(slug):
    payload = {"query": QUERY, "variables": {"titleSlug": slug}}
    res = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
    res.raise_for_status()
    d = res.json()["data"]["question"]
    return d["content"], [t["name"] for t in d["topicTags"]]


