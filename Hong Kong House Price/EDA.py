# -*- coding: utf-8 -*-

# Import relevant libraries
import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge as rd
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from scipy.stats import pearsonr
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor

import seaborn as sns
import plotly as pl
import plotly.graph_objects as go
import matplotlib.pyplot as plt
%matplotlib


import time




# Read data
df = pd.read_csv('D:..data/result.csv')

# Fix data type and deal with null value on Saleable area
df = df[df['Address'] != 'Address']
df['B. Age'] = df['B. Age'].astype(int)
df['Transaction Price'] = df['Transaction Price'].replace(['\$','M'],'',regex=True).astype(float)
df['Saleable Area'] = df['Saleable Area'].replace(['s.f.','-'],['',0],regex=True).astype(int)
df2 = df[df['Saleable Area']!=0]
df2.describe()
df2['Price(000)/sqft'] = df2['Transaction Price']/df2['Saleable Area'] * 1000
df2['Transaction date'] = pd.to_datetime(df2['Transaction date'],dayfirst = True)


# Construct encoding for Area and Building name 
#label_encoder = preprocessing.LabelEncoder() # label encoder doesnt work because a high number in this case does not justify the significance of the location.
#df2['Area_code']= label_encoder.fit_transform(df2['Area'])
area_code_dict = {'Midlevelcentral':10, 'Midlevelwest':9,'Sheungwan': 8,'Wanchai':7 ,'Happyvalley': 6,'Kennedy Town/SYP': 6,'Midlevelnorthpoint':5,
             'Northpoint':4,'Quarrybay':3,'Shaukeiwan':2}
df2['Area Code'] = df2['Area'].map(area_code_dict)


# Q: Which period of time has the most transaction?
# Ans: September has the most transaction with 544 number of transactions. 
# The number of transaction has been increasing but the price per square foot presents a cyclical trend. 
# Currently in January, the number of transaction has shown positive sign and price per square foot is approaching the mean.
date = df2.groupby(df2['Transaction date'].dt.month)['Transaction Price'].count()
plt.figure() # to open another window
plt.bar(date.index, date)
plt.title('Change in number of transaction  from July 2020 to Early Jan 2021')
plt.ylabel('Number of Transaction')
plt.xlabel('Transaction Period')

price =  df2.groupby('Transaction date',as_index= False)['Price(000)/sqft'].mean()
plt.figure() # to open another window
plt.plot(price['Transaction date'],price['Price(000)/sqft'],'-o')
plt.axhline(y = price['Price(000)/sqft'].mean(),color ='k', linestyle = '--')
plt.title('Change in transaction price from July 2020 to Early Jan 2021')
plt.ylabel('Price(000)/sqft')
plt.xlabel('Transaction Period')

         
# Studying areas of interest
df_WC = df2[df2['Area']=='Wanchai']
df_KTown =df2[df2['Area']=='Kennedy Town/SYP']
df_MidlevelW = df2[df2['Area']=='Mid Level West']
df_MidlevelCentral = df2[df2['Area']=='Midlevecentral']
df_SKW = df2[df2['Area']=='Shaukeiwan']
df_Happy =df2[df2['Area']=='Happyvalley']
df_NP =df2[df2['Area']=='Northpoint']
df_MLNP =df2[df2['Area']=='MidlevelNorthPoint']

# Groupby area to investigate questions below
gp = df2.groupby('Area')
gp.count()
gp['Price(000)/sqft'].describe()

'''
                    count       mean        std        min        25%  \
Area                                                                    
Happyvalley         192.0  26.180803  14.643098  13.225371  18.967766   
Kennedy Town/SYP    497.0  19.712031   4.779366   8.252427  16.873065   
Midlevelcentral      75.0  28.852442   8.999857  14.834674  22.094238   
Midlevelnorthpoint   77.0  21.010978   4.223552  14.024505  18.163265   
Midlevelwest        287.0  22.975269   4.630832  13.086093  20.040181   
Northpoint          512.0  18.555351   5.958850   8.333333  15.184382   
Quarrybay           284.0  16.267737   3.915956   8.333333  13.551460   
Shaukeiwan          626.0  15.749197   4.189911   5.053191  12.500000   
Sheungwan           134.0  19.567427   3.031740  11.726619  17.684597   
Wanchai             254.0  18.314147   4.514772   9.868421  14.695811   

                          50%        75%         max  
Area                                                  
Happyvalley         22.683351  26.134828  144.388536  
Kennedy Town/SYP    19.337979  21.886121   47.996820  
Midlevelcentral     26.588846  34.164484   49.836525  
Midlevelnorthpoint  20.000000  22.950820   32.085561  
Midlevelwest        22.305764  25.041074   47.057101  
Northpoint          17.230322  20.236351   45.030303  
Quarrybay           16.373038  18.101515   32.996689  
Shaukeiwan          15.568700  18.305961   42.443730  
Sheungwan           19.527981  21.431152   27.500000  
Wanchai             17.514881  21.416546   33.333333  
'''

# Q:  Which area has the most transaction?
# Ans: Shaukeiwan, Northpoint, KennedyTown/SYP

# Q: Which area has the highest price per sqft?
# Ans: Midlevel Central

# Q: Which area has the highest price variation?
# Ans: Happyvalley, Midlevelcentral, Northpoint

# Q: How has price dropped with building age?
# Ans: There is a clear downward trend with the building age with a few exception and except MidLevelCentral. 
# MidLevelCentral has the highest value retention. The price is pretty consistent from 20-40 yo. And a huge drop from 40 years old onwards.

df_old = df2[df2['B. Age'] > 30]
df_old = df_old.groupby(['Area','B. Age'])['Price(000)/sqft'].mean().unstack(level=0) # switching axis, now is x =B.Age, y = Area
for i in df_old.columns[0:5]:
    print('PLoting' + i)
    plt.plot(df_old.index,df_old[i],'-o',label = i)
    
for i in df_old.columns[4::]:
    print('PLoting' + i)
    plt.plot(df_old.index,df_old[i],'-o',label = i)  


# Let's look at how prices across areas are related
plt.figure()
corr_map1 = df2.groupby(['Area','B. Age'])['Price(000)/sqft'].mean().unstack(level=0).corr()
sns.heatmap(corr_map1,annot = True)

corr_map2 = df2.corr()
sns.heatmap(corr_map2,annot = True)

# Q: Any feature has higher correlation?
# Ans: Price/ per squarefeet has 0.49 correlation with Saleable Area, and 0.37 with Area_code
# TODO: Statistical significance?
stat, p = pearsonr(df2['Price(000)/sqft'],df2['Saleable Area'])
stat1, p1 = pearsonr(df2['Price(000)/sqft'],df2['Area_code'])
stat2, p2 = pearsonr(df2['Price(000)/sqft'],df2['B. Age'])

x2 = df_KTown.groupby('B. Age')['Price(000)/sqft'].mean()
x3 = df_Happy.groupby('B. Age')['Price(000)/sqft'].mean()
x4 = df_SKW.groupby('B. Age')['Price(000)/sqft'].mean()
x5 = df_NP.groupby('B. Age')['Price(000)/sqft'].mean()
x6 = df_MidlevelCentral.groupby('B. Age')['Price(000)/sqft'].mean()

plt.figure()
plt.plot(x1.index,x1,'-o',color = 'orange',label = 'Wanchai')
plt.plot(x2.index,x2,'-*',color = 'blue',label = 'Kennedy Town')
plt.plot(x5.index,x5,'--',color = 'cyan',label = 'North Point')
plt.plot(x4.index,x4,'-.',color = 'black',label = 'Shau Kei Wan')
plt.plot(x6.index,x6,'-.',color = 'green',label = 'MidLevelCentral')

plt.suptitle("Building Age vs Price per square feet")
plt.xlabel('Building Age')
plt.ylabel('Price(000)/sqft')
plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)


 
'''
# Not suitable for plotting 3 bars together because the X-axis needs to be precise.
plt.bar(x1,y1,color = 'navy',width= 0.2)
plt.bar(x2+0.2,y2,color = 'green',width= 0.2)
plt.bar(x3+0.4,y3,color = 'red', width= 0.2)

# Plotting bar charts in 3 subplots
# axe is an array with the dimension of row x columns indicated in the subplot arguments, each entry is a subplot object
plt.style.use('seaborn-whitegrid')
fig, axe = plt.subplots(4,1) 


axe[0].plot(x1.index,x1,'-o')
axe[0].set_title('Wanchai')

axe[1].plot(x2.index,x2,'-o')
axe[1].set_title('Kennedy Town')

axe[2].plot(x5.index,x5,'-o')
axe[2].set_title('North Point')

axe[3].plot(x4.index,x4,'-o')
axe[3].set_title('Shau Kei Wan')

'''
plt.figure(0)
plt.bar(x1,y1)
plt.title("Wanchai")

plt.figure(1)
plt.bar(x2,y2)
plt.title("KTown")

plt.figure(3)
plt.bar(x3,y3)
plt.title("Happy Valley")

plt.figure(4)
plt.bar(x4,y4)
plt.title("Shaukeiwan")



# To fit a trend line across all subplots to see the trend more clearly
#GOAL: Understand Ridge regularization
lr = Ridge()
lr.fit(df_WC[['B. Age']],df_WC['Price(000)/sqft'])
plt.plot(df_WC['B. Age'], lr.coef_*df_WC['B. Age']+lr.intercept_, color='orange')

plt.figure(1)
lr.fit(df_KTown[['B. Age']],df_KTown['Price(000)/sqft'])
plt.plot(df_KTown['B. Age'], lr.coef_*df_KTown['B. Age']+lr.intercept_, color='red')

plt.figure(3)
lr.fit(df_Happy[['B. Age']],df_Happy['Price(000)/sqft'])
plt.plot(df_Happy['B. Age'], lr.coef_*df_Happy['B. Age']+lr.intercept_, color='green')

# TODO: try to predict house price per sqft
# Split data into train, test set. Predict using MLR
X_var = df2[['B. Age','Area Code']]
y_var = df2['Price(000)/sqft']
X_train,X_test,Y_train,Y_test = train_test_split(X_var,y_var,test_size = 0.05, random_state=0)
lr = LinearRegression()
lr.fit(X_train,Y_train)
lr.predict(X_test)
print(('R-Squared :'), lr.score(X_test, Y_test))

ridge = rd()
ridge.fit(X_train,Y_train)
pred = ridge.predict(X_test)
ridge.score(X_test,Y_test)
#accuracy_score(Y_test,pred), accuracy score is for classifier.


regressor = RandomForestRegressor(n_estimators = 25, random_state = 0)
regressor.fit(X_train, Y_train)
Y_pred = regressor.predict(X_test)
regressor.score(X_test,Y_test) #0.7531978314201866


# vars= 'B. Age','Area Code'
# R-Squared : R-Squared : 0.40800741373336546

# vars = 'B. Age','Area Code','Saleable Area'
#R-Squared : 0.4842325309015129


#test_df = pd.DataFrame([[0,'a'],[1,'a'],[1,'b'],[3,'b']],columns =['score','category'])
