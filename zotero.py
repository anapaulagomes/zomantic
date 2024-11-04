import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def get_items_added_from(api_key, user_id, start_date):
    url = f"https://api.zotero.org/users/{user_id}/items"
    headers = {
        "Zotero-API-Key": api_key
    }
    params = {
        "since": start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "format": "json"
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_items_added_this_week(api_key):
    user_id = os.getenv("ZOTERO_USER_ID")
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday())
    return get_items_added_from(api_key, user_id, start_of_week)
