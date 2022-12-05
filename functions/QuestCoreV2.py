from functions.provider import w3
import json

QuestCoreJson = open("abi/QuestCoreV2.json")
QuestCoreABI = json.load(QuestCoreJson)

quest_core_contract = w3.eth.contract(address = "0xE9AbfBC143d7cef74b5b793ec5907fa62ca53154", abi = QuestCoreABI)