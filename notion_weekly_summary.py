"""
This work is based on the information provided in https://developers.notion.com/reference/intro
The objective is to provide a summary for Notion records of what's done during the week.
"""

import requests
from datetime import date, timedelta

NOTION_TOKEN = "secret_"
DATABASE_ID = "7a15b146da9d46b48aa90bedaed2f597"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]

    # while data["has_more"] and get_all:
    #     payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
    #     url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    #     response = requests.post(url, json=payload, headers=headers)
    #     data = response.json()
    #     results.extend(data["results"])

    return results

def get_blocks(page_id, num_pages=None):
    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size={page_size}"

    response = requests.get(url=url, headers=headers)

    data = response.json()

    results = data["results"]
    
    return results

def get_weekly_summary(start_date, end_date):
    dates = []
    delta = timedelta(1)

    while start_date <= end_date:
        dates.append(str(start_date))
        start_date += delta

    # print(dates)

    results = set()

    pages = get_pages()

    for page in pages:
        page_id = page["id"]
        blocks = get_blocks(page_id)

        for block in blocks:
            # print(block['paragraph']['rich_text'][0]['text']['content'])
            if block['created_time'][:10] in dates:
                results.add(block['paragraph']['rich_text'][0]['text']['content'])

    return results

start_date = date(2023, 7, 3)
end_date = date(2023, 7, 7)

weekly_summary = get_weekly_summary(start_date, end_date)

print(*weekly_summary, sep='\n')
