from functions.Contracts import getMeditation

ZERO_ADDRESS = '0x0000000000000000000000000000000000000000'

def levelUpHero(hero, hero_data, account, nonce, w3, network):
    meditation_contract = getMeditation(w3, network)
    tx = meditation_contract.functions.startMeditation(
                                hero, 
                                hero_data["primaryStat"], 
                                hero_data["secondaryStat"], 
                                hero_data["tertiaryStat"],
                                ZERO_ADDRESS
                                ).build_transaction({
                                    "from": account.address,
                                    'nonce': nonce
                                })
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)

def completeMeditation(hero, account, nonce, w3, network):
    meditation_contract = getMeditation(w3, network)
    tx = meditation_contract.functions.completeMeditation(hero).build_transaction({
        "from": account.address,
        'nonce': nonce
    })
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)
