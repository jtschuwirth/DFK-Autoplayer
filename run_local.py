from lambda_function import handler

user = "0x7C50D01C7Ba0EDE836bDA6daC88A952f325756e3"

    # 0: "Strength"
    # 1: "Agility"
    # 2: "Intelligence"
    # 3: "Wisdom"
    # 4: "Luck"
    # 5: "Vitality"
    # 6: "Endurance"
    # 7: "Dexterity"


response = handler({
    "users": [user],
    "override": {
        "vitality": []
    },
    "level_up": {
        "1000000061678": {
            "_primaryStat": 6,
            "_secondaryStat": 5,
            "_tertiaryStat": 0
        },
        "1000000014600": {
            "_primaryStat": 0,
            "_secondaryStat": 5,
            "_tertiaryStat": 6
        }

    }
}, "")

for item in response[user]:
    print(item,": ", response[user][item])
