from functions.QuestCoreV2 import quest_core_contract

address = {
    "mining": "0x75912145f5cFEfb980616FA47B2f103210FaAb94",
    "fishing": "0x407ab39B3675f29A719476af6eb3B9E5d93969E6"
}

def startQuest(heroes, profession):
    quest_core_contract.functions.multiStartQuest(address[profession], heroes, 5, 0).call()