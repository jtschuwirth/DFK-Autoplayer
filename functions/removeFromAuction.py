from functions.Contracts import hero_sale_contract
from functions.provider import w3, account

def removeFromAuction(heroId, nonce):
    tx = hero_sale_contract.functions.cancelAuction(heroId).build_transaction({
        "from": account.address,
        'nonce': nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)