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
df_MidlevelW = df2[df2['Area']=='Midlevelwest']
df_MidlevelCentral = df2[df2['Area']=='Midlevelcentral']
df_SKW = df2[df2['Area']=='Shaukeiwan']
df_Happy =df2[df2['Area']=='Happyvalley']
df_NP =df2[df2['Area']=='Northpoint']
df_MLNP =df2[df2['Area']=='Midlevelnorthpoint']
df_QB =df2[df2['Area']=='Quarrybay']
df_SW =df2[df2['Area']=='Sheungwan']


# Groupby area to investigate questions below
gp = df2.groupby('Area')
gp.count()
gp['Price(000)/sqft'].describe()


# Q:  Which area has the most transaction?
# Ans: Shaukeiwan, Northpoint, KennedyTown/SYP

# Q: Which area has the highest price per sqft?
# Ans: Midlevel Central

# Q: Which area has the highest price variation?
# Ans: Happyvalley, Midlevelcentral, Northpoint

# Q: How has price dropped with building age?
# Ans: There is a clear downward trend with the building age with a few exception and except MidLevelCentral. 
# MidLevelCentral has the highest value retention. The price is pretty consistent from 20-40 yo. And a huge drop from 40 years old onwards.

# Let's look at how prices across areas are related
plt.figure()
corr_map1 = df2.groupby(['Area','B. Age'])['Price(000)/sqft'].mean().unstack(level=0).corr()
sns.heatmap(corr_map1,annot = True)

corr_map2 = df2.corr()
sns.heatmap(corr_map2,annot = True)


# Q: Any feature has higher correlation?
# Ans: Price/ per squarefeet has 0.49 correlation with Saleable Area, and 0.37 with Area_code
stat, p = pearsonr(df2['Price(000)/sqft'],df2['Saleable Area'])
stat1, p1 = pearsonr(df2['Price(000)/sqft'],df2['Area_code'])
stat2, p2 = pearsonr(df2['Price(000)/sqft'],df2['B. Age'])

x1 = df_WC.groupby('B. Age')['Price(000)/sqft'].mean()
x2 = df_KTown.groupby('B. Age')['Price(000)/sqft'].mean()
x3 = df_Happy.groupby('B. Age')['Price(000)/sqft'].mean()
x4 = df_SKW.groupby('B. Age')['Price(000)/sqft'].mean()
x5 = df_SW.groupby('B. Age')['Price(000)/sqft'].mean()
x6 = df_MidlevelCentral.groupby('B. Age')['Price(000)/sqft'].mean()

x7 = df_QB.groupby('B. Age')['Price(000)/sqft'].mean()
x8 = df_MLNP.groupby('B. Age')['Price(000)/sqft'].mean()
x9 = df_NP.groupby('B. Age')['Price(000)/sqft'].mean()
x10 = df_MidlevelW.groupby('B. Age')['Price(000)/sqft'].mean()

plt.figure()
plt.plot(x1.index,x1,'-o',color = 'orange',label = 'Wanchai')
plt.plot(x2.index,x2,'-*',color = 'blue',label = 'Kennedy Town')
plt.plot(x3.index,x3,'--',color = 'cyan',label = 'Happy Valley')
plt.plot(x4.index,x4,'-.',color = 'black',label = 'Shau Kei Wan')
plt.plot(x5.index,x5,'-.',color = 'green',label = 'Sheung Wan')

plt.figure()
plt.plot(x6.index,x6,'-o',color = 'orange',label = 'MidlevelCentral')
plt.plot(x7.index,x7,'-*',color = 'blue',label = 'QuarryBay')
plt.plot(x8.index,x8,'--',color = 'cyan',label = 'Mid Level North Point')
plt.plot(x9.index,x9,'-.',color = 'black',label = 'North Point')
plt.plot(x10.index,x10,'-.',color = 'green',label = 'Mid level West')


plt.suptitle("Building Age vs Price per square feet")
plt.xlabel('Building Age')
plt.ylabel('Price(000)/sqft')
plt.legend(bbox_to_anchor=(1, 1), loc='upper left', borderaxespad=0.)


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


regressor = RandomForestRegressor(n_estimators = 25, random_state = 0)
regressor.fit(X_train, Y_train)
Y_pred = regressor.predict(X_test)
regressor.score(X_test,Y_test) #0.7531978314201866