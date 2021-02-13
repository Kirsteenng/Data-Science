# Data Science Portfolio
This repository contains practice projects that describe my learning process from data exploration, visualisation to building prediction models.

## Projects
[Climate Change: Earth Surface Temperature ](https://github.com/Kirsteenng/Data-Science/tree/master/Climate%20Change)

* The data is downloaded from [Kaggle](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data/notebooks).
* Constructed a complete list of ISO-3 country list.
* Investigated time periods of rapid increase in earth surface temperature.
* Constructed time series choropleth to present the change in earth surface temperature over time. 
* Findings: 
  * Temperature has been rising since 1750 and rises most rapidly around 1822 to 1880s. This rise can be associated with the beginning of the industrial revolution in Europe which     is around the 1800s.
  * Fast rising developing countries such as the UK,USA and China have experienced greatest increase of surface temperature, which is +5-6 degrees, over past 100 years. These         countries share the same history of being an industrial/agricultural focused economy before transforming into service based.
* Keywords: EDA, Choropleth, Wordcloud

![graph](https://github.com/Kirsteenng/Data-Science/blob/master/Climate%20Change/ClimateChange.png)


[Housing Prices in Hong Kong ](https://github.com/Kirsteenng/Data-Science/tree/master/Hong%20Kong%20House%20Price)

* The data is crawled from Centaline which uses transaction data which publishes transaction data from Hong Kong Housing Authorities .
* Analysed and investigated trends on number of transactions and price/sqft
* Findings: 
  * From July to December 2020, September has the most transaction. Shaukeiwan was the area with most transaction with 626 units.
  * Sheung Wan, Mid Levels West,Mid Level North Point and Happy Valley are the areas with highest retention value ie buildings after 30years old have the least fluctuation.
  * Sheung Wan has a positive correlation with other 9 areas.
  * Using Random Forest Regressor, we can build a prediction model of 75% accuracy using Area Code and Building Age as independent variables.
* Keywords: EDA, Random Forrest Regressor

![graph](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/graphs/Change%20in%20price%20over%206%20months.png)

