import requests
import pandas as pd

base_url = "https://api.opendota.com/api"

def GetItemsInfo():
    api_url = f"{base_url}/constants/items"
    response = requests.get(api_url)
    items_info = response.json()
    return items_info

def GetItemsMap(items_info):
    items_map = {int(item["id"]): item['dname'] for item in items_info.values()}
    return items_map

items_info = GetItemsInfo()
items_map = GetItemsMap(items_info)
print(items_info)