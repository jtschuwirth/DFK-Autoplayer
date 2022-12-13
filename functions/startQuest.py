from functions.Contracts import quest_core_contract
from functions.provider import w3

address = {
    "mining": "0x75912145f5cFEfb980616FA47B2f103210FaAb94",
    "fishing": "0x407ab39B3675f29A719476af6eb3B9E5d93969E6",
    "foraging": "0xAd51199B453075C73FA106aFcAAD59f705EF7872",
    "vitality": "0xE3edf52D33F2BB05DBdA5BA73903E27a9B9b7e9d"
}

def startQuest(heroes, profession, account, nonce):
    attempts = 5
    if profession == "mining": attempts = 25
    tx = quest_core_contract.functions.startQuest(heroes, address[profession], attempts, 0).build_transaction({
            "from": account.address,
            'nonce': nonce
            })
    signed_tx = w3.eth.account.sign_transaction(tx, account.key)
    w3.eth.send_raw_transaction(signed_tx.rawTransaction)