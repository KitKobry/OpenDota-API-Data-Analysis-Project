import requests
import pandas as pd

base_url = "https://api.opendota.com/api"

def GetMatchInfo(match_id):
    api_url = f"{base_url}/matches/{match_id}"
    response = requests.get(api_url)
    match_data = response.json()
    return match_data

def GetPlayerInfo(account_id):
    api_url = f"{base_url}/players/{account_id}"
    response = requests.get(api_url)
    player_data = response.json()
    return player_data

def GetHeroInfo():
    api_url = f"{base_url}/heroes/"
    response = requests.get(api_url)
    hero_info = response.json()
    return hero_info

def GetItemsInfo():
    api_url = f"{base_url}/constants/items"
    response = requests.get(api_url)
    items_info = response.json()
    return items_info

def GetRegionInfo():
    api_url = f"{base_url}/constants/region"
    response = requests.get(api_url)
    region_info = response.json()
    return region_info

def GetGamemodeInfo():
    api_url = f"{base_url}/constants/game_mode"
    response = requests.get(api_url)
    gamemode_info = response.json()
    return gamemode_info

def ParsePlayers(match_info):
    players_list = match_info["players"]
    return players_list

def GetHeroMap(hero_info):
    hero_map = {hero["id"]: hero["localized_name"] for hero in hero_info}
    return hero_map

def GetItemsMap(items_info):
    items_map = {int(item["id"]): item.get("dname") for item in items_info.values()}
    return items_map

def GetItemsList(player, items_map):
    items = []
    for i in range(6):
        item_id = player[f"item_{i}"]
        item_name = items_map.get(item_id, "Empty") if item_id != 0 else "Empty"
        items.append(item_name)
    return items

def GetBackpackItemsList(player, items_map):
    backpack_items = []
    for i in range(3):
        backpack_item_id = player[f"backpack_{i}"]
        backpack_item_name = items_map.get(backpack_item_id, "Empty") if backpack_item_id != 0 else "Empty"
        backpack_items.append(backpack_item_name)
    return backpack_items

def GetHeroName(player, hero_map):
    hero_name = hero_map.get(player["hero_id"])
    return hero_name

def GetRegionName(region_info, match_info):
    region_name = region_info.get(str(match_info['region']), "Unknown Region")
    return region_name

def GetPlayerName(player):
    name = player.get("personaname") or "No Name"
    return name

def BuildPlayerDF(player, hero_name, name, items, backpack_items):
    return {
        "Name": name,
        "Hero name": hero_name,
        "K/D/A": f"{player['kills']}/{player['deaths']}/{player['assists']}",
        "Last Hits": player["last_hits"],
        "Denies": player["denies"],
        "GPM": player["gold_per_min"],
        "XP per minute": player["xp_per_min"],
        "LVL": player["level"],
        "Networth": player["net_worth"],
        "Hero Damage": player['hero_damage'],
        "Tower Damage": player['tower_damage'],
        "Healing": player['hero_healing'],
        "Item 1": items[0],
        "Item 2": items[1],
        "Item 3": items[2],
        "Item 4": items[3],
        "Item 5": items[4],
        "Item 6": items[5],
        "Backpack 1": backpack_items[0],
        "Backpack 2": backpack_items[1],
        "Backpack 3": backpack_items[2]
    }

def BuildDataFrame(players_list, hero_map, items_map):
    dict_list = []
    for player in players_list:
        items = GetItemsList(player, items_map)
        backpack_items = GetBackpackItemsList(player, items_map)
        hero_name = GetHeroName(player,hero_map)
        name = GetPlayerName(player)
        temp_dict = BuildPlayerDF(player, hero_name, name, items, backpack_items)
        dict_list.append(temp_dict)
    df = pd.DataFrame.from_dict(dict_list)
    return df

def DisplayMatchInfo(match_info, df, region_info):
    region_name = GetRegionName(region_info,match_info)
    print(f"Region: {region_name}")
    print(f"Gamemode: {match_info['game_mode']}") 
    print(df.to_string())

match_id = input("Enter your match id: ")
match_info = GetMatchInfo(match_id)
player_list = ParsePlayers(match_info)
hero_info = GetHeroInfo()
items_info = GetItemsInfo()
region_info = GetRegionInfo()
hero_map = GetHeroMap(hero_info)
items_map = GetItemsMap(items_info)
match_df = BuildDataFrame(player_list, hero_map, items_map)
DisplayMatchInfo(match_info, match_df, region_info)
print(match_info)
##print(player_list)
##print(items_info)