#code author: Samantha Sieklicki
#uses token from apiAccess.py
import json
import requests
import csv
import time
import collections

#Oauth credentials
client_id='upb6bmpmr830tlrber6kt6scv4'
client_secret='f6hul7degqdc03g57pt21ettkp'
refresh_token='b9c85116a79b407825facc0a8177b4b6'

#refresh token (needs to be done hourly)
def refresh():
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
    return final_token

#token 20:54
final_token='Bearer 482af9f7a45d2b5adf395ecf11a61115'

def only(attLs):
    only=''
    for att in attLs:
        only=only+str(att)+','
    only=only[:-1]
    return only

#Code from https://stackoverflow.com/questions/6027558/flatten-nested-dictionaries-compressing-keys
def flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)    
    
def fillCols(lsDic,attLs):
    lsDic2=[]
    for dic in lsDic:
        lsDic2.append(flatten(dic))
    for dic in lsDic2:
        for att in attLs:
            if att not in dic:
                dic[att]=''
    return lsDic2

#A method's output inherits the attributes on which the item search was based
#In name is used to differentiate between keys in different dictionaries that share the same name
#For example the "name" key in the topics dictionary would become topicname while the "name" key in the events dictionary would remain unchanged
def inKey(lsDic,inDic,inName='SetMe'):
    for dic in lsDic:
        for key in inDic:
            if key not in dic:
                dic[key]=inDic[key]
            else:
                nKey=inName+key
                dic[nKey]=inDic[key]
    return lsDic

#category_ids and name are the required topic attributes to search for groups    
topicAtt=['category_ids','name']
def getTopics(topicAtt=topicAtt):
    meth="https://api.meetup.com/find/topic_categories"
    header={
        'Authorization': final_token
        }
    param = {
        "only":only(topicAtt)
        }
    response=requests.get(meth, headers=header, params=param)
    topics=fillCols(response.json(),topicAtt)
    return topics

#was used to get topic Cats list copied below
#topics=getTopics()
#topicCats=[]
#for topic in topics:
#    for cat in topic['category_ids']:
#        topicCats.append(cat)
#print(topicCats)

topicCats=[3, 23, 34, 25, 14, 33, 9, 32, 6, 27, 10, 36, 16, 21, 4, 13, 12, 20, 11, 29, 22, 24, 28, 1, 18, 5, 26, 15, 8, 31, 2]

#urlname is the required group attribute to search for events 
groupAtt=['urlname','name','member_pay_fee','members','organizer.name','pro_network.number_of_groups','created','meta_category.name']
#30 requests allowed per 10 seconds
def getGroups(cat, lat=45.45, lon=-75.69):
    meth="https://api.meetup.com/find/groups"
    header={
        'Authorization': final_token
        }
    param = {
        "lat": lat,
        "lon": lon,
        "radius": 50,
        "page": 200,
        "only": only(groupAtt),
        "category": cat
        }
    response=requests.get(meth, headers=header, params=param)
    groups=fillCols(response.json(),groupAtt)
    return groups





eventAtt=['duration','rsvp_limit','local_date','local_time','waitlist_count','yes_rsvp_count','venue.name','venue.address_1','is_online_event','fee.required','fee.amount']
#30 requests allowed per 10 seconds
def getEvents(grp,eventAtt=eventAtt,after='2020-09-01T00:00:00.000', before='2021-01-01T00:00:00.000'):
    meth="https://api.meetup.com/"+grp+"/events"
    header={
        'Authorization': final_token
        }
    param={
        "no_later_than": before,
        "no_earlier_than": after,
        "status": 'past,upcoming',
        "page": 625,
        "only": only(eventAtt)
        }
    response=requests.get(meth, headers=header, params=param)
    events=fillCols(response.json(),eventAtt)
    return events

#First allKey and inKey then lastly lsDicFlip
#inDic is the dictionary from which all dic in lsDic inherit all keys
#lsDic is the list of dictionaries output by the get methods
#inName is the name to give similar keys, for example name in topic becomes topic name
#format example: lsDic=[{'k1':'a','k2':'1'},{'k1':'b','k2':'2'}]
#format example: inDic={'k1':'z'}
#format example: inName="inDic"



#csv for Tableau
def lsDicToCsv(lsDic,name='Data'):
    cols=[]
    for key in lsDic[0]:
        cols.append(key)
    fName=name+'.csv'
    f=open(fName, 'w')
    writer = csv.DictWriter(f, fieldnames=cols)
    writer.writeheader()
    for dic in lsDic:
        writer.writerow(dic)
    f.close()
    
#json for Altair
def lsDicToDicLs(lsDic):
    dicLs={}
    for key in lsDic[0]:
        dicLs[key]=[]
    for dic in lsDic:
        for key in dic:
            dicLs[key].append(dic[key])
    return dicLs

#A method's output inherits the attributes on which the item search was based
#In name is used to differentiate between keys in different dictionaries that share the same name
#For example the "name" key in the topics dictionary would become topicname while the "name" key in the events dictionary would remain unchanged
#def inKey(lsDic,inDic,inName='SetMe'):

count=1
groups=[]
events=[]

for cat in topicCats:
    if count%25==0:
        time.sleep(11)
    groups+=getGroups(cat)
    count+=1

for group in groups:
    if count%25==0:
        time.sleep(11)
    events+=inKey(getEvents(group['urlname']),group,inName='group')
    count+=1

#altairData=lsDicToDicLs(events)
lsDicToCsv(events,'meetupF2020')

