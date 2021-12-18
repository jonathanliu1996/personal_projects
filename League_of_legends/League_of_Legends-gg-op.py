# Webscraping OP.GG (League of Legends website) to gather general gameplay information for a select user

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


user_name = "enter_Username_Here"
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(executable_path=r'/Users/chromedriver', chrome_options=chrome_options)
driver.get("https://na.op.gg/summoner/userName="+user_Name)

drop_down_button = driver.find_elements_by_xpath("//*[@id=\"right_match\"]")

for x in drop_down_button:
    driver.execute_script("arguments[0].scrollIntoView();", x)
    x.click()
    time.sleep(1)


source = driver.page_source
soup = BeautifulSoup(source, "html.parser")

df = pd.DataFrame()


match_number = 1
match = []
game_type = []
team_list = []
control_wards = []
other_wards = []
match_result = []

for GameDetail in soup.find_all("div", {"class": "GameDetail"}):
    for LosingTeam in GameDetail.find_all("table", {"class": "GameDetailTable Result-LOSE"}):
        for LosingTeamContent in LosingTeam.find_all("tbody", {"class": "Content"}):
            for NamesLosingTeam in LosingTeamContent.find_all('td' , {'class' : 'SummonerName Cell'}):
                match.append(match_number)
                team_list.append(NamesLosingTeam.text.replace('\n',''))

            for ControlWards in LosingTeamContent.find_all("div", {"class": "Buy"}):
                match_result.append("LOSE")
                control_wards.append(ControlWards.get_text().replace('\n',''))
                other_wards.append((ControlWards.find_next_sibling("div").text.replace('\n','').replace('\t','')))
                game_type.append((GameDetail.parent.parent.find("div", {"class": "GameType"}).get_text().replace('\n','').replace('\t','')))


    for WinningTeam in GameDetail.find_all("table", {"class": "GameDetailTable Result-WIN"}):
        for WinningTeamContent in WinningTeam.find_all("tbody", {"class": "Content"}):
            for NamesWinningTeam in WinningTeamContent.find_all('td' , {'class' : 'SummonerName Cell'}):
                match.append(match_number)
                team_list.append(NamesWinningTeam.text.replace('\n',''))

            for ControlWards in WinningTeamContent.find_all("div", {"class": "Buy"}):
                match_result.append("WIN")
                control_wards.append(ControlWards.get_text().replace('\n',''))
                other_wards.append((ControlWards.find_next_sibling("div").text.replace('\n','').replace('\t','')))
                game_type.append((GameDetail.parent.parent.find("div", {"class": "GameType"}).get_text().replace('\n','').replace('\t','')))

    match_number += 1


df['Match_Number'] = match
df['Match_Result'] = match_result
df['Summoner'] = team_list
df['Control_Wards'] = control_wards
df['Wards_Placed_Killed'] = other_wards
df['Game_Type'] = game_type

df.to_excel("League_Results.xlsx", index = False, header = True)
