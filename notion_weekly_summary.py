"""
This work is based on the information provided in https://developers.notion.com/reference/intro
The objective is to provide a summary for Notion records of what's done during the week.
"""

import requests

NOTION_TOKEN = "secret_"
DATABASE_ID = "7a15b146da9d46b48aa90bedaed2f597"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

# As of Jul 4, 2023, get_pages retrieves all the records not just those of specific week. Extra parameters such as start_date and end_date are to be added for that functionality.
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

pages = get_pages()

weekly_summary = set()

for page in pages:
    page_id = page["id"]
    blocks = get_blocks(page_id)

    for block in blocks:
        # print(block['paragraph']['rich_text'][0]['text']['content'])
        weekly_summary.add(block['paragraph']['rich_text'][0]['text']['content'])

print(*weekly_summary, sep='\n')
