import requests

def get_recommendations(api_key, paper_ids):
    url = "https://api.semanticscholar.org/recommendations/v1/papers"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    data = {
        "positivePaperIds": paper_ids,
        "fieldsOfStudy": ["Computer Science"]
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
