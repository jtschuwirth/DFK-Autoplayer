import boto3
import os
from functions.checkHeroes import checkHeroes

users= {}

my_session = boto3.session.Session(
        aws_access_key_id=os.environ.get("ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("SECRET_KEY"),
        region_name = "us-east-1",
    )
table = my_session.resource('dynamodb').Table("dfk-autoplayer-heroes")

chains = [
    "dfk", 
    #"kla"
]

def handler(event, context):
    response = {}
    for user in event["users"]:
        response[user] = []
        for chain in chains:
            response[user].append(checkHeroes(user, chain, table))
    return response
