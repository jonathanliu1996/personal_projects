import time
from selenium import webdriver

def setup_website(summoner_username, chrome_driver_path):
    '''
    Opening up the web driver and the op.gg website for a specific username
        Input: Username, Chrome Driver path
        Output: op.gg search for username
    '''

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")
    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=chrome_options)
    driver.get("https://na.op.gg/summoner/userName="+ summoner_username)
    return driver


def show_game_history(driver, click_show_more):
    '''
    Page loads up game history for  20 games. The 'Show More' button expands the list 20 more games.
        Input: Int (number of times the 'Show More' button will be clicked)
        Output: (Input * 20) more games will be shown on the web driver page
    '''

    for x in range(click_show_more):
        show_more = driver.find_element_by_xpath("//button[contains(text(), 'Show More')]")
        show_more.click()
        time.sleep(2)


def expand_game_history(driver):
    '''
    To scrape the details of each game, the drop down button must be clicked to expand the history
        Input: None
        Output: Game history detail will be expanded for each game
    '''

    drop_down_button = driver.find_elements_by_class_name("action")

    for x in drop_down_button:
        driver.execute_script("arguments[0].scrollIntoView();", x)
        x.click()
        time.sleep(1)
