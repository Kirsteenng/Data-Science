# -*- coding: utf-8 -*-
## House price crawler


import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import ElementClickInterceptedException
# from selenium.common.exceptions import ElementNotInteractableException


#USER_AGENT ={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


'''
Questions to answer
1. Flow analysis - how has the buying and selling been, which areas were more active within which time period
2. House price movement vs housing age
3. House price movement vs area
4. House price movement vs HSI vs Hibor rate
5. Predict price direction

'''
    
    
def get_data(location):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    #chrome_options=options
    browser = webdriver.Chrome('~/Data Science/Hong Kong House Price/data/chromedriver',options = options)
    browser.get(location)
    sub_building,extra_sale = {},{}
    main_pg = browser.window_handles[0]
    
    #to conitnue where I last stopped
    for i in range(0,175):
        print('moving to page ', str(i))
        time.sleep(3)
        browser.find_elements_by_class_name('btn-next')[0].location_once_scrolled_into_view
        browser.execute_script("window.scrollBy(0, arguments[0]);", -200)
        #time.sleep(3)
        WebDriverWait(browser,3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-next'))).click()
        
        
    #total time for 1 row: 65sec, 1 page: 1560sec/26min
    try:

        for j in range(0,150):
            print('*****************      Now at page ',j+175, '******')
            time.sleep(5)
            buildings = browser.find_elements_by_class_name('title-lg') # building name and area
            area_list = browser.find_elements_by_class_name('tag-adress')
            transact = browser.find_elements_by_class_name('date')
            num_build = len(buildings)
            print('number of buildings: ',num_build)
            print('number of area: ',len(area_list))
            
            if num_build == 0:
                print('....no building here, skipping....')
                WebDriverWait(browser,3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-next'))).click()
                continue
             
            if ((j+120) % 10 == 0):
                print('saving some data at page',str(j))
                df_agg = pd.DataFrame.from_dict(sub_building,orient='index',columns=['Date','Area','Name','B.Age','Price', 'Size'])
                df_agg.to_csv('house_transact' + str(j) + '.csv')
                #extra_sale_df = pd.DataFrame.from_dict(extra_sale,orient = 'index',columns = ['Other transaction'])
                #extra_sale_df.to_csv('extra_transact' + str(j) + '.csv')
                sub_building,extra_sale = {},{}
        
            for i in range(0,num_build):
                try:
                    
                    browser.switch_to.window(main_pg)
                    print(' Now at main') 
                    name = buildings[i].text
                    area = area_list[i].text
                    date = transact[i].text
                    #TODO: move items to be click out of the top red banner
                    buildings[i].location_once_scrolled_into_view
                    browser.execute_script("window.scrollBy(0, arguments[0]);", -200)
                    time.sleep(3)
                    buildings[i].click()
                    #link = '//*[@id="__layout"]/div/div[4]/div[4]/div/div[1]/div[' + str(i+2) + ']/a/div[2]/div[1]/span[1]'
                    #WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH,link))).click()
                    #actions.move_to_element(buildings[i]).perform()
                   
                    
                    # move to new page after click
                    browser.switch_to.window(browser.window_handles[-1])
                    
                    print('trying building ',name)
                    time.sleep(3)
                    build = "//p[text()= 'Building Age']//following-sibling::p"
                    b_age = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, build))).text
                    net_price = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME,'price-lbl'))).text # size and price/sqft                 
                    price_sqft = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CLASS_NAME,'fs24'))).text # price
                  
                    print(b_age,' ',net_price,' ',date, ' ',price_sqft)
                    
                    #TODO: to get other relevant transaction data
                    # extra = browser.find_elements_by_id('Category2')[0].text
                    # if (extra != ''):
                    #     extra_sale.update({name:extra})  
                    
                    
                    sub_building.update({name: [date, area, name,b_age,net_price,price_sqft]})
                    print('No error. Going back to main')
                    browser.close()
                    
                    
                    
                # if couldnt get data then close
                except Exception as e:
                    print('having error while clicking on page: ', e)
                    browser.close()
                    
                        
    
            print('Going to next page')
            browser.switch_to.window(main_pg)
            buildings[-1].location_once_scrolled_into_view
            WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-next'))).click()
             
    except Exception as e:
        print('having error while going next page: ', e)
    
    
        
    print('exporting to csv')
    df_agg = pd.DataFrame.from_dict(sub_building,orient='index',columns=['Date','Area','Name','B.Age','Price', 'Size'])
    # extra_sale_df = pd.DataFrame.from_dict(extra_sale,orient = 'index',columns = ['Other transaction'])
    # extra_sale_df.to_csv('extra_transact7.csv')
    return df_agg
           

def main():
    location = 'https://hk.centanet.com/findproperty/en/list/transaction?q=mptTD0GZW0mpDQyHGtyobA'
    data = get_data(location)
    
    data.to_csv('House_transact7.csv')
    return


