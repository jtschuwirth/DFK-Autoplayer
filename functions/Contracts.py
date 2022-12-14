from functions.provider import w3
import json

QuestCoreJson = open("abi/QuestCoreV2.json")
QuestCoreABI = json.load(QuestCoreJson)

HeroSaleJson = open("abi/HeroSale.json")
HeroSaleABI = json.load(HeroSaleJson)

MeditationCircleJson = open("abi/MeditationCircle.json")
MeditationCircleABI = json.load(MeditationCircleJson)

quest_core_contract = w3.eth.contract(
    address="0xE9AbfBC143d7cef74b5b793ec5907fa62ca53154", abi=QuestCoreABI)

hero_sale_contract = w3.eth.contract(
    address="0xc390fAA4C7f66E4D62E59C231D5beD32Ff77BEf0", abi=HeroSaleABI)

meditation_contract = w3.eth.contract(
    address="0xD507b6b299d9FC835a0Df92f718920D13fA49B47", abi=MeditationCircleABI)
