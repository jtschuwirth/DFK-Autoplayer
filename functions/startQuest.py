from functions.QuestCoreV2 import quest_core_contract
from functions.provider import w3, account

address = {
    "mining": "0x75912145f5cFEfb980616FA47B2f103210FaAb94",
    "fishing": "0x407ab39B3675f29A719476af6eb3B9E5d93969E6"
}

def startQuest(heroes, profession):
    attempts = 5
    if profession == "mining":
        attempts = 25
    tx = quest_core_contract.functions.startQuest(heroes, address[profession], attempts, 0).build_transaction({
            "from": account.address,
            'nonce': w3.eth.get_transaction_count(account.address)
            })
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)