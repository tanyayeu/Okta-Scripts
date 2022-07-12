# Remove Deactivated Users from Okta Groups
This will grab all groups from Okta and go through each list of users and remove any deactivated users.\
Replace `orgUrl` and `token` with the approprite URL and your own Okta API token. 
```
pip install okta
python3 cleangroups.py
```
Terminal will output the users that are being removed from groups.\
Please see https://github.com/okta/okta-sdk-python for more information about the APIs used. 
