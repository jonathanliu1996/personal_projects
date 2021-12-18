# Project goal: Utilizing Selenium to webscrape campaign performace report as API access does not exist

# import packages
from selenium import webdriver
import getpass
import time
import shutil
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd


webdriver.get("file:///D:/folder/abcd.html");

# Setting webdriver parameters

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

prefs = {"download.default_directory" : "C:\\Users\\download_location"}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome(chrome_options=options)


wd.get('https://console.krux.com/marketing/performance/?activeTab=campaigns')

email_area = wd.find_element_by_name('email')
email_area.send_keys(raw_input("Email: "))

password_area = wd.find_element_by_name('password')
password_area.send_keys(getpass.getpass(prompt="Password: "))

log_in_button = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/ui-view/div/div[1]/div[1]/div/div/div[3]/form/div/div[3]/button')
log_in_button.click()


#Display campaign names
list_of_campaigns = ['NuvaRing 2019 Digital','Nexplanon 2019 Digital ','Belsomra Digital 2019','Keytruda Lung Digital 2019',
'P23 Digital 2019','Keytruda Melanoma Digital 2019  2','Gardasil Get Smarter 2019 Digital','Steglatro Digital 2019',
'Keytruda TNBC Digital 2019','Keytruda Head & Neck Digital 2019','How 2 Type 2 Digital 2019','G9 Moms Digital 2019',
'Januvia Digital 2019','Keytruda MSI-H Digital 2019','Keytruda UC Digital 2019','Keytruda RCC Digital 2019',
'P23 Digital 2019 Partner Makegood','Isentress Hornet AV 2019','Isentress Digital 2019']

#Video campaign names
list_of_campaigns = ['Gardasil Adolescent OTT 2019', 'Keytruda Lung Video 2019', 'Gardasil Adolescent FEP 2019',
'Nexplanon 2019 Video', 'Keytruda OTT 2019', 'Gardasil Moms Video 2019', 'P23 Video 2019', 'Gardasil Young Adults Video 2019',
'KEYTRUDA FEP 2019','Belsomra Video 2019']

#Mobile
list_of_campaigns = ['Nexplanon 2019 Digital ','P23 Digital 2019','Januvia Digital 2019','Gardasil Get Smarter 2019 Digital',
'Steglatro Digital 2019','Belsomra Digital 2019','G9 Moms Digital 2019']

#Variable to add to file name - Display, Video or Mobile
channel = "Mobile"

for x in list_of_campaigns:

    list_50_campaigns = wd.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/ui-view/form/div/div/div[5]/div/div/div/div[3]/div/div[2]/div[1]/select/option[3]")
    list_50_campaigns.click()
    time.sleep(3)

    print("Looking for campaign: " + x)
    time.sleep(1)

    try:
        select_campaign = wd.find_element_by_xpath("//a[contains(.,'%s')]" % x)
    except:
        print("Could not find campaign:" + x)
        pass
    else:
        print("Found campaign")
        select_campaign.click()

    time.sleep(10)


    #Downloading files
    print("Downloading files")

    number_of_files = os.listdir("C:\\Users\\Jonathan.Liu2\\Desktop\\Discrepancy\\All_Reports")
    number_files = len(number_of_files)

    download_files = wd.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/ui-view/form/div/div/div[3]/kx-export/button")
    download_files.click()
    campaign = wd.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]/ui-view/form/div/div/div[2]/div/div")
    campaign_name = campaign.text

    new_number_files = number_files + 1

    while number_files != new_number_files:
        number_of_files = os.listdir("C:\\Users\\download_location")
        number_files = len(number_of_files)
        print ("Waiting for file to download")
        time.sleep(5)


    try:
        filepath = "C:\\Users\\download_location"
        filename = max([filepath + "\\" + f for f in os.listdir("C:\\Users\\download_location")], key=os.path.getctime)
        new_filename = filepath + "\\" + campaign_name + "-"  + channel + ".csv"
    except:
        print("Error with file name")

    os.rename(filename,new_filename)
    print("File has been renamed")


    #Returning to all campaigns
    print("Returning to all campaigns")
    return_to_campaigns = wd.find_element_by_xpath("/html/body/div[1]/div[2]/nav/div/div[2]/ul/li[2]/a")
    return_to_campaigns.click()
    time.sleep(5)


# Location where all files have been saved, for Video Mobile and Display
video_path = ("C:\\Users\\download_location\\Video")
mobile_path = ("C:\\Users\\download_location\\Mobile")
display_path = ("C:\\Users\\download_location\\Display")


# Updating each video report file

df_final_video = pd.DataFrame()

for x in video_files:
    file_path = video_path + "\\\\" + x

    df_summary = pd.read_excel(file_path, 'Summary')
    df_placement = pd.read_excel(file_path, 'Placements', dtype={'Impressions':int,'Clicks':int})

    df_summary_name = df_summary.iloc[4]['Value']
    df_summary_id = df_summary.iloc[6]['Value']
    df_summary_channel = df_summary.iloc[7]['Value']

    df_placement.insert(0,'Campaign Name', df_summary_name)
    df_placement.insert(1,'Campaign ID', df_summary_id)
    df_placement.insert(2,'Channel', df_summary_channel)

    df_final_video = df_final_video.append(df_placement)

df_final_video['Campaign ID'] = pd.to_numeric(df_final_video['Campaign ID'])
# display(df_final_video['Campaign Name'].unique())

# Updating each Mobile report file

df_final_mobile = pd.DataFrame()

for x in mobile_files:
    file_path = mobile_path + "\\\\" + x

    df_summary = pd.read_excel(file_path, 'Summary')
    df_placement = pd.read_excel(file_path, 'Placements')

    df_summary_name = df_summary.iloc[4]['Value']
    df_summary_id = df_summary.iloc[6]['Value']
    df_summary_channel = df_summary.iloc[7]['Value']

    df_placement.insert(0,'Campaign Name', df_summary_name)
    df_placement.insert(1,'Campaign ID', df_summary_id)
    df_placement.insert(2,'Channel', df_summary_channel)

    df_final_mobile = df_final_mobile.append(df_placement)

df_final_mobile['Campaign ID'] = pd.to_numeric(df_final_mobile['Campaign ID'])
# display(df_final_mobile['Campaign Name'].unique())

# Updating each Display report file

df_final_display = pd.DataFrame()

for x in display_files:
    file_path = display_path + "\\\\" + x

    df_summary = pd.read_excel(file_path, 'Summary')
    df_placement = pd.read_excel(file_path, 'Placements')

    df_summary_name = df_summary.iloc[4]['Value']
    df_summary_id = df_summary.iloc[6]['Value']
    df_summary_channel = df_summary.iloc[7]['Value']

    df_placement.insert(0,'Campaign Name', df_summary_name)
    df_placement.insert(1,'Campaign ID', df_summary_id)
    df_placement.insert(2,'Channel', df_summary_channel)

    df_final_display = df_final_display.append(df_placement)

df_final_display['Campaign ID'] = pd.to_numeric(df_final_display['Campaign ID'])
# display(df_final_display['Campaign Name'].unique())

# Consolidated all Display, Mobile and Video reports into 1 file
df_final_channels = pd.concat([df_final_display, df_final_mobile, df_final_video])
df_final_channels.reset_index(drop = True, inplace = True)

df_final_channels.to_excel("Consolidated_Files.xlsx", header = True, index = False)
