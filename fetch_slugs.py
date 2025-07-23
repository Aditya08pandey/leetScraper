import requests

def get_all_slugs():
    url = "https://leetcode.com/api/problems/all/"
    res = requests.get(url)
    res.raise_for_status()
    arr = res.json()["stat_status_pairs"]
   
    diff_map = {1: "Easy", 2: "Medium", 3: "Hard"}
    out = []
    for e in arr:
        if e["paid_only"]:
            continue 
        out.append({
            "question_id": e["stat"]["frontend_question_id"],
            "slug":        e["stat"]["question__title_slug"],
            "title":       e["stat"]["question__title"],
            "difficulty":  diff_map[e["difficulty"]["level"]]
        })
    return out
