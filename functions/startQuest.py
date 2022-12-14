from functions.Contracts import quest_core_contract
from functions.provider import w3

def startQuest(heroes, profession, account, nonce):
    attempts = 5
    if profession == "mining": attempts = 25
    tx = quest_core_contract.functions.startQuest(heroes, profession, attempts, 0).build_transaction({
            "from": account.address,
            'nonce': nonce
            })
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)