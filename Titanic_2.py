#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 10:44:33 2018

@author: Kirsteenng
"""

# data analysis and manipulation
import pandas as pd
import numpy as np

# visualisation
import matplotlib.pyplot as plt
import seaborn as sns

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
import statsmodels.api as sm
from scipy import stats

# helper functions

def reducing_titles(df):
   for dataset in df:
       df['Title'] = df.Name.str.extract(' ([A-Za-z]+)\.', expand=False)
   pd.crosstab(df.Title,df.Sex)
   df.Title = df.Title.replace(['Lady', 'Countess','Capt', 'Col',\
 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'],'Rare')
   df.Title = df.Title.replace(['Mlle','Ms'],'Miss')
   df.Title = df.Title.replace('Mme','Mrs')
   return

def mapping(df):
   title_mapping = {'Master':0, 'Miss':1, 'Mr':2,'Mrs':3,'Rare':4}
   sex_mapping = {'female':0, 'male':1}
   df.Embarked = df.Embarked.fillna('S') # because 'S' is the mode
   embarked_mapping ={'S':0,'C':1,'Q':2}
   df.Title = df.Title.map(title_mapping)
   df.Sex = df.Sex.map(sex_mapping)
   df.Embarked = df.Embarked.map(embarked_mapping)
   return

def fill_ages(df):
   guess_ages = np.zeros((2,3))
   for dataset in df:
       for i in range(0, 2):
           for j in range(0, 3):
               df[(df['Sex'] == i) & (df['Pclass'] == j+1)]['Age'].dropna()
               guess_df = df[(df['Sex'] == i) & (df['Pclass'] == j+1)]['Age'].dropna()
               guess_df
               guess_ages[i,j]= guess_df.median()


               # Convert random age float to nearest .5 age
               #guess_ages[i,j] = int( age_guess/0.5 + 0.5 ) * 0.5

           for i in range(0, 2):
               for j in range(0, 3):
                   df.loc[ (df.Age.isnull()) & (df.Sex == i) & (df.Pclass == j+1),'Age'] = guess_ages[i,j]

   df['Age'] = df['Age'].astype(int)
   return

def feature_engg(df):
   # Categorizing into age

   df['FamilySize'] =  df['SibSp'] + df['Parch'] + 1
   df['IsAlone'] = 0
   df.IsAlone.loc[df.FamilySize==1] = 1
   return

def dropping(df):
   df = df.drop(['Name','PassengerId','SibSp','Parch','Fare'],axis =1)
   print df.columns
   return

# read data
train_df = pd.read_csv('/Users/Kirsteenng/Desktop/Fun/Titanic/train.csv')
test_df = pd.read_csv('/Users/Kirsteenng/Desktop/Fun/Titanic/test.csv')
combine = [train_df,test_df]

# first few questions to ask:which features are categorical? which features are numerical?
# categorical: Survived,Pclass,Sex,Embarked
# numerical:Age,SibSp,Parch,Fare

train_df.head()
train_df.describe() # only includes numeric data
train_df.describe(include =[np.object]) #only include string objects
train_df.describe(include = 'all') # include all columns
train_df.info()

# Completing:
# now we know age, cabin features have null values, will need to fix these features

# Correcting:
# we know ticket has high duplicate ratio(23%), but shouldn't ticket number be unique?can be dropped?
# name and passenger Id can be dropped as not affecting survival rate

# Clarrifying:
# Hypothesis 1: Women were more likely to survive
# Hypothesis 2: Children (age and parch) are more likely to survive
# Hypothesis 3: Upper class (pclass =1 ) were more likely to survive
# Hypothesis 4: Is there any relationship between embark and pclass?
# Hypothesis 5: Easier to survive if travelling alone?


# Data exploration stage

# Hypothesis 1: 74% female survived while 19% male survived. Female aged 20-38 survived most.
train_df[['Sex','Survived']].groupby(['Sex'],as_index = False).mean().sort_values(by='Survived',ascending= False)
g1 = sns.FacetGrid(train_df, col ='Survived', row ='Sex')
g1.map(plt.hist, 'Age',bins=20)

# Hypothesis 2: 0-4 yo has high survival rate, followed by mid 20s.
# Further explore which age bucket has highest survival rate
train_df[['Parch','Survived']].groupby(['Parch'],as_index = False).mean().sort_values(by='Survived',ascending= False)
train_df[['SibSp','Survived']].groupby(['SibSp'],as_index = False).mean().sort_values(by='Survived',ascending= False)
g2 = sns.FacetGrid(train_df, col= 'Survived')
g2.map(plt.hist, 'Age', bins=20)

# Hypothesis 3: Pclass 1 has highest survival of 63% and decreases with class.
# Obs: Pclass 3 has most passengers, followed by PClass 1 then PClass 2.
train_df[['Pclass','Survived']].groupby(['Pclass'],as_index = False).mean().sort_values(by='Survived',ascending= False)
g3 = sns.FacetGrid(train_df, col ='Survived', row ='Pclass')
g3.map(plt.hist, 'Age',bins=20)


# Hypothesis 4:
g4 = sns.FacetGrid(train_df, row='Embarked', col='Survived', size=2.2, aspect=1.6)
g4.map(sns.barplot, 'Sex','Fare', alpha=.5, ci=None)
g4.add_legend()


reducing_titles(train_df)
mapping(train_df)
fill_ages(train_df)
train_df.info() # ages should be all filled here
feature_engg(train_df)
train_df['AgeBand'] = pd.cut(train_df.Age,5)
AgeBand_mapping = {'(-0.08, 16]':0,'(16, 32]':1,'(32, 48]':2,'(48, 64]':3,'(64, 80]':4}
train_df.Age = train_df.AgeBand.map(AgeBand_mapping)
train_df = train_df.drop(['Name','PassengerId','SibSp','Parch','Fare','AgeBand','Ticket','Cabin'],axis =1)

train_df[['AgeBand','Survived','Pclass','Age']].groupby('AgeBand')['Survived'].mean()

reducing_titles(test_df)
mapping(test_df)
#drop ages == nan
test_df.Age = test_df[np.isnan(test_df.Age) == False]
test_df.info() # ages should be all filled here
feature_engg(test_df)
test_df = test_df.drop(['Name','PassengerId','SibSp','Parch','Fare','AgeBand','Ticket','Cabin'],axis =1)
test_df.info()

#3. Modelling and predicting
X_train = train_df.drop(['Survived'],axis =1)
Y_train = train_df.Survived
X_test = test_df.copy()


# TODO2: find features that have p < 0.05 and remove those greater
logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
Y_pred = logreg.predict(X_test)
acc_log = round(logreg.score(X_train, Y_train) * 100, 2) # The accuracy is 80.36

svc = SVC()
svc.fit(X_train, Y_train)
Y_pred = svc.predict(X_test)
acc_svc = round(svc.score(X_train, Y_train) * 100, 2)

knn = KNeighborsClassifier(n_neighbors = 3 )
knn.fit(X_train, Y_train)
Y_pred = knn.predict(X_test)
acc_knn = round(knn.score(X_train,Y_train) * 100, 2)

gaussian = GaussianNB()
gaussian.fit(X_train,Y_train)
Y_pred = gaussian.predict(X_test) # what is the difference between predict and score
acc_gaussian = round(gaussian.score(X_train, Y_train) * 100, 2)

perceptron = Perceptron()
perceptron.fit(X_train, Y_train)
Y_pred = perceptron.predict(X_test)
acc_perceptron = round(perceptron.score(X_train, Y_train) * 100, 2)

linear_svc = LinearSVC()
linear_svc.fit(X_train, Y_train)
Y_pred = linear_svc.predict(X_test)
acc_linear_svc = round(linear_svc.score(X_train, Y_train) * 100, 2)

sgd = SGDClassifier()
sgd.fit(X_train, Y_train)
Y_pred = sgd.predict(X_test)
acc_sgd = round(sgd.score(X_train, Y_train) * 100, 2)

decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, Y_train)
Y_pred = decision_tree.predict(X_test)
acc_decision_tree = round(decision_tree.score(X_train, Y_train) * 100, 2)

random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_train, Y_train)
acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)

models = pd.DataFrame({
   'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression',
             'Random Forest', 'Naive Bayes', 'Perceptron',
             'Stochastic Gradient Decent', 'Linear SVC',
             'Decision Tree'],
   'Score': [acc_svc, acc_knn, acc_log,
             acc_random_forest, acc_gaussian, acc_perceptron,
             acc_sgd, acc_linear_svc, acc_decision_tree]})
models.sort_values(by='Score', ascending=False)
