import requests
import pprint
from pandas import json_normalize
import time
import pandas as pd
import numpy as np
import datetime
from bs4 import BeautifulSoup
import urllib

# Setting up dataframe to show all columns
pd.set_option('display.max_columns', None)


api_key = ''
username = ""
account_info = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+ username + "?api_key="+api_key


account_info_response = requests.get(account_info)
print(account_info_response)

json_res = account_info_response.json()

# Get accountId and puuid
accountId = json_res['accountId']
puuid = json_res['puuid']

# Match history based on puuid
match_history = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/" + puuid + "/ids?api_key=" + api_key
match_history_response = requests.get(match_history)

match_history_df = pd.DataFrame(match_history_response.json())

# Initializting final dataframe
all_games_df = pd.DataFrame()


# List of Items and ID
page = requests.get("https://darkintaqt.com/blog/league-item-id-list/")
soup = BeautifulSoup(page.content, 'html.parser')

item_list = []

for items in soup.find_all("li"):
    item_list.append(items.text)

item_list_df = pd.DataFrame(item_list)

item_list_df[['itemID', 'itemName']] = item_list_df[0].str.split(':', expand = True)
item_list_df.drop(0, axis = 1, inplace = True)
item_list_df['itemID'] = pd.to_numeric(item_list_df['itemID'])



for index, match_id in match_history_df.iterrows():
    match_id_url = "https://americas.api.riotgames.com/lol/match/v5/matches/" + str(match_id[0]) + "?api_key=" + api_key

    match_id_response = requests.get(match_id_url)

    json_res = match_id_response.json()

    match_info = json_res['info']

    game_info = pd.json_normalize(match_info, record_path = ['participants'], meta = ['gameId', 'gameMode', 'gameCreation'])
    game_info_df = game_info[['gameId', 'gameMode', 'gameCreation', 'teamId',
                             'championName', 'champLevel', 'goldEarned', 'individualPosition',
                              'kills', 'deaths', 'assists',
                              'item0', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6',
                              'summoner1Id', 'summoner2Id',
                              'summonerName',
                              'totalDamageDealt', 'totalDamageTaken', 'totalHeal', 'visionScore',
                              'win']]

    game_info_item_name = game_info_df.merge(item_list_df, how = 'left', left_on = "item0", right_on = 'itemID')
    game_info_item_name.rename({'itemName':'item0_Name'}, axis = 1, inplace = True)
    game_info_item_name.drop('itemID', axis = 1, inplace = True)

    game_info_item_name = game_info_item_name.merge(item_list_df, how = 'left', left_on = "item1", right_on = 'itemID')
    game_info_item_name.rename({'itemName':'item1_Name'}, axis = 1, inplace = True)
    game_info_item_name.drop('itemID', axis = 1, inplace = True)

    game_info_item_name = game_info_item_name.merge(item_list_df, how = 'left', left_on = "item2", right_on = 'itemID')
    game_info_item_name.rename({'itemName':'item2_Name'}, axis = 1, inplace = True)
    game_info_item_name.drop('itemID', axis = 1, inplace = True)

    game_info_item_name = game_info_item_name.merge(item_list_df, how = 'left', left_on = "item3", right_on = 'itemID')
    game_info_item_name.rename({'itemName':'item3_Name'}, axis = 1, inplace = True)
    game_info_item_name.drop('itemID', axis = 1, inplace = True)

    game_info_item_name = game_info_item_name.merge(item_list_df, how = 'left', left_on = "item4", right_on = 'itemID')
    game_info_item_name.rename({'itemName':'item4_Name'}, axis = 1, inplace = True)
    game_info_item_name.drop('itemID', axis = 1, inplace = True)

    game_info_item_name = game_info_item_name.merge(item_list_df, how = 'left', left_on = "item5", right_on = 'itemID')
    game_info_item_name.rename({'itemName':'item5_Name'}, axis = 1, inplace = True)
    game_info_item_name.drop('itemID', axis = 1, inplace = True)

    game_info_item_name = game_info_item_name.merge(item_list_df, how = 'left', left_on = "item6", right_on = 'itemID')
    game_info_item_name.rename({'itemName':'item6_Name'}, axis = 1, inplace = True)
    game_info_item_name.drop('itemID', axis = 1, inplace = True)

    all_games_df = pd.DataFrame.append(game_info_item_name, all_games_df)

# Changing unix datestamp to datetime
timestamp = []
for x in all_games_df['gameCreation']:
    timestamp.append(datetime.datetime.fromtimestamp(x/1000.0))

all_games_df['timestamp'] = timestamp

all_games_df['day_of_week'] = all_games_df['timestamp'].dt.day_name()
all_games_df['hour'] = all_games_df['timestamp'].dt.hour

# Convert raw data to Excel
# all_games_df.to_excel("all_games.xlsx", header = True, index = False)

# Importing models
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

# Selecting only games for specific User to prevent duplicates
personal_games = all_games_df[all_games_df['summonerName'] == username]

# Setting X and y for training model
X = personal_games[['kills', 'deaths', 'assists', 'totalDamageDealt']]
y = personal_games['win']
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8)

# Return accuracy score for Decision Tree
model = DecisionTreeClassifier()
model.fit(X_train, y_train)
model.score(X_test, y_test)

# Returning scores for all models
print(cross_val_score(LogisticRegression(), X, y))
print(cross_val_score(DecisionTreeClassifier(), X, y))
print(cross_val_score(RandomForestClassifier(n_estimators = 50), X, y))
print(cross_val_score(SVC(), X, y))
print(cross_val_score(GaussianNB(), X, y))
