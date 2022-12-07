from lambda_function import handler

user = "0x7C50D01C7Ba0EDE836bDA6daC88A952f325756e3"

response = handler({"users": [user]}, "")

for i in response[user]:
    if i == "auction": continue
    print(f"{i}: mining: {len(response[user][i]['mining'])}, fishing: {len(response[user][i]['fishing'])}")
print(f"On auction: {len(response[user]['auction'])}")