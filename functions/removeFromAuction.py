from functions.Contracts import getHeroSale


def removeFromAuction(heroId, account, nonce, w3):
    hero_sale_contract = getHeroSale(w3)
    tx = hero_sale_contract.functions.cancelAuction(int(heroId)).build_transaction({
        "from": account.address,
        'nonce': nonce
    })

    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
