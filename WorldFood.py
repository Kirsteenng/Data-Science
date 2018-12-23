# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 14:55:30 2018

@author: Kirsteen Ng
"""
# Data manipulation
import pandas as pd
import numpy as np
import os
import geopandas as gpd

# Data visualization
import seaborn as sns
import matplotlib as plt


# Read data. Download the data files from https://www.kaggle.com/openfoodfacts/world-food-facts
df = pd.read_csv('D:\Data Science\World Food\world-food-facts\food_data.tsv',delimiter = '\t',encoding ='utf-8')

# Quick check on how many columns contain null values
df.isnull().mean(axis =0).plot.barh()

# Check precisely which columns do not contain null values
# 161/163 columns do not contain null values
df[df.columns[ df.isnull().mean() > 0.0]]

# Choose columns that contain 50% non-null values
food = df[df.columns[ df.isnull().mean() < 0.5]]
food = food.dropna() # Final result with 34 non-null columms
food = food.reset_index(drop=True)
food.info()



# Q1: Which country produces the most food?

# countries_en contains strings separated by comma. The following vectorized method will split rows for selected columns.
food[['countries','product_name']].groupby(['countries'],as_index =False).count().sort_values(by ='product_name',ascending = False)

group_country = food.drop(['code','url','creator','created_t','created_datetime','last_modified_t',
                           'last_modified_datetime','states','states_tags','states_en'],axis= 1)



# product_name, brands, and countries will be the selected columns to investigate food from different countries.
index_product = ['product_name','brands']
separated_by_country = pd.DataFrame(group_country.countries_en.str.split(',').tolist(),index =[group_country['product_name'],group_country['brands']]).stack()
separated_by_country  = separated_by_country.reset_index()[['product_name','brands',0]]
separated_by_country .columns = ['product_name','brands','countries']
countries =separated_by_country['countries'].value_counts()
countries[:20][:-1].plot.barh()

# However this is not efficient if we want to study few columns with countries involved. 
# The following helper function will split countries row while retaining other columns.

    
def SplitDataFrame(df,target_col,separator):
    def SplitListToRows(row,row_acc,target_col,separator):
        #print 'row_acc', row_acc
        #print 'row',row
        split_row = row[target_col].split(separator)
        for s in split_row:
            #print 'split_row',split_row
            new_row = row.to_dict()
            #print 'new_row', new_row
            new_row[target_col] = s
            row_acc.append(new_row)
          #  print row_acc
    new_rows= []
    df.apply(SplitListToRows,axis =1,args = (new_rows,target_col,separator))
    new_df = pd.DataFrame(new_rows)
    
    return new_df

# Which country has the most variety of brands? United States with 134052 products
splited_country = SplitDataFrame(group_country,'countries_en',',')
countries = splited_country[['countries_en','product_name']].groupby(['countries_en'],as_index =False).count().sort_values(by ='product_name',ascending = False)
countries[:20].plot(kind= 'bar' ,x='countries_en',y = 'product_name')


# drop products that cannot represent the country, ie. with product count less than 10
study_list = countries[countries.product_name > 10].countries_en
new_country = splited_country[splited_country.countries_en.isin(study_list)]
 
# In US, which brand has the most products? Meijer with 1543 products
USproduct = new_country [new_country['countries_en'] == 'United States']
USproduct_brand = USproduct[['brands','product_name']].groupby(['brands'],as_index = False).count().sort_values(by ='product_name',ascending = False)

# Food from which country has the most additives? Morocco with 3.846g
additives = new_country[['countries_en','additives_n']].groupby(['countries_en'],as_index =False).mean().sort_values(by ='additives_n',ascending = False)
additives[:20].plot(kind= 'bar' ,x='countries_en',y = 'additives_n')


# Feature Engineering: Label food that is above mean for sugar and fat as junk food, need to find definition of junk food     
means = new_country[['countries_en','nutrition-score-fr_100g','fat_100g','saturated-fat_100g',
                      'carbohydrates_100g','sugars_100g','fiber_100g',
                      'proteins_100g','salt_100g','sodium_100g']].groupby(['countries_en'],as_index =True).mean().sort_values(by ='sugars_100g',ascending = False)


# Will use FR score to assess nutrients because more consistent. Which country has the most nutrients? 
means['nutrition-score-fr_100g'].sort_values(ascending = False) # Serbia has most nutrients with 16.27g
means['fat_100g'].sort_values(ascending = False) # Serbia has most fat with 19.7g
means['sugars_100g'].sort_values(ascending = False) # Brazil has most sugar with 24.95g
means['salt_100g'].sort_values(ascending = False) # Thailand has most salt with 12.69g
 
new_country['junk_food'] = 0
# found out that .at is much faster than .at. and why
for index,row in new_country.iterrows():
   key = row['countries_en']
   if (row['fat_100g'] > means.loc[key].fat_100g and row['sugars_100g'] > means.loc[key].sugars_100g and row['salt_100g'] > means.loc[key].salt_100g):
      # print row['product_name'],row['brands']
       new_country.at[index, 'junk_food'] =1

# Which country has the most junk food?
ex_US = new_country [new_country['countries_en'] != 'United States']
junk = ex_US[['countries_en','junk_food']].groupby(['countries_en'],as_index = False).sum().sort_values(by = 'junk_food',ascending = False)
junk[:20].plot(kind = 'bar', x='countries_en',y = 'junk_food')       
    



