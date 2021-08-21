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
    browser = webdriver.Chrome('/Users/Kirsteenng_1/Data Science/Hong Kong House Price/data/chromedriver',options = options)
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


# def get_data(location,area_name):
#     df_agg = pd.DataFrame([])
#     browser = webdriver.Chrome('D:\Data Science\Hong Kong House Price\chromedriver.exe')
#     browser.get(location)

                                                    
#     #TODO: get row data from table, use this class tbscp1
#     nextpage = True
    
#     while nextpage:
#         try:
#             for i in range(len(buildings)):
               
#                 try:
#                     building_name = buildings[i].text
#                     area = browser.find_elements_by_xpath("//div[@class='title']/following-sibling::div")
#                     print(building_name)
#                     #TODO: loop to create pairwise building name and area
                    
#                     #TODO: think if i click into the page to collect data or not? how to get child element
                    
#                     buildings[i].click()
                
#                     # Getting the relevant data
#                     address = []    
#                     date = []
#                     age = []
#                     price = []
#                     area = []
                    
#                     print('getting data')
#                     element = [address,date,age,price,area]
                    
#                     classes = ['tdtr1addr','tdtr1reg' ,'tdtr1age','tdtr1con','tdtr1area']
                
#                 #TODO: optimize code
#                     for index in range(len(element)):
#                         for j in browser.find_elements_by_class_name(classes[index]):
#                             if j.text != '':
#                                 element[index].append(j.text)
            
#                     #TODO: pop odd number in area
#                     del element[4][2::2]
                                      
#                     df = pd.DataFrame(list(zip(element[0],element[1],element[2],element[3],element[4])))
#                     df['Building Name'] = building_name
#                     df['Area'] = area_name
#                     df.columns = ['Address','Transaction date','B. Age','Transaction Price','Saleable Area','Building Name','Area']
#                     #TODO: combine all df into one big df  
#                     df_agg = df_agg.append(df)
#                     #breakpoint()
#                     browser.back()
#                     time.sleep(2) 
#                 except Exception as err:
#                     print(err)
                    
#             print('going into next page')
#             browser.find_elements_by_class_name('btn-next')[0].click()
            
#         except Exception:
#             nextpage = False
       
#     df_agg.info()        
#     browser.close()
#     return df_agg


# #TODO: clean up data type.


    
# def main():
    
    # Ktown = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=101&info=&code2=&page=0'
    # Wanchai = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=108'
    # Midlevelwest = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=106&info=&code2=&page=0'
    # Midlevelcentral = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=109&info=&code2=&page=0'
    # Sheungwan = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=117&info=&code2=&page=0'
    # HappyValley ='http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=110&info=&code2=&page=0'
    # MidLevelNorthPoint ='http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=111&info=&code2=&page=0'
    # Northpoint = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=112&info=&code2=&page=0'
    # Quarrybay = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=113&info=&code2=&page=0'
    # Shaukeiwan = 'http://www1.centadata.com/epaddresssearch1.aspx?type=district17&code=115&info=&code2=&page=0'
    
    # df = pd.DataFrame([])
    
    # Ktown_data = get_data(Ktown, 'Kennedy Town/SYP')
    # df = df.append(Ktown_data)
    
    # Wanchai_data = get_data(Wanchai,'Wanchai')
    # df = df.append(Wanchai_data)
   
    
    # Midlevelwest_data = get_data(Midlevelwest,'Midlevelwest')
    # df = df.append(Midlevelwest_data)
    
    # Midlevelcentral_data = get_data(Midlevelcentral,'Midlevelcentral')
    # df = df.append(Midlevelcentral_data)
    
    # Sheungwan_data = get_data(Sheungwan,'Sheungwan')
    # df = df.append(Sheungwan_data)
    
    # HappyValley_data = get_data(HappyValley,'Happyvalley')
    # df = df.append(HappyValley_data)
    
    # MidLevelNorthPoint_data = get_data(MidLevelNorthPoint,'Midlevelnorthpoint')
    # df = df.append(MidLevelNorthPoint_data)
    
    # Northpoint_data = get_data(Northpoint,'Northpoint')
    # df = df.append(Northpoint_data)
    
    # Quarrybay_data = get_data(Quarrybay,'Quarrybay')
    # df = df.append(Quarrybay_data)
    
    # Shaukeiwan_data = get_data(Shaukeiwan,'Shaukeiwan')
    # df = df.append(Shaukeiwan_data)
    

    
    

    #df.info()
    
    #combine_data = df.append(Wanchai_data,Midlevelwest_data,Midlevelcentral_data,Sheungwan_data)
    #breakpoint()
   # return df


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