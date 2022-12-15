import requests
from datetime import datetime
import time

from functions.startQuest import startQuest
from functions.claimReward import claimReward
from functions.removeFromAuction import removeFromAuction
from functions.Meditation import levelUpHero, completeMeditation

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
        "vitality": "0xE3edf52D33F2BB05DBdA5BA73903E27a9B9b7e9d"
    },
    "kla": {
        "mining": "0x46F036B26870188aD69877621815238D2b81bef1",
        "fishing": "0x0E7a8b035eF2FA0183a2680458818256424Bd60B",
        "foraging": "0x54DaD24dDc2cC6E7616438816DE0EeFCad79B625",
        "vitality": "0x89a60d8B332ce2Dd3bE8b170c6391F98a03a665F"
    }
}


def checkHeroes(user, network, table):
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

    if not "data" in response.json(): 
        print("no Heroes on chain: ", network)
        return
    for hero in response.json()["data"]["heroes"]:
        hero_setting = table.get_item(
            Key={"heroId_": int(hero["id"]), "owner_": user})
        override = False
        level_up = False
        stats = {}
        if "Item" in hero_setting:
            if "override_" in hero_setting["Item"]:
                override = hero_setting["Item"]["override_"]
            if "levelUp_" in hero_setting["Item"]:
                level_up = hero_setting["Item"]["levelUp_"]
            if level_up:
                stats = {
                    "primaryStat": hero_setting["Item"]["primaryStat_"],
                    "secondaryStat": hero_setting["Item"]["secondaryStat_"],
                    "tertiaryStat": hero_setting["Item"]["tertiaryStat_"]
                }
        if hero["saleAuction"] and hero["staminaFullAt"] <= int(time.mktime(datetime.now().timetuple()))+30*60:
            try:
                removeFromAuction(int(hero["id"]), account, nonce, w3, network)
                print(f"Hero: {hero['id']} removed from auction")
                nonce += 1
            except Exception as e:
                print(
                    f"error canceling auction with hero: {hero['id']}, error: {e}")

        # Ready to Quest
        if hero["currentQuest"] == ZERO_ADDRESS and int(hero["staminaFullAt"]) <= int(time.mktime(datetime.now().timetuple()))+60*200:
            if override:
                ready_to_quest[address_from_quest[network][override]].append(hero)
            elif address_from_quest[network][hero["profession"]] in ready_to_quest:
                ready_to_quest[address_from_quest[network][hero["profession"]]].append(
                    int(hero["id"]))
            else:
                ready_to_quest[address_from_quest[network][hero["profession"]]] = [
                    int(hero["id"])]

        # Currently Questing
        elif hero["currentQuest"] != ZERO_ADDRESS:
            if hero["currentQuest"] == "0xD507b6b299d9FC835a0Df92f718920D13fA49B47" or hero["currentQuest"] == "0xdbEE8C336B06f2d30a6d2bB3817a3Ae0E34f4900":
                try:
                    completeMeditation(int(hero["id"]), account, nonce, w3, network)
                    nonce += 1
                except Exception as e:
                    print("Error:", e)
            else:
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
            if level_up and (hero["xp"] % 1000 == 0 and hero["xp"] != 0) and hero["level"]<6:
                try:
                    levelUpHero(int(hero["id"]),
                                stats, account, nonce, w3, network)
                    nonce += 1
                except Exception as e:
                    print("Error:", e)
            else:
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
