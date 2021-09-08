## This script gets all groups from okta and checks the group membership and removes
## any deactivated users from the group

from okta.client import Client as OktaClient
import asyncio
import csv
"""
group management
https://github.com/okta/okta-sdk-python/blob/master/okta/resource_clients/group_client.py
"""

config = {
    'orgUrl': 'https://{COMPANY}.okta.com',
    'token': '{API_TOKEN}'
}
client = OktaClient(config)


## api to list all groups in okta
async def list_groups():
    result, resp, err = await client.list_groups()
    return result

# calls the previous async api
def getAllGroups():
    all_groups = []
    loop = asyncio.get_event_loop()
    data_set = loop.run_until_complete(list_groups())
    for group in data_set:
        all_groups.append([group.id, group.profile.name, group.type])
    return all_groups

## list all group members. provide the group ID
async def getMembers(groupID):
    result, resp, err =  await client.list_group_users(groupID)
    return result

#delete specificied user from group
async def deleteUser(groupID, userID):
    resp, err = await client.remove_user_from_group(groupID, userID)

#looks at the member list and if the user is deactivated, 
#it will delete the user from the group
#calls the api to remove user from group
def removeUsersFromGroup(members, group):
    groupID = group[0]
    groupName = group[1]
    loop = asyncio.get_event_loop()
    for user in members:
        status = user.status
        login = user.profile.login
        userID = user.id
        if "DEPROVISION" in status:
            print("Remove ", login, "from ", groupName)
            loop.run_until_complete(deleteUser(groupID, userID))

# Removes deactivated users from all groups if the group type is OKTA_GROUP
def scrubGroups(all_groups):
    loop = asyncio.get_event_loop()
    for group in all_groups:
        groupID = group[0]
        groupType = group[2]
        members = {}
        if "OKTA_GROUP" in groupType:
            members = loop.run_until_complete(getMembers(groupID))
            removeUsersFromGroup(members, group)

all_groups = []
all_groups = getAllGroups()
scrubGroups(all_groups)

