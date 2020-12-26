# install python 3.7  & pip, then run below code in console
# python3.7 pip install requests

import requests
import json

#Oauth credentials
client_id=*****
redirect_uri=*****
client_secret=*****
email=*****
password=*****

#API access step 1
site1 = 'https://secure.meetup.com/oauth2/authorize'
header1 = {
   "Accept": "Application/json"
 }
creds1 = {
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'response_type': 'anonymous_code'
}
auth1 = requests.get(site1, headers=header1, params=creds1)
print(auth1.status_code)
print(auth1)
authcode=auth1.json()['code']

#API access step 2
site2='https://secure.meetup.com/oauth2/access'
header2=header1
creds2 = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'anonymous_code',
        'redirect_uri': redirect_uri,
        'code': authcode
}
auth2 = requests.(site2, headers=header2, params=creds2)
print(auth2.status_code)
print(auth2)
bearer_token='Bearer '+str(auth2.json()['access_token'])

#API access step 3
site3='https://api.meetup.com/sessions'
header3={
    'Authorization': final_token
}
creds3={
    'email':email,
    'password':password
    }
auth3 = requests.post(site3, headers=header3, params=creds3)
print(auth3.status_code)
print(auth3)
oauth_token=auth3.json()['oauth_token'])
final_token='Bearer '+str(oauth_token)
refresh_token=auth3.json()['refresh_token']

#calls meetup api find groups fn
meth='https://api.meetup.com/find/groups'
header5={
    'Authorization': final_token
    }
params1 = {
        "zip": 11211,
        "radius": 1,
        "category": 25,
        "order": 'members'
    }
response=requests.get(meth, headers=header5, params=params1)
print(response.status_code)
print(response)

#a function to format json output
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

# prints the data
jprint(response.json())

#refresh token (needs to be done hourly)
site4='https://secure.meetup.com/oauth2/access'
header4={
    'Accept': 'application/x-www-form-urlencoded'
    }
creds4={
    'client_id': client_id,
    'client_secret':client_secret,
    'grant_type': 'refresh_token',
    'refresh_token':refresh_token
    }
auth_re=requests.post(site4, headers=header4, params=creds4)
oauth_token=auth_re.json()['access_token']
final_token='Bearer '+str(oauth_token)



#'0affac32173f86046eb2239724b50400'

#{'access_token': '1db187b7665df0d15968b30021d6926a', 'refresh_token': 'b9c85116a79b407825facc0a8177b4b6', 'token_type': 'bearer', 'expires_in': 3600}
