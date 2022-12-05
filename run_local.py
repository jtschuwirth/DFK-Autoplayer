from lambda_function import handler

response = handler({"user": "0x7C50D01C7Ba0EDE836bDA6daC88A952f325756e3"}, "")

for i in response:
    print(f"{i}: mining: {len(response[i]['mining'])}, fishing: {len(response[i]['fishing'])}")