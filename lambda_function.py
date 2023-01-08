from functions.checkHeroes import checkHeroes

users= {}

chains = [
    "dfk", 
    #"kla"
]

def handler(event, context):
    response = {}
    for user in event["users"]:
        response[user] = []
        for chain in chains:
            response[user].append(checkHeroes(user, chain))
    return response
