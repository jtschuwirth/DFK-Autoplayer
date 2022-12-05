from functions.QuestCoreV2 import quest_core_contract

def claimReward(heroes):
    quest_core_contract.functions.multiCompleteQuest(heroes).call()