from functions.Contracts import quest_core_contract
from functions.provider import w3

def claimReward(heroes, account, nonce):
    tx = quest_core_contract.functions.completeQuest(heroes[0]).build_transaction({
        "from": account.address,
        'nonce': nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = w3.toHex(hash)
