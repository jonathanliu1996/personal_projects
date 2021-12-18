# Project goal: Downloading frequency reports for each campaign

# import packages
from selenium import webdriver
import getpass
import time
import shutil
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from os import listdir
from os.path import isfile, join
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument("--test-type")

prefs = {"download.default_directory" : "C:\\Users\\download_location"}
options.add_experimental_option("prefs",prefs)

wd = webdriver.Chrome(chrome_options=options)

wd.get('https://console.krux.com/iris/frequency-reports-iris')

email_area = wd.find_element_by_name('email')
email_area.send_keys(raw_input("Email: "))

password_area = wd.find_element_by_name('password')
password_area.send_keys(getpass.getpass(prompt="Password: "))

log_in_button = wd.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/ui-view/div/div[1]/div[1]/div/div/div[3]/form/div/div[3]/button')
log_in_button.click()


#Switching to data visualization iframe
iframe = wd.find_element_by_xpath('//*[@id="vizContainer"]/iframe')
wd.switch_to_frame(iframe)


#Downloading the reports after setting all parameters
def downloading_Files():
    click_inside_graph = wd.find_element_by_xpath('//*[@id="view3229496257427718365_16378628002420611836"]/div[1]/div[2]/canvas[2]')
    click_inside_graph.click()
    click_inside_graph.click()
    click_inside_graph.click()
    main_download_button = wd.find_element_by_xpath('//*[@id="toolbar-container"]/div[1]/div[2]/div[3]')
    main_download_button.click()
    download_data_button = wd.find_element_by_xpath('//*[@id="DownloadDialog-Dialog-Body-Id"]/div/div[2]')
    download_data_button.click()
    window_after = wd.window_handles[1]
    wd.switch_to.window(window_after)
    print("Switching to download page")
    time.sleep(7)
    full_data_button = wd.find_element_by_xpath('//*[@id="tab-view-full-data"]')
    full_data_button.click()
    print("Switching to Full data page")
    time.sleep(7)
    show_all_columns = wd.find_element_by_xpath('//*[@id="tabContent-panel-underlying"]/div[2]/div/label/div[1]/input')
    show_all_columns.click()
    download_all_data = wd.find_element_by_xpath('//*[@id="tabContent-panel-underlying"]/div[1]/div[2]/a')
    download_all_data.click()
    print("Downloading data")
    window_before = wd.window_handles[0]
    wd.switch_to.window(window_before)
    iframe = wd.find_element_by_xpath('//*[@id="vizContainer"]/iframe')
    wd.switch_to_frame(iframe)
    print("Switching back to Frequency report page")
    time.sleep(10)

#List of all campaigns for suppression
list_of_campaigns = ['Belsomra Digital 2019',
                     'G9 Moms Digital 2019',
                     'Gardasil Moms Video 2019', 'Gardasil Get Smarter 2019 Digital', 'Gardasil Young Adults Video 2019',
                     'Januvia Digital 2019','Januvia Video 2019',
                     'KEYTRUDA FEP 2019','Keytruda Head & Neck Digital 2019', 'Keytruda Lung Digital 2019',
                     'Keytruda Lung Video 2019', 'Keytruda Melanoma Digital 2019  2', 'Keytruda MSI-H Digital 2019',
                     'Keytruda OTT 2019','Keytruda TNBC Digital 2019','Keytruda UC Digital 2019',
                     'Nexplanon 2019 Digital ', 'Nexplanon 2019 Video',
                     'NuvaRing 2019 Digital',
                     'P23 Digital 2019', 'P23 Video 2019',
                     'Steglatro Digital 2019']

#Assigning Lower limit and Upper Limit frequency
Frequency_dict = {}

Frequency_7_12 = [7,12]
Frequency_7_15 = [7,15]
Frequency_7_10 = [7,10]
Frequency_7_25 = [7,25]

Frequency_dict['Belsomra Digital 2019'] = Frequency_7_12

Frequency_dict['G9 Moms Digital 2019'] = Frequency_7_15
Frequency_dict['Gardasil Adolescent FEP 2019'] = Frequency_7_10
Frequency_dict['Gardasil Adolescent OTT 2019'] = Frequency_7_10
Frequency_dict['Gardasil Moms Video 2019'] = Frequency_7_10
Frequency_dict['Gardasil Get Smarter 2019 Digital'] = Frequency_7_15
Frequency_dict['Gardasil Young Adults Video 2019'] = Frequency_7_15

Frequency_dict['Isentress Digital 2019'] = Frequency_7_15
Frequency_dict['Isentress Hornet AV 2019'] = Frequency_7_15

Frequency_dict['Januvia Digital 2019'] = Frequency_7_15
Frequency_dict['Januvia Video 2019'] = Frequency_7_12

Frequency_dict['KEYTRUDA FEP 2019'] = Frequency_7_15
Frequency_dict['Keytruda Lung Video 2019'] = Frequency_7_15
Frequency_dict['Keytruda OTT 2019'] = Frequency_7_15
Frequency_dict['Keytruda Head & Neck Digital 2019'] = Frequency_7_25
Frequency_dict['Keytruda Lung Digital 2019'] = Frequency_7_25
Frequency_dict['Keytruda Melanoma Digital 2019  2'] = Frequency_7_25
Frequency_dict['Keytruda MSI-H Digital 2019'] = Frequency_7_25
Frequency_dict['Keytruda TNBC Digital 2019'] = Frequency_7_25
Frequency_dict['Keytruda UC Digital 2019'] = Frequency_7_25

Frequency_dict['Nexplanon 2019 Digital '] = Frequency_7_15
Frequency_dict['Nexplanon 2019 Video'] = Frequency_7_12

Frequency_dict['NuvaRing 2019 Digital'] = Frequency_7_12

Frequency_dict['P23 Digital 2019'] = Frequency_7_15
Frequency_dict['P23 Video 2019'] = Frequency_7_10

Frequency_dict['Steglatro Digital 2019'] = Frequency_7_15



wd.implicitly_wait(10)

for x in list_of_campaigns:
    drop_down_campaigns = wd.find_element_by_xpath('//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_1"]/div/div[3]/span/div[2]/span')
    time.sleep(5)
    drop_down_campaigns.click()


    print("Looking for this campaign: " + x)
    time.sleep(10)

    try:
        select_campaign_from_list = wd.find_element_by_css_selector('[title="%s"]' % x)
    except:
        print("Could not find campaign:" + x)
        return_back = wd.find_element_by_css_selector('[title=" ***All Campaigns"]')
        return_back.click()
        pass
    else:
        time.sleep(7)
        select_campaign_from_list.click()
        time.sleep(7)
        print("Found campaign: " + x)


    for key in Frequency_dict:
        if str(x) == str(key):

            print("Found campaign, changing limits")
            lower_limit = wd.find_element_by_xpath('//*[@id="typein_[Parameters].[Impressions Parameter]"]/span[1]/input')
            print("Changing Lower Limit for Target Frequency")
            lower_limit.send_keys(Keys.CONTROL + "a")
            lower_limit.send_keys(Frequency_dict[x][0])
            print("Lower Limit has been changed")
            time.sleep(7)

            click_inside_graph = wd.find_element_by_xpath('//*[@id="view3229496257427718365_16378628002420611836"]/div[1]/div[2]/canvas[2]')
            click_inside_graph.click()
            time.sleep(5)

            upper_limit = wd.find_element_by_xpath('//*[@id="typein_[Parameters].[Lower Limit (copy)]"]/span[1]/input')
            print("Changing Upper Limit for Target Frequency")
            upper_limit.send_keys(Keys.CONTROL + "a")
            upper_limit.send_keys(Frequency_dict[x][1])
            print("Upper Limit has been changed")
            time.sleep(7)

            click_inside_graph = wd.find_element_by_xpath('//*[@id="view3229496257427718365_16378628002420611836"]/div[1]/div[2]/canvas[2]')
            click_inside_graph.click()
            time.sleep(5)

            print("Now looking for sites")


            drop_down_site_name = wd.find_element_by_xpath('//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_3"]/div/div[3]/span/div[2]')
            drop_down_site_name.click()
            time.sleep(7)

            parentElement_site_name = wd.find_element_by_xpath('//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_3_menu"]')
            childrenElement_site_name = (parentElement_site_name.text)
            all_sites = childrenElement_site_name.splitlines()

            exit_drop_down_site_name = wd.find_element_by_css_selector('[title=" ***All Sites"]')
            exit_drop_down_site_name.click()


            for y in range(0, len(all_sites)):
                if all_sites[y] == "***All Sites":
                    all_sites[y] = " ***All Sites"

            print(all_sites)

            for w in all_sites:
                drop_down_site_name = wd.find_element_by_xpath('//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_3"]/div/div[3]/span/div[2]')
                time.sleep(10)
                drop_down_site_name.click()
                time.sleep(10)
                picking_site_name = wd.find_element_by_css_selector('[title="%s"]' % w)
                picking_site_name.click()
                time.sleep(10)
                print(w)

                downloading_Files()

                print("Changing file name")
                filepath = "C:\\Users\\Jonathan.Liu2\\Desktop\\Budget Frequency\\Download files Test"

                filename = max([filepath + "\\" + f for f in os.listdir("C:\\Users\\download_location")], key=os.path.getctime)

                time.sleep(5)
                new_filename = filepath + "\\" + x + "-" + w + ".xlsx"
                new_filename = new_filename.replace(" ***","")

                os.rename(filename,new_filename)

            drop_down_site_name = wd.find_element_by_xpath('//*[@id="tableau_base_widget_LegacyCategoricalQuickFilter_3"]/div/div[3]/span/div[2]')
            drop_down_site_name.click()
            picking_site_name = wd.find_element_by_css_selector('[title=" ***All Sites"]')
            picking_site_name.click()

            continue
        else:
            continue

#Combining all files
onlyfiles = [f for f in listdir("C:\\Users\\download_location") if isfile(join("C:\\Users\\download_location", f))]

all_frames = []
for x in onlyfiles:
    df = pd.read_csv("C:\\Users\\download_location" + str(x))
    all_frames.append(df)

result = pd.concat(all_frames)
display(result)

result.to_excel("C:\\Users\\download_location\\All_Reports.xlsx", header = True, index = False,  engine='openpyxl')
