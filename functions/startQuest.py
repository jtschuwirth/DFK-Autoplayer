from functions.Contracts import getQuestCore


def startQuest(heroes, profession, account, nonce, w3, network):
    attempts = 3
    quest_core_contract = getQuestCore(w3, network)
    if profession == "0x75912145f5cFEfb980616FA47B2f103210FaAb94" or profession == "0x46F036B26870188aD69877621815238D2b81bef1": 
        attempts = 15
    tx = quest_core_contract.functions.startQuest(heroes, profession, attempts, 0).build_transaction({
        "from": account.address,
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)
