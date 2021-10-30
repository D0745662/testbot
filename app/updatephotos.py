# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 15:25:10 2021

@author: DLJW_
"""

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from time import sleep
import requests
from selenium import webdriver
import random

drinks_file = pd.read_csv('cocktails_db1.csv')
# print(drinks_file['Cocktail Name'][1])

# headers = {'cookie': 'ECC=GoogleBot',
#            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

# response = requests.get(drinks_file['Link'][1], headers)

# sleep(1)
# if response.status_code == 200:
#     soup = BeautifulSoup(response.text, 'html.parser')
#     targetimage_id = soup.select('#figure_2-0')[0]
#     print(targetimage_id)
drinks_file['Image'] = [0 for i in range(382)]
temp = 0
url = 'https://www.thecocktaildb.com/'
for data in drinks_file.iterrows():
    
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        driver.find_elements_by_class_name('form-control')[0].send_keys(data[1]['Cocktail Name'])
        driver.find_elements_by_class_name('input-group-btn')[0].find_elements_by_tag_name('button')[0].click()
        img_url = driver.find_element_by_id("feature").find_elements_by_tag_name('img')[0].get_attribute('src')
    except:
        drinks_file['Image'][temp] = None
    else:
        drinks_file['Image'][temp] = img_url
    driver.close()
    print(temp)
    temp+=1
    
drinks_file.to_csv('newcocktails_db1.csv', index = False)







# drinks_file = pd.read_csv('data/newrecipes.csv')
# temp = drinks_file.drop('Unnamed: 0', axis = 1)
# temp.to_csv('data/newrecipes.csv', index = False)