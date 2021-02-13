# -*- coding: utf-8 -*-
## House price crawler

import requests as r
from bs4 import BeautifulSoup as bs
import datetime
import re
import pandas as pd
from selenium import webdriver
import time

#USER_AGENT ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}



def get_data(location,area_name):
    df_agg = pd.DataFrame([])
    browser = webdriver.Chrome('D:\Data Science\Hong Kong House Price\chromedriver.exe')
    browser.get(location)
    buildings = browser.find_elements_by_class_name('tbscp1')
    #TODO: get row data from table, use this class tbscp1
    nextpage = True
    
    while nextpage:
        try:
            for i in range(len(buildings)):
                # TODO: contruct a loop to collect building name
                try:
                    buildings = browser.find_elements_by_class_name('tbscp1')
                    building_name = buildings[i].find_element_by_tag_name('span').text
                    print(building_name)
                    buildings[i].click()
                
                    # Getting the relevant data
                    address = []    
                    date = []
                    age = []
                    price = []
                    area = []
                    
                    print('getting data')
                    element = [address,date,age,price,area]   
                    classes = ['tdtr1addr','tdtr1reg' ,'tdtr1age','tdtr1con','tdtr1area']
                
                #TODO: optimize code
                    for index in range(len(element)):
                        for j in browser.find_elements_by_class_name(classes[index]):
                            if j.text != '':
                                element[index].append(j.text)
            
                    #TODO: pop odd number in area
                    del element[4][2::2]
                                      
                    df = pd.DataFrame(list(zip(element[0],element[1],element[2],element[3],element[4])))
                    df['Building Name'] = building_name
                    df['Area'] = area_name
                    df.columns = ['Address','Transaction date','B. Age','Transaction Price','Saleable Area','Building Name','Area']
                    #TODO: combine all df into one big df  
                    df_agg = df_agg.append(df)
                    #breakpoint()
                    browser.back()
                    time.sleep(2) 
                except Exception as err:
                    print(err)
                    
            print('going into next page')
            browser.find_element_by_link_text('Next Page').click()
            
        except Exception:
            nextpage = False
       
    df_agg.info()        
    browser.close()
    return df_agg


#TODO: clean up data type.


    
def main():
    
    Ktown = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=101&info=&code2=&page=0'
    Wanchai = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=108'
    Midlevelwest = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=106&info=&code2=&page=0'
    Midlevelcentral = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=109&info=&code2=&page=0'
    Sheungwan = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=117&info=&code2=&page=0'
    HappyValley ='http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=110&info=&code2=&page=0'
    MidLevelNorthPoint ='http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=111&info=&code2=&page=0'
    Northpoint = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=112&info=&code2=&page=0'
    Quarrybay = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=113&info=&code2=&page=0'
    Shaukeiwan = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=115&info=&code2=&page=0'
    
    df = pd.DataFrame([])
    
    Ktown_data = get_data(Ktown, 'Kennedy Town/SYP')
    df = df.append(Ktown_data)
    
    Wanchai_data = get_data(Wanchai,'Wanchai')
    df = df.append(Wanchai_data)
   
    
    Midlevelwest_data = get_data(Midlevelwest,'Midlevelwest')
    df = df.append(Midlevelwest_data)
    
    Midlevelcentral_data = get_data(Midlevelcentral,'Midlevelcentral')
    df = df.append(Midlevelcentral_data)
    
    Sheungwan_data = get_data(Sheungwan,'Sheungwan')
    df = df.append(Sheungwan_data)
    
    HappyValley_data = get_data(HappyValley,'Happyvalley')
    df = df.append(HappyValley_data)
    
    MidLevelNorthPoint_data = get_data(MidLevelNorthPoint,'Midlevelnorthpoint')
    df = df.append(MidLevelNorthPoint_data)
    
    Northpoint_data = get_data(Northpoint,'Northpoint')
    df = df.append(Northpoint_data)
    
    Quarrybay_data = get_data(Quarrybay,'Quarrybay')
    df = df.append(Quarrybay_data)
    
    Shaukeiwan_data = get_data(Shaukeiwan,'Shaukeiwan')
    df = df.append(Shaukeiwan_data)
    

    df.info()
    
    #combine_data = df.append(Wanchai_data,Midlevelwest_data,Midlevelcentral_data,Sheungwan_data)
    #breakpoint()
    return df

result = main()
result.to_csv('result.csv')
''' Tests and useful notes
#tic = time.perf_counter()
#toc = time.perf_counter()
#print(toc - tic)



# Test for webdriver
#driver = webdriver.Chrome('D:\Data Science\Hong Kong House Price\chromedriver.exe')
#driver.get('http://www.facebook.com/');
#time.sleep(5)
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
#time.sleep(5) 
#driver.quit() 

'''
