import boto3
import os
from functions.checkHeroes import checkHeroes

users= {}

my_session = boto3.session.Session(
        aws_access_key_id=os.environ.get("ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("SECRET_KEY"),
        region_name = "us-east-1",
    )
table = my_session.resource('dynamodb').Table("dfk-autoplayer")

def handler(event, context):
    for user in event["users"]:
        users[user] = checkHeroes(user, event["override"],table)
    return users
