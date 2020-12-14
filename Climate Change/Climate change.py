# -*- coding: utf-8 -*-

#Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import plotly as pl
import plotly.graph_objects as go
pl.io.renderers.default = 'browser'

## Import data
country = pd.read_csv('./data/GlobalLandTemperaturesByCountry.csv')
city = pd.read_csv('./data/GlobalLandTemperaturesByCity.csv')
country_code = pd.DataFrame(pd.read_csv('./data/ISO.csv'))


## This code is used to update the missing countries and their ISO in my csv file
# missing = ['Bolivia', 'Venezuela', 'United Kingdom', "Côte d'Ivoire", 'Tanzania', 'Czechia', 'Syria', 'Congo', 'Iran','Myanmar']
# iso = ['BOL','VEN','GBR','CIV','TAN','CZE','SYR','COD','IRN','MMR']
# add_on = pd.Series(dict(zip(iso,missing))).reset_index()
# add_on.columns=['ISO','CountryName']
# country_code.append(add_on)

## Inspect data
country.info()
country.head(5)
country.describe()
col = country.columns

## Check for null values and remove
country_temp = country[~country.AverageTemperature.isna()]
country_count = country.groupby(['Country'])

## Reorganize data into better format
country_temp['dt']=pd.to_datetime(country_temp.dt).dt.strftime('%d/%m/%Y')
country_temp['year'] = country_temp['dt'].apply(lambda x: x[6::])
wc = country_temp.groupby(['Country'])['AverageTemperature'].mean().reset_index()
 
## Task1: build wordcloud based on average temperature for top 100 countries
def wordcloud():
    wc_100 = wc.sort_values('AverageTemperature',ascending= False).head(100)
    wc_dict = dict(zip(wc['Country'],wc['AverageTemperature']))
    wc_100_dict = dict(zip(wc_100['Country'],wc_100['AverageTemperature']))

    wc_code = pd.merge(wc,country_code,left_on = 'Country',right_on = 'CountryName')

    ## WordCloud().generate_from_frequencies() requires a dict
    WordC = WordCloud().generate_from_frequencies(wc_dict)
    WordC2= WordCloud().generate_from_frequencies(wc_100_dict)

    plt.figure(figsize = (10,5))
    #plt.imshow(WordC)
    plt.imshow(WordC2)
    plt.show()


## Task2: build choropleth on average temperature
def choro():
    wc_code = pd.merge(wc,country_code,left_on = 'Country',right_on = 'CountryName')

    overall_average = dict(type='choropleth',
                       locations = wc_code['ISO'].astype(str),
                       z = wc_code['AverageTemperature'],
                       locationmode ='ISO-3',
                       text = wc_code['Country'],
                       colorscale = 'Blues',
                       colorbar_title = "Degree Celcius")

    overall_layout = dict(geo = dict(scope = 'world'))

    fig = dict(data = overall_average, 
           layout = overall_layout)

    pl.offline.iplot(fig)

    
""" ## Another way of plotting choropleth
    fig = pl.express.choropleth(wc_code,
                            locations = 'ISO',
                            color = 'AverageTemperature',
                            hover_name = 'Country')
    fig.show()
"""
# Task3: build time slider that shows average temperature rise and fall with year for each country
def slider():
    # Found out that not all country's starting year is the same. Hence select date from 1903 to 2013(which is max)
    wc_year = country_temp[country_temp['year'] >= '1903' ].reset_index()
    wc_year.year.nunique()
    wc_year =wc_year.groupby(['year','Country'])['AverageTemperature'].mean().reset_index()
    wc_year = pd.merge(wc_year,country_code,left_on = 'Country',right_on = 'CountryName')


    # Populating data 
    data = []
    for year in wc_year.year.unique():
        data_selected = wc_year[wc_year['year']==year]
        data_one_yr = dict(
                 type='choropleth',
                 locations = data_selected['ISO'].astype(str),
                 z= data_selected['AverageTemperature'].astype(float),
                 locationmode='ISO-3',
                 text = data_selected['Country'],
                 colorscale = 'Blues',
                 colorbar_title = "Degree Celcius")
    
        data.append(data_one_yr)


    # Creating steps for slider ie the individual gap on the slider
    steps = []
    for i in range(len(data)):
        step = dict(method = 'restyle',
                    args = ['visible',[False]* len(data)], 
                    label = 'Year {}'.format(i + 1903 ))
        step['args'][1][i] = True
        steps.append(step)
    
    
    sliders = [dict(active =0,
                    pad ={"t":1},
                    steps = steps)]
    layout = dict(geo = dict(scope = 'world'),
                  sliders = sliders)
    
    fig = dict(data = data, 
               layout = layout
               )

    pl.offline.iplot(fig)


# Task4: investigate the most incremented countries and period. Examine those period.
def linechart():
    gb_year = country_temp.groupby(['year'])['AverageTemperature'].mean().reset_index()
    data = [go.Scatter(
            x = gb_year['year'],
            y = gb_year['AverageTemperature'],
            name='Average Temperature',
            line=dict(color='rgb(199, 121, 093)'))]
    
    layout = go.Layout(
        xaxis=dict(title='year'),
        yaxis=dict(title='Average Temperature, °C'),
        title='Average land temperature in world',
        showlegend = False)

    fig = dict(data=data, layout=layout)
    pl.offline.iplot(fig)
    

if __name__ == 'main':
    wordcloud()
    slider()
    choro()
    