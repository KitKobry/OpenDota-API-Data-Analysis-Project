import requests

url = "https://api.opendota.com/api"
print(url)
def getPlayerInfo(steamId):
    apiUrl = f"{url}/players/{steamId}"
    response = requests.get(apiUrl)
    print(response)

    if response.status_code == 200:
        playerData = response.json()
        return (playerData)
    else:
        print(f"error {response.status_code}")

valve = 76561197960265728
steamId = int(input("enter your steam id"))
playerId = steamId - valve

playerInfo = getPlayerInfo(playerId)
print (playerInfo)
if playerInfo:
    print(f"players mmr is : {playerInfo["computed_mmr"]}")
    print(f"players mmr in turbo is : {playerInfo["computed_mmr_turbo"]}")
    print(f"players rank tier is' : {playerInfo["rank_tier"]}")