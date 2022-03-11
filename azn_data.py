import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
import os
from os import listdir
from os.path import isfile, join
import pandas as pd
from pathlib import Path
import datetime
import pyautogui, sys

pyautogui.FAILSAFE = False
pyautogui.moveTo(pyautogui.size())

urls = [
"https://sellercentral.amazon.com/payments/reports/custom/request?ref_=xx_report_ttab_dash&tbla_daterangereportstable=sort:%7B%22sortOrder%22%3A%22DESCENDING%22%7D;search:undefined;pagination:1;",
'https://sellercentral.amazon.com/reportcentral/AFNInventoryReport/1',
'https://sellercentral.amazon.com/reportcentral/FlatFileAllOrdersReport/1',
'https://sellercentral.amazon.com/reportcentral/CUSTOMER_RETURNS/1',
'https://sellercentral.amazon.com/reportcentral/REPLACEMENT/1',
'https://sellercentral.amazon.com/returns/report/ref=xx_scnvrr_dnav_xx',
'https://sellercentral.amazon.com/reportcentral/INVENTORY_AGE/1',
'https://sellercentral.amazon.com/listing/reports/ref=xx_invreport_dnav_xx'
]

file_path = ['AznPay', 'Amazon Fulfilled Inventory', 'AznAllOrders', 'AznRetrunFBA', 'Replacement',  'AznReturn', 'Age', 'Listing' ]


def get_profile_path(profile):
    FF_PROFILE_PATH = os.path.join(os.environ['APPDATA'],'Mozilla', 'Firefox', 'Profiles')

    try:
        profiles = os.listdir(FF_PROFILE_PATH)
    except WindowsError:
        print("Could not find profiles directory.")
        sys.exit(1)
    try:
        for folder in profiles:
            print(folder)
            if folder.endswith(profile):
                loc = folder
    except StopIteration:
        print("Firefox profile not found.")
        sys.exit(1)
    return os.path.join(FF_PROFILE_PATH, loc)



download_path_root = os.path.join(os.environ['OneDrive'], 'U1')

prof = 'fxlhg0z0.default-release'


today_date = datetime.datetime.now()

DD = datetime.timedelta(days=30)
from_date = today_date - DD

DD = datetime.timedelta(days=1)
to_date = today_date - DD


# Payment Report

for root, dirs, files in os.walk(download_path_root+"\\"+file_path[0]):
    for file in files:
        os.remove(os.path.join(root, file))

print("\n\nFetching Payment Report")




mime_types = "text/csv"
profile = webdriver.FirefoxProfile(get_profile_path(prof))

profile.set_preference("browser.download.folderList",2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[0]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
# profile.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(firefox_profile=profile)

driver.get(urls[0])
driver.maximize_window()
wait = WebDriverWait(driver, 10)

time.sleep(10)
driver.find_element(By.CSS_SELECTOR, '#drrGenerateReportButton').click()
time.sleep(10)
driver.find_element(By.CSS_SELECTOR, '#drrReportRangeTypeRadioCustom').click()
driver.find_element(By.CSS_SELECTOR, '#drrFromDate').send_keys((to_date - datetime.timedelta(days=90)).strftime("%m/%d/%Y"))
driver.find_element(By.CSS_SELECTOR, '#drrToDate').send_keys(to_date.strftime("%m/%d/%Y"))
time.sleep(5)

driver.find_element(By.CSS_SELECTOR, '#drrGenerateReportsGenerateButton').click()
time.sleep(5)


while True:
    tbl_cell = driver.find_element(By.CSS_SELECTOR, 'table tbody .mt-row td.mt-cell:nth-child(4)')
    if tbl_cell.text == 'Download':
        tbl_cell.find_element(By.CSS_SELECTOR, '#downloadButton').click()
        break
    else:

        print("In Progress")
        driver.refresh()
        time.sleep(10)

time.sleep(60)

driver.quit()


# Amazon Fulfilled Inventory


for root, dirs, files in os.walk(download_path_root+"\\"+file_path[1]):
    for file in files:
        os.remove(os.path.join(root, file))

print("\n\nFetching Amazon Fulfilled Inventory Report")

mime_types = "text/csv"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[1]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)


driver = webdriver.Firefox(firefox_profile=profile)

driver.maximize_window()
wait = WebDriverWait(driver, 10)

driver.get(urls[1])
time.sleep(60)
driver.find_element(By.CSS_SELECTOR, 'kat-button[label="Request .csv Download"]').click()
time.sleep(10)
table_row = driver.find_elements(By.CSS_SELECTOR, 'kat-table-row')


while True:
    table_cell = table_row[1].find_elements(By.CSS_SELECTOR, 'kat-table-cell')[4]
    if table_cell.text == 'Download':
        table_cell.find_element(By.CSS_SELECTOR, 'kat-button[label="Download"]').click()
        break

    else:
        print('In Progress')
        time.sleep(60)
        continue

time.sleep(60)

driver.quit()


for root, dirs, files in os.walk(download_path_root+"\\"+file_path[2]):
    for file in files:
        os.remove(os.path.join(root, file))

# All orders

print("\n\nFetching Orders Report")

mime_types = "text/plain"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[2]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)


driver = webdriver.Firefox(firefox_profile=profile)

driver.maximize_window()
wait = WebDriverWait(driver, 10)

driver.get(urls[2])
time.sleep(10)
drp_down = driver.find_element(By.CSS_SELECTOR, 'kat-dropdown')
drp_down.click()
time.sleep(3)

drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.RETURN)


time.sleep(2)
x=1
t= today_date - datetime.timedelta(days=1)
f = t - datetime.timedelta(days=30)

while x<=3 :
    driver.execute_script("document.querySelector('#daily-time-picker-kat-date-range-picker').setAttribute('start-value','"+f.strftime("%m/%d/%Y")+"')")
    driver.execute_script("document.querySelector('#daily-time-picker-kat-date-range-picker').setAttribute('end-value','"+t.strftime("%m/%d/%Y")+"')")

    driver.find_element(By.CSS_SELECTOR, 'kat-button[label = "Request Download"]').click()
    time.sleep(10)
    table_row = driver.find_elements(By.CSS_SELECTOR, 'kat-table-body kat-table-row')
    table_cell = table_row[0].find_elements(By.CSS_SELECTOR, 'kat-table-cell')
    while True:
        try:
            download_btn = table_cell[3].find_element(By.CSS_SELECTOR, 'kat-button[label="Download"]')
            download_btn.click()
            break
        except NoSuchElementException as exp :
            print("In Progress")
            time.sleep(60)
            continue
    t= f-datetime.timedelta(days = 1)
    f = t - datetime.timedelta(days = 30)
    x+=1

time.sleep(60)
driver.quit()

for root, dirs, files in os.walk(download_path_root+"\\"+file_path[3]):
    for file in files:
        os.remove(os.path.join(root, file))

# Customer Return

print("\n\nFetching FBA Customer Return Report")

mime_types = "text/csv"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[3]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)


driver = webdriver.Firefox(firefox_profile=profile)
driver.get(urls[3])

driver.maximize_window()
wait = WebDriverWait(driver, 10)



time.sleep(60)
drp_down = driver.find_element(By.CSS_SELECTOR, 'kat-dropdown')
drp_down.click()
time.sleep(10)

drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.RETURN)

time.sleep(3)


t= today_date - datetime.timedelta(days=1)
f = t - datetime.timedelta(days=30)
x=1
while x<=3 :
    driver.execute_script("document.querySelector('#daily-time-picker-kat-date-range-picker').setAttribute('start-value','"+f.strftime("%m/%d/%Y")+"')")
    driver.execute_script("document.querySelector('#daily-time-picker-kat-date-range-picker').setAttribute('end-value','"+t.strftime("%m/%d/%Y")+"')")


    driver.find_element(By.CSS_SELECTOR, 'kat-button[label = "Request .csv Download"]').click()

    time.sleep(10)
    table_row = driver.find_elements(By.CSS_SELECTOR, 'kat-table-body kat-table-row')
    table_cell = table_row[0].find_elements(By.CSS_SELECTOR, 'kat-table-cell')


    while True:
        try:
            download_btn = table_cell[4].find_element(By.CSS_SELECTOR, 'kat-button[label="Download"]')
            download_btn.click()
            break
        except NoSuchElementException as exp :
            print("In Progress")
            time.sleep(60)
            continue

    t= f-datetime.timedelta(days = 1)
    f = t - datetime.timedelta(days = 30)
    x+=1
time.sleep(60)
driver.quit()

for root, dirs, files in os.walk(download_path_root+"\\"+file_path[4]):
    for file in files:
        os.remove(os.path.join(root, file))

# replacement

print("\n\nFetching Replacement Report")

mime_types = "text/csv"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[4]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)


driver = webdriver.Firefox(firefox_profile=profile)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
driver.get(urls[4])


time.sleep(60)

drp_down = driver.find_element(By.CSS_SELECTOR, 'kat-dropdown')
drp_down.click()
time.sleep(10)

drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.DOWN)
drp_down.send_keys(Keys.RETURN)
time.sleep(5)
x=1
t= today_date - datetime.timedelta(days=1)
f = t - datetime.timedelta(days=30)

while x<=3 :
    driver.execute_script("document.querySelector('#daily-time-picker-kat-date-range-picker').setAttribute('start-value','"+f.strftime("%m/%d/%Y")+"')")
    driver.execute_script("document.querySelector('#daily-time-picker-kat-date-range-picker').setAttribute('end-value','"+t.strftime("%m/%d/%Y")+"')")

    driver.find_element(By.CSS_SELECTOR, 'kat-button[label = "Request .csv Download"]').click()
    time.sleep(10)
    table_row = driver.find_elements(By.CSS_SELECTOR, 'kat-table-body kat-table-row')
    table_cell = table_row[0].find_elements(By.CSS_SELECTOR, 'kat-table-cell')

    time.sleep(5)
    table_row = driver.find_elements(By.CSS_SELECTOR, 'kat-table-body kat-table-row')
    table_cell = table_row[0].find_elements(By.CSS_SELECTOR, 'kat-table-cell')

    while True:
        if table_cell[4].text == 'In Progress':
            print('In Progress')
            time.sleep(60)
            continue
        elif table_cell[4].text == 'No Data Available':
            print('No Data Available')
            break
        else:
            try:
                download_btn = table_cell[4].find_element(By.CSS_SELECTOR, 'kat-button[label="Download"]')
                download_btn.click()
                break
            except NoSuchElementException as exp :
                print("In Progress")
                time.sleep(60)
                continue
    t= f-datetime.timedelta(days = 1)
    f = t - datetime.timedelta(days = 30)
    x+=1
time.sleep(60)

driver.quit()

# Customer Returns
for root, dirs, files in os.walk(download_path_root+"\\"+file_path[5]):
    for file in files:
        os.remove(os.path.join(root, file))


print("\n\nFetching Customer Return Report")

mime_types = r"application/x-xml"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[5]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)


driver = webdriver.Firefox(firefox_profile=profile)
driver.maximize_window()
wait = WebDriverWait(driver, 10)


driver.get(urls[5])
time.sleep(10)


t= today_date - datetime.timedelta(days=1)
f = t - datetime.timedelta(days=30)
x=1
while x<=3 :

    drp_down = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div/div[3]/div/div[2]/div[1]/span[1]/span/span/span')
    drp_down.click()
    time.sleep(3)
    opts = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/ul/li')

    for opt in opts:
        if opt.text == 'All Returns':
            opt.click()


    drp_down = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/div/div/div[1]/div/div[3]/div/div[2]/div[1]/div[1]/span[2]/span/span')
    drp_down.click()
    time.sleep(3)
    opt = driver.find_element(By.XPATH, '/html/body/div[4]/div/div/ul/li[4]')
    opt.click()
    # driver.find_element(By.XPATH, '/html/body/div[4]/div/div/ul/li[3]')
    driver.find_element(By.CSS_SELECTOR, "#adhocReportFromDateInput").send_keys(f.strftime("%m/%d/%Y"))
    driver.find_element(By.CSS_SELECTOR, "#adhocReportToDateInput").send_keys(t.strftime("%m/%d/%Y"))
    driver.find_element(By.CSS_SELECTOR, '#buttonRequestAdhocReport').click()
    time.sleep(3)
    refresh_btn = driver.find_element(By.CSS_SELECTOR, '#buttonReturnsReportRefresh')
    refresh_btn.click()

    time.sleep(3)
    row = driver.find_elements(By.CSS_SELECTOR, '#returnsReportListBody .reportRequestRecord')[0]
    tbl_cell = row.find_elements(By.CSS_SELECTOR, '.a-span-last')[1]
    # print(tbl_cell.text)
    while True:
        row = driver.find_elements(By.CSS_SELECTOR, '#returnsReportListBody .reportRequestRecord')[0]
        tbl_cell = row.find_elements(By.CSS_SELECTOR, 'div.a-row div.a-column.a-span3.a-span-last div.a-row div.a-column.a-span6')[0]
        if tbl_cell.text == 'In progress':
            print('In Progress')
            driver.refresh()
            time.sleep(10)
            continue
        else:
            try:
                download_btn = tbl_cell.find_elements(By.CSS_SELECTOR, '.a-button')[0]
                download_btn.click()
                break
            except NoSuchElementException as exp :
                print("hello")
                driver.refresh()
                time.sleep(10)
                continue
    t= f-datetime.timedelta(days = 1)
    f = t - datetime.timedelta(days = 30)
    x+=1

time.sleep(60)

driver.quit()


for root, dirs, files in os.walk(download_path_root+"\\"+file_path[6]):
    for file in files:
        os.remove(os.path.join(root, file))

#Inventory Age



print("\n\nFetching Inventory Age Report")

mime_types = r"text/csv"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[6]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)


driver = webdriver.Firefox(firefox_profile=profile)
driver.maximize_window()
wait = WebDriverWait(driver, 10)
driver.get(urls[6])
time.sleep(60)
driver.find_element(By.CSS_SELECTOR, 'kat-button[label="Request .csv Download"]').click()
time.sleep(10)
table_row = driver.find_elements(By.CSS_SELECTOR, 'kat-table-row')


while True:
    table_cell = table_row[1].find_elements(By.CSS_SELECTOR, 'kat-table-cell')[4]
    if table_cell.text == 'Download':
        table_cell.find_element(By.CSS_SELECTOR, 'kat-button[label="Download"]').click()
        break

    else:
        print('In Progress')
        time.sleep(60)
        continue

time.sleep(60)

driver.quit()


# Listing report


for root, dirs, files in os.walk(download_path_root+"\\"+file_path[7]):
    for file in files:
        os.remove(os.path.join(root, file))

print("\n\nListing Report")


mime_types = "text/plain"
profile = webdriver.FirefoxProfile(get_profile_path(prof))
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", os.path.join(download_path_root, file_path[7]))
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", mime_types)
profile.set_preference("plugin.disable_full_page_plugin_for_types", mime_types)
# profile.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(firefox_profile=profile)

driver.get(urls[7])
driver.maximize_window()
wait = WebDriverWait(driver, 10)

time.sleep(10)


drp_down = driver.find_element(By.CSS_SELECTOR, '#reportVariantClick')
drp_down.click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, 'ul li[aria-labelledby="dropdown1_7"] ').click()
time.sleep(1)
driver.find_element(By.CSS_SELECTOR, 'input[name="report-request-button"] ').click()


time.sleep(20)

def func_download():
    try:
        loop_checker=False

        while True:
            data_row = driver.find_elements(By.CSS_SELECTOR, '#reports-table tr')

            for x in range(1,len(data_row)):
                rt_type=data_row[x].find_element(By.CSS_SELECTOR, 'td[data-column="report_type"]').text
                rt_status=data_row[x].find_element(By.CSS_SELECTOR, 'td[data-column="status"]').text

                if rt_type == "All Listings Report (Custom)":

                    if rt_status == "Ready":
                        data_row[x].find_element(By.CSS_SELECTOR, 'td[data-column="report_download"]').click()
                        loop_checker=True
                        print("if:breaking inner loop")
                        time.sleep(10)
                        break
                    else:
                        time.sleep(5)
                        print("else:breaking inner loop")
                        break
            if loop_checker==True:
                print("breaking outer loop")
                break
            time.sleep(5)
    except:
        print("exception")
        time.sleep(3)
        func_download()

func_download()


driver.quit()
