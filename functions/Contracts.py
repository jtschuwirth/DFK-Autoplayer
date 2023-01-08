import json

QuestCoreJson = open("abi/QuestCoreV2.json")
QuestCoreABI = json.load(QuestCoreJson)

HeroSaleJson = open("abi/HeroSale.json")
HeroSaleABI = json.load(HeroSaleJson)

HeroRentJson = open("abi/HeroRent.json")
HeroRentABI = json.load(HeroRentJson)

MeditationCircleJson = open("abi/MeditationCircle.json")
MeditationCircleABI = json.load(MeditationCircleJson)

SummonJson = open("abi/Summon.json")
SummonABI = json.load(SummonJson)

quest_core_address = {
    "dfk": "0xE9AbfBC143d7cef74b5b793ec5907fa62ca53154",
    "kla": "0x8dc58d6327E1f65b18B82EDFb01A361f3AAEf624"
}

hero_sale_address = {
    "dfk": "0xc390fAA4C7f66E4D62E59C231D5beD32Ff77BEf0",
    "kla": "0x7F2B66DB2D02f642a9eb8d13Bc998d441DDe17A8"
}

hero_rent_address = {
    "dfk": "0x8101CfFBec8E045c3FAdC3877a1D30f97d301209",
    "kla": "0xA2cef1763e59198025259d76Ce8F9E60d27B17B5"
}

meditation_address = {
    "dfk": "0xD507b6b299d9FC835a0Df92f718920D13fA49B47",
    "kla": "0xdbEE8C336B06f2d30a6d2bB3817a3Ae0E34f4900"
}

summon_address = {
    "dfk": "0xBc36D18662Bb97F9e74B1EAA1B752aA7A44595A7",
    "kla": "0xb086584f476Ad21B40aF0672f385a67334A0b294"
}


def getQuestCore(w3, network):
    return w3.eth.contract(
        address=quest_core_address[network], abi=QuestCoreABI)


def getHeroSale(w3, network):
    return w3.eth.contract(
        address=hero_sale_address[network], abi=HeroSaleABI)


def getMeditation(w3, network):
    return w3.eth.contract(
        address=meditation_address[network], abi=MeditationCircleABI)

def getHeroRent(w3, network):
    return w3.eth.contract(
        address=hero_rent_address[network], abi=HeroRentABI
    )

def getSummon(w3, network):
    return w3.eth.contract(
        address=summon_address[network], abi=SummonABI
    )
