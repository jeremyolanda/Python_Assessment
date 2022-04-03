# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 20:09:52 2022

Web site Search API
Automatic searching and downloading of video clips based on the predefined 
keywords & durations in the google sheet.

@author: Jeremy G. Olanda

"""

import os
import time
import shutil
import os.path as pt
import glob
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def find_files(search_path):    
    for name in glob.glob(search_path):
        return(name)    
        

def web_search_api():
    sheet_url = "https://docs.google.com/spreadsheets/d/1SvvY2nAHRcYM_J6kz3mmKFuPlmKWusl9jaO0-DWZ_0g/edit#gid=0"
    url_1 = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
    df = pd.read_csv(url_1)
    video_keywords = df.iloc[1].tolist()[1:]
    web_api_link1 = df.iloc[5].tolist()[1]
    
    options = Options()
    options.add_argument("download.default_directory=C:\Python_Assessment")
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.set_capability('acceptInsecureCerts', True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    params = {'behavior': 'allow', 'downloadPath':os.getcwd()}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    driver.implicitly_wait(10)
    driver.get(web_api_link1)
    
    videos_num = ['6339299', '3571264', '4478322', '9760429', '6550654', '5513063', '5264778'] 
    
    http_search_vid = 'https://www.pexels.com/search/videos/'
    http_video = 'https://www.pexels.com/video/'
    WebDriverWait(driver, 20) 

    path = "C:\\Python_Assessment"
    destpath = "C:\\Python_Assessment\\videos"
        
    if not pt.exists(destpath):
        os.mkdir(destpath)
                    
    for idx, vid in enumerate(video_keywords):
        search = driver.find_element(By.ID, 'search')
        search.clear()
        search.send_keys(vid)
        search.send_keys(Keys.RETURN)
        driver.get(http_search_vid + vid)
        WebDriverWait(driver, 10)
        driver.get(http_video + videos_num[idx] + '/download/')
        time.sleep(2)
        endTime = time.time() + 5

        while True:
            try:
                file = find_files(path+'\\*.mp4')
                new_file = 'v'+str(idx)+ '_' + file.split('\\')[2]
                os.rename(file.split('\\')[2], new_file)                
                shutil.move(path + "\\" + new_file, destpath + "\\" + new_file)                
            except:
                pass
            time.sleep(1)
            if time.time() > endTime:
                break    
    time.sleep(10)
    driver.quit()

    
if __name__ == "__main__":
    web_search_api()   

    