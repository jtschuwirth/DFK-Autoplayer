import requests
from datetime import datetime
import time

from functions.startQuest import startQuest
from functions.claimReward import claimReward
from functions.removeFromAuction import removeFromAuction

from functions.Contracts import quest_core_contract
from functions.provider import w3, get_account

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
graph_url = "https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}


def checkHeroes(user, override, table):
    account = get_account(user)
    nonce = w3.eth.get_transaction_count(account.address)
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

    response = requests.post(
        graph_url, json={"query": query, "variables": variables}, headers=headers)
    ready_to_quest = {
        "mining": [],
        "fishing": [],
        "foraging": [],
        "vitality": []
    }
    questing = {
        "mining": [],
        "fishing": [],
        "foraging": [],
        "vitality": []
    }
    done_questing = {
        "mining": [],
        "fishing": [],
        "foraging": [],
        "vitality": []
    }
    recharging = {
        "mining": [],
        "fishing": [],
        "foraging": [],
        "vitality": []
    }
    auction = []

    for hero in response.json()["data"]["heroes"]:
        if hero["saleAuction"]:
            auction.append(hero)
            continue

        # Ready to Quest
        if hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) <= int(time.mktime(datetime.now().timetuple())):
            overrided = False
            for training_quest in override:
                if hero["id"] in override[training_quest]:
                    ready_to_quest[training_quest].append(hero)
                    overrided = True
                    break
            if not overrided: ready_to_quest[hero["profession"]].append(int(hero["id"]))

        # Currently Questing
        elif hero["currentQuest"] != ZERO_ADDRESS:
            hero_quest = quest_core_contract.functions.getHeroQuest(
                int(hero["id"])).call()
            end_time = hero_quest[7]
            if int(end_time) <= int(time.mktime(datetime.now().timetuple())):
                done_questing[hero["profession"]].append(int(hero["id"]))
            else:
                questing[hero["profession"]].append(int(hero["id"]))

        # Recharging Stamina
        elif hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) >= int(time.mktime(datetime.now().timetuple())):
            recharging[hero["profession"]].append(int(hero["id"]))

    for hero in auction:
        if hero["staminaFullAt"] <= int(time.mktime(datetime.now().timetuple()))+30*60:
            try:
                removeFromAuction(hero["id"], account, nonce)
                print(f"Hero: {hero['id']} removed from auction")
                nonce += 1
            except Exception as e:
                print(
                    f"error canceling auction with hero: {hero['id']}, error: {e}")

    for profession in done_questing:
        if done_questing[profession]:
            try:
                claimReward(done_questing[profession],
                            profession, account, nonce, table)
                print(f"Heroes: {done_questing[profession]} claimed reward")
                nonce += 1
            except Exception as e:
                print(
                    f"error claiming quest with heroes: {done_questing[profession]}, error: {e}")

    for profession in ready_to_quest:
        if ready_to_quest[profession] and not questing[profession]:
            try:
                startQuest(ready_to_quest[profession][0:6], profession, account, nonce)
                print(
                    f"Heroes: {ready_to_quest[profession][0:6]} started quest")
                nonce += 1
            except Exception as e:
                print(
                    f"error starting quest with heroes: {ready_to_quest[profession][0:6]}, error: {e}")

    return {
        "ready to quest": ready_to_quest,
        "questing": questing,
        "done_questing": done_questing,
        "recharging": recharging,
        "auction": auction
    }
