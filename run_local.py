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


response = handler({"users":["0x7C50D01C7Ba0EDE836bDA6daC88A952f325756e3", "0xa691623968855b91A066661b0552a7D3764c9a64"]}, "")

for user_result in response:
    for chain_result in response[user_result]:
        print(" ")
        print(f"--------{user_result}---------------")
        print(" ")
        for result in chain_result:
            print(result,": ", chain_result[result])
