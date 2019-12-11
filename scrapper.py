#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import pandas
from pathlib import Path

api_key = 'api_key'
# limit: 10 request per minute
api_key = Path(api_key).read_text().strip()
api_key


# In[48]:


url = 'https://api.pubg.com/shards/'
platform_list = ['steam/','console/','kakao/']

headers = {'Authorization': 'Bearer ' + api_key,
           'Accept': 'application/vnd.api+json'}


# In[49]:


# get match samples
match_list = []
for platform in platform_list:
    sample_url = url + platform + 'samples'
    sample_response = requests.get(sample_url, headers=headers)
    sample_data = json.loads(sample_response.text)
    for match in sample_data['data']['relationships']['matches']['data']:
        match_list.append(match['id'])


len(match_list) # 2007 matches from three platforms


all_rows = []


for i,match in enumerate(match_list):
    match_url = url + platform + 'matches/' + match
    match_response = requests.get(match_url, headers = headers)
    # get match
    sample_match = json.loads(match_response.text)
    # get match attributes
    matchType = sample_match['data']['attributes']['gameMode']
    matchDuration = sample_match['data']['attributes']['duration']
    matchId = match
    # get player attributes
    included = sample_match['included']
    for obj in included:
        if obj['type'] == 'participant':
            player = obj['attributes']['stats']
            playerId = player['playerId']
            playerName = player['name']
            DBNOs = player['DBNOs']
            assists = player['assists']
            boosts = player['boosts']
            damageDealt = player['damageDealt']
            deathType = player['deathType']
            headshotKills = player['headshotKills']
            heals = player['heals']
            killPlace = player['killPlace']
            killStreaks = player['killStreaks']
            kills = player['kills']
            longestKill = player['longestKill']
            revives = player['revives']
            rideDistance = player['rideDistance']
            roadKills = player['roadKills']
            swimDistance = player['swimDistance']
            teamKills = player['teamKills']
            timeSurvived = player['timeSurvived']
            vehicleDestroys = player['vehicleDestroys']
            walkDistance = player['walkDistance']
            weaponsAcquired = player['weaponsAcquired']
            winPlace = player['winPlace']
            row = (playerId, matchId, assists, boosts,damageDealt,DBNOs,headshotKills,heals,killPlace,
                   kills,killStreaks,longestKill,matchDuration,matchType,revives,
                   rideDistance,roadKills,swimDistance,teamKills,vehicleDestroys,walkDistance,weaponsAcquired,winPlace)
            all_rows.append(row)


# In[68]:


len(all_rows) # 173087 rows


# In[77]:


columns = ["playerId", "matchId", "assists", "boosts","damageDealt","DBNOs","headshotKills","heals","killPlace","kills","killStreaks","longestKill","matchDuration","matchType","revives","rideDistance","roadKills","swimDistance","teamKills","vehicleDestroys","walkDistance","weaponsAcquired","winPlace"]


# In[78]:


import csv
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    for row in all_rows:
        writer.writerow(row)






