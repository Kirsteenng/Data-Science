# Climate Change: Earth Surface Temperature

This project is one of my practices on EDA and data visualisations. The goal of this exercise is 
* To understand and describe the change in average surface temperature of each country from 1740 to 2013.  
* To visualise the trend in change over time 
* Practice on choropleth and wordcloud tool

## Data 
The data used here is from [Kaggle](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data). I have dropped some columns and the followings are the remaining columns used for plotting the charts.
* dt: date in the format of yyyy-mm-dd
* AverageTemperature: average temperature of the country during the time in degree Celcius
* AverageTemperatureUncertainty: the 95% confidence interval around the average
* Country: name of the country which will be the key to merge with ISO.csv during EDA process

## Results and charts
Firstly, the average global temperature has risen 280% from around 5dC in 1740 to 20dC in 2013. The greatest increment occurs around 1830 which is speculated to be caused by Industrial Revolution. 
![graph1](https://github.com/Kirsteenng/Data-Science/blob/master/Climate%20Change/trendline.png)

Secondly, I have decided to observe the change in average temperature for each country from 1930 to 2013 by using a time slider on choropleth graph. I found out that all the countries only have data from 1930 onwards, hence I only studied the change in that 100 years.
![graph2](https://github.com/Kirsteenng/Data-Science/blob/master/Climate%20Change/ClimateChange.png)

Lastly, for fun I have plotted a wordcloud based on the aggregated average temperature to see if that can help us understand which country has higher temperature. The result is very intuitive; the countries dominating the wordcloud are mostly from Africa which are tropical countries that are surrounded by deserts.
![graph3](https://github.com/Kirsteenng/Data-Science/blob/master/Climate%20Change/WordCloud.png)


## Improvements
* Calculate the change in gradient to identify the change in temperature increment
* Scrape a more complete dataset, data on some countries, such as Vietname, is missing from the datasource.
