import random

import requests
from dotenv import load_dotenv
import os

import time

load_dotenv()


def get_paper_ids(items):
    """Search for a paper on Semantic Scholar and return its ID and title.
    The API returns up to 500 papers at time."""
    items_paper_ids = {}
    for zotero_key, item in items.items():
        response = requests.get(
            f'https://api.semanticscholar.org/graph/v1/paper/search/match?'
            f'query={item["data"]["title"]}&fields=title,paperId',
        )
        if response.ok:
            data = response.json()
            if data:
                paper_id = data['data'][0].get('paperId')
                items_paper_ids[zotero_key] = {
                    'paper_id': paper_id,
                    'item': item
                }
    return items_paper_ids


def store_papers_in_semantic_scholar_library(papers, session, collection_folder_ids=None):
    """Save papers to the Semantic Scholar library, placing each in its matching folder(s).

    collection_folder_ids: {collection_name: ss_folder_id} mapping.
    papers: each entry may include 'collection_keys' (list of Zotero collection keys)
            and the caller provides a collections dict {key: name} to resolve names.
    """
    if collection_folder_ids is None:
        collection_folder_ids = {}

    print(f'Attempt to store {len(papers)} items...')
    count = 0

    for paper in papers:
        print(paper['title'])
        folder_ids = paper.get('folder_ids', [])
        response = save_paper_to_library(paper['paper_id'], paper['title'], session, folder_ids=folder_ids)
        if response.ok:
            count += 1
        time.sleep(random.randint(1, 3))

    print(f'Finished saving papers to Semantic Scholar Library. Attempted to save {count} papers.')
    print('Check them out: https://www.semanticscholar.org/me/library/all')


def login():
    session = requests.Session()

    url = "https://www.semanticscholar.org"
    session.get(url)

    login_url = "https://www.semanticscholar.org/api/1/auth/cognito/login"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0",
        "Content-Type": "application/json",
        "X-S2-UI-Version": "8c3d74bcd9b3357febf74868a2a34ed576c6fd0b",
        "X-S2-Client": "webapp-browser",
        "Origin": "https://www.semanticscholar.org",
        "Referer": "https://www.semanticscholar.org/",
    }
    data = {
        "email": os.getenv("SEMANTIC_SCHOLAR_LOGIN"),
        "password": os.getenv("SEMANTIC_SCHOLAR_PASSWORD"),
    }

    response = session.post(login_url, headers=headers, json=data)
    response.raise_for_status()
    return session


_HEADERS = {
    "Host": "www.semanticscholar.org",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Accept": "*/*",
    "Accept-Language": "pt-BR,en-US;q=0.8,en;q=0.5,de;q=0.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Prefer": "safe",
    "Cache-Control": "no-cache,no-store,must-revalidate,max-age=-1",
    "Content-Type": "application/json",
    "X-S2-UI-Version": "8c3d74bcd9b3357febf74868a2a34ed576c6fd0b",
    "X-S2-Client": "webapp-browser",
    "Origin": "https://www.semanticscholar.org",
    "Referer": "https://www.semanticscholar.org/api/1/library/folders/entries/bulk",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0",
    "TE": "trailers",
}


def get_or_create_folder(folder_name, session):
    url = (
        "https://www.semanticscholar.org/api/1/library/folders"
        "?entrySourceTypeFilter=AuthorLibraryFolder&entrySourceTypeFilter=Library"
        "&entrySourceTypeFilter=Feed&folderSourceTypeFilter=AllPapers"
        "&folderSourceTypeFilter=AuthorLibraryFolder&folderSourceTypeFilter=Feed"
        "&folderSourceTypeFilter=Library"
    )
    folders = session.get(url, headers=_HEADERS).json().get("folders", [])
    for folder in folders:
        if folder["name"] == folder_name:
            return folder["id"]

    response = session.post(
        "https://www.semanticscholar.org/api/1/library/folders",
        json={"name": folder_name, "recommendationStatus": "On"},
        headers=_HEADERS,
    )
    return response.json()["folder"]["id"]


def save_paper_to_library(paper_id, paper_title, session, folder_ids=None):
    if folder_ids is None:
        folder_ids = []
    url = "https://www.semanticscholar.org/api/1/library/folders/entries/bulk"
    data = {
        "paperId": paper_id,
        "paperTitle": paper_title,
        "folderIds": folder_ids,
        "annotationState": None,
        "sourceType": "Library"
    }

    response = session.post(url, headers=_HEADERS, json=data)
    print(f"Status Code: {response.status_code}")
    return response
