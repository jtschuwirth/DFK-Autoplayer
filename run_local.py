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


response = handler({"users": [user]}, "")

for item in response[user]:
    print(item,": ", response[user][item])
