import requests
from datetime import datetime
import time
from functions.startQuest import startQuest
from functions.claimReward import claimReward
from functions.QuestCoreV2 import quest_core_contract

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
graph_url = "https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

def checkHeroes(user, table):

    query = """
        query ($user: String) {
            heroes(where: {owner: $user}) {
                id
                profession
                currentQuest
                staminaFullAt
                saleAuction {
    	            id
    	        }
            }
        }
    """
    variables = {
        "user": user
    }

    response = requests.post(graph_url, json={"query":query, "variables": variables}, headers=headers)
    ready_to_quest = {
            "mining":[],
            "fishing":[]
        }
    questing = {
            "mining":[],
            "fishing":[]
        }
    done_questing = {
        "mining":[],
        "fishing":[]
    }
    recharging= {
            "mining":[],
            "fishing":[]
        }
    auction = []

    for hero in response.json()["data"]["heroes"]:
        if hero["saleAuction"]: 
            auction.append(int(hero["id"]))
            continue
        
        #Ready to Quest
        if hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) <= int(time.mktime(datetime.now().timetuple())):
           ready_to_quest[hero["profession"]].append(int(hero["id"]))
        
        #Currently Questing
        elif hero["currentQuest"] != ZERO_ADDRESS:
            hero_quest = quest_core_contract.functions.getHeroQuest(int(hero["id"])).call()
            end_time = hero_quest[7]
            if int(end_time) <= int(time.mktime(datetime.now().timetuple())):
                done_questing[hero["profession"]].append(int(hero["id"]))
            else:
                questing[hero["profession"]].append(int(hero["id"]))

        #Recharging Stamina
        elif hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) >= int(time.mktime(datetime.now().timetuple())):
            recharging[hero["profession"]].append(int(hero["id"]))
            
    for profession in done_questing:
        if done_questing[profession]:
            try:
                claimReward(done_questing[profession], profession, table)
            except Exception as e:
                print(f"error claiming quest with heroes: {done_questing[profession]}, error: {e}")
    
    for profession in ready_to_quest:
        if ready_to_quest[profession] and not questing[profession]:
            try:
                startQuest(ready_to_quest[profession][0:6], profession)
            except Exception as e:
                print(f"error starting quest with heroes: {ready_to_quest[profession][0:6]}, error: {e}")

    return {
        "ready to quest": ready_to_quest,
        "questing": questing, 
        "done_questing": done_questing,
        "recharging": recharging,
        "auction":auction
        }