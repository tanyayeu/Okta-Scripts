
import asyncio
import csv
import os
from okta.client import Client as OktaClient
from dotenv import load_dotenv

# https://github.com/okta/okta-sdk-python

load_dotenv()
TOKEN = os.getenv('OKTA_TOKEN')
ORG_URL = os.getenv('ORG_URL')

config = {
    'orgUrl': ORG_URL,
    'token': TOKEN
}

client = OktaClient(config)


all_users = [] ## array of users
all_users_groups = [] ## all users w/ their groups

#pass in the function here
def func_loop(func):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(func)

# List all active users
async def list_users():
    query_params = {'filter': 'status eq "ACTIVE"'}
    users, resp, err  = await client.list_users(query_params)
    #f = open("okta_users.txt", "w") # writes all users to txt file
    while True:
        for user in users:
            all_users.append(user.profile.login)
        if resp.has_next():
            users, err = await resp.next()
        else:
            break

# Get groups for one user
async def get_groups(user):
    groups, resp, err = await client.list_user_groups(user)
    user_groups = []
    user_groups.append(user)
    for group in groups:
        if group.type == "OKTA_GROUP":
            user_groups.append(group.profile.name)
    all_users_groups.append(user_groups)
    print(user_groups)

# Loop through user list and get their groups, spit it out to csv
def get_user_groups():
    func_loop(list_users())
    for user in all_users:
        func_loop(get_groups(user))
    with open('okta_users_groups.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(all_users_groups)

get_user_groups()
