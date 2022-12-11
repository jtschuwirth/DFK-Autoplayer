from functions.Contracts import quest_core_contract
from functions.provider import w3, account
from datetime import datetime

def claimReward(heroes, profession, nonce, table):
    tx = quest_core_contract.functions.completeQuest(heroes[0]).build_transaction({
        "from": account.address,
        'nonce': nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)

    now = int(datetime.now().timestamp())
    table.put_item(Item={
        "address_": account.address, 
        "date_": now, 
        "hash_": hash,
        "profession_": profession
    })
