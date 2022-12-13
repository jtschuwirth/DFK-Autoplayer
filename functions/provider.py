from web3 import Web3
import os
from dotenv import load_dotenv
load_dotenv()
from web3.middleware import geth_poa_middleware


rpc_url = "https://avax-dfk.gateway.pokt.network/v1/lb/6244818c00b9f0003ad1b619/ext/bc/q2aTwKuyzgs8pynF7UXBZCU7DejbZbZ6EUyHr3JQzYgwNPUPi/rpc"
w3 = Web3(Web3.HTTPProvider(rpc_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.clientVersion

def get_account(address):
    return w3.eth.account.from_key(os.environ.get(address))
