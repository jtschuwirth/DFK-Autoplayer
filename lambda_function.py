
from functions.checkHeroes import checkHeroes

def handler(event, context):
    return checkHeroes(event["user"])
