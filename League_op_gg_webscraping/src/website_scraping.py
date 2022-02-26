import pandas as pd

def website_scraping(soup):
    '''
    Initializing a dataframe and then searching the op.gg website to scrape data
        Input: op.gg soup
        Output: Dataframe
    '''

    df = pd.DataFrame()

    match_number = 1
    match = []
    team_list = []
    damage = []
    cs = []
    control_wards = []
    wards_placed = []
    wards_killed = []
    match_result = []


    for GameDetail in soup.find_all("div", {"class": "css-1dlzamu eo0wf2y0"}):
        for WinningTeam in GameDetail.find_all("table", {"class": 'css-jms47u e15ptgz10'}):
            for WinningTeamContent in WinningTeam.find_all("tr", {"result": "WIN"}):
                for WinningTeamContentName in WinningTeamContent.find_all("td", {"class": "name"}):
                    # print("WINNER: " + WinningTeamContentName.text)
                    match.append(match_number)
                    team_list.append(WinningTeamContentName.text)
                    match_result.append("WIN")
                for WinningTeamContentWards in WinningTeamContent.find_all("td", {"class": "ward"}):
                    for wards in WinningTeamContentWards.children:
                        control_wards.append(wards.select('div')[0].text)
                        wards_placed.append([x.strip() for x in wards.select('div')[1].text.split("/")][0])
                        wards_killed.append([x.strip() for x in wards.select('div')[1].text.split("/")][1])
                for WinningTeamContentDamage in WinningTeamContent.find_all("td", {"class": "damage"}):
                    damage.append(WinningTeamContentDamage.div.getText())
                for WinningTeamContentCS in WinningTeamContent.find_all("td", {"class": "cs"}):
                    cs.append(WinningTeamContentCS.findChild().text)

        for LosingTeam in GameDetail.find_all("table", {"class": 'css-1l89vou e15ptgz10'}):
            for LosingTeamContent in LosingTeam.find_all("tr", {"result": "LOSE"}):
                for LosingTeamContentName in LosingTeamContent.find_all("td", {"class": "name"}):
                    # print("LOSER: " + LosingTeamContentName.text)
                    match.append(match_number)
                    team_list.append(LosingTeamContentName.text)
                    match_result.append("WIN")
                for LosingTeamContentWards in LosingTeamContent.find_all("td", {"class": "ward"}):
                    for wards in LosingTeamContentWards.children:
                        control_wards.append(wards.select('div')[0].text)
                        wards_placed.append([x.strip() for x in wards.select('div')[1].text.split("/")][0])
                        wards_killed.append([x.strip() for x in wards.select('div')[1].text.split("/")][1])
                for LosingTeamContentDamage in LosingTeamContent.find_all("td", {"class": "damage"}):
                    damage.append(LosingTeamContentDamage.div.getText())
                for LosingTeamContentCS in LosingTeamContent.find_all("td", {"class": "cs"}):
                    cs.append(LosingTeamContentCS.findChild().text)

        match_number += 1

    df['Match_Number'] = match
    df['Match_Result'] = match_result
    df['Summoner'] = team_list
    df['Control_Wards'] = control_wards
    df['Wards_Place'] = wards_placed
    df['Wards_Killed'] = wards_killed
    df['Damage'] = damage
    df['cs'] = cs

    return df