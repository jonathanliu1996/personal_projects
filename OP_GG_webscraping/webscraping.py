# Webscraping OP.GG (League of Legends website) to gather general gameplay information for a select user

from bs4 import BeautifulSoup
# from selenium import webdriver
import pandas as pd

from functools import partial
from website_preparation import setup_website, show_game_history, expand_game_history
from website_scraping import website_scraping


summoner_username = "Skyce"
chrome_driver_path = "C:\\Users\\Jonathan\\Desktop\\Jupyter_Notebook\\GitHub_Files\\op_gg_webscraping\\src\\chromedriver.exe"

def prepare_website(summoner_username, chrome_driver_path):
    '''
    Open the op.gg website and prepare all the match history to scrape data
        Input: None
        Output: Web driver opened, show game history, and details for each game
    '''

    driver = setup_website(summoner_username, chrome_driver_path)

    game_history_driver = partial(show_game_history, driver)
    game_history_driver(1)

    expand_game_history(driver)

    source = driver.page_source
    soup = BeautifulSoup(source, "html.parser")

    return soup

    
soup = prepare_website(summoner_username, chrome_driver_path)

df = website_scraping(soup)

print(df)

# df.to_excel("League_Results.xlsx", index = False, header = True)
