from functions.QuestCoreV2 import quest_core_contract
from functions.provider import w3, account
from datetime import datetime

def claimReward(heroes, profession, table):
    tx = quest_core_contract.functions.completeQuest(heroes[0]).build_transaction({
        "from": account.address,
        'nonce': w3.eth.get_transaction_count(account.address)
    })

    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(tx_hash)
    now = int(datetime.now().timestamp())
    table.put_item(Item={
        "address_": account.address, 
        "date_": now, 
        "tx_hash_": tx_hash,
        "profession_": profession
    })
