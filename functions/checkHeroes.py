import requests
from datetime import datetime
import time

from functions.startQuest import startQuest
from functions.claimReward import claimReward

from functions.Contracts import getQuestCore
from functions.provider import get_account, get_provider

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'
graph_url = "https://defi-kingdoms-community-api-gateway-co06z8vi.uc.gateway.dev/graphql"

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0'
}

address_from_quest = {
    "dfk": {
        "mining": "0x75912145f5cFEfb980616FA47B2f103210FaAb94",
        "fishing": "0x407ab39B3675f29A719476af6eb3B9E5d93969E6",
        "foraging": "0xAd51199B453075C73FA106aFcAAD59f705EF7872",
        "gardening": "0xC4839Fb9A5466878168EaE3fD58c647B71475b61"
    },
    "kla": {
        "mining": "0x46F036B26870188aD69877621815238D2b81bef1",
        "fishing": "0x0E7a8b035eF2FA0183a2680458818256424Bd60B",
        "foraging": "0x54DaD24dDc2cC6E7616438816DE0EeFCad79B625",
        "gardening": "0x3837612f3A14C92Da8E0186AB398A753fe169dc1"
    }
}

meditation_quests = [
    "0xD507b6b299d9FC835a0Df92f718920D13fA49B47",
    "0xdbEE8C336B06f2d30a6d2bB3817a3Ae0E34f4900"
]


def checkHeroes(user, network):
    w3 = get_provider(network)
    account = get_account(user, w3)
    nonce = w3.eth.get_transaction_count(account.address)
    query = """
        query ($user: String, $network: String) {
            heroes(where: {owner: $user, network: $network}) {
                id
                xp
                level
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
        "user": user,
        "network": network
    }

    response = requests.post(
        graph_url, json={"query": query, "variables": variables}, headers=headers)

    ready_to_quest = {
    }
    questing = {
    }
    done_questing = {
    }

    recharging = {
        "mining": [],
        "fishing": [],
        "foraging": [],
        "vitality": []
    }

    if not "data" in response.json() or len(response.json()["data"]["heroes"]) == 0: 
        print("No Heroes on chain: ", network)
        return
    for hero in response.json()["data"]["heroes"]:
        # Ready to Quest Miner or Gardener
        if (hero["profession"]=="mining" or hero["profession"] == "gardening") and hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) <= int(time.mktime(datetime.now().timetuple()))+60*200:
            if address_from_quest[network][hero["profession"]] in ready_to_quest:
                ready_to_quest[address_from_quest[network][hero["profession"]]].append(
                    int(hero["id"]))
            else:
                ready_to_quest[address_from_quest[network][hero["profession"]]] = [
                    int(hero["id"])]

        # Ready to Quest Fisher or Forager
        elif hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) <= int(time.mktime(datetime.now().timetuple())):
            if address_from_quest[network][hero["profession"]] in ready_to_quest:
                ready_to_quest[address_from_quest[network][hero["profession"]]].append(
                    int(hero["id"]))
            else:
                ready_to_quest[address_from_quest[network][hero["profession"]]] = [
                    int(hero["id"])]

        # Currently Questing
        elif hero["currentQuest"] != ZERO_ADDRESS:
            quest_core_contract = getQuestCore(w3, network)
            hero_quest = quest_core_contract.functions.getHeroQuest(
                int(hero["id"])).call()
            end_time = hero_quest[7]
            if int(end_time) <= int(time.mktime(datetime.now().timetuple())):
                if hero_quest[1] in done_questing:
                    done_questing[hero_quest[1]].append(int(hero["id"]))
                else:
                    done_questing[hero_quest[1]] = [int(hero["id"])]
            else:
                if hero_quest[1] in questing:
                    questing[hero_quest[1]].append(int(hero["id"]))
                else:
                    questing[hero_quest[1]] = [int(hero["id"])]

        # Recharging Stamina
        elif hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) >= int(time.mktime(datetime.now().timetuple())):
            recharging[hero["profession"]].append(int(hero["id"]))

    for profession in done_questing:
        if done_questing[profession]:
            try:
                claimReward(done_questing[profession], account, nonce, w3, network)
                print(f"Heroes: {done_questing[profession]} claimed reward")
                nonce += 1
            except Exception as e:
                print(
                    f"error claiming quest with heroes: {done_questing[profession]}, error: {e}")

    for profession in ready_to_quest:
        if ready_to_quest[profession] and not profession in questing:
            try:
                if profession == address_from_quest[network]["gardening"]:
                    startQuest(ready_to_quest[profession]
                        [0: 2], profession, account, nonce, w3, network)
                    print(
                        f"Heroes: {ready_to_quest[profession][0:2]} started quest")
                else:
                    startQuest(ready_to_quest[profession]
                        [0: 6], profession, account, nonce, w3, network)
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
        "recharging": recharging
    }
