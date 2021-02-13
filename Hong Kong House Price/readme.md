
# Hong Kong Housing Price: Analysis on housing price movement

Hong Kong is one of the most expensive cities in the world to own a house. An average price per squarefoot on Hong Kong island is . The goals of this project are 
* To collect housing transaction data from [Centaline](http://www1.centadata.com/ephome.aspx), Hong Kong's largest real estate agent site. 
* To visualise the trend in change over 6 months.
* To identify related features that would affect housing prices.

## Data 
The data used here is from [Centaline](http://www1.centadata.com/ephome.aspx). 
I have built a crawler to collect the data from all region in Hong Kong Island for the past 6months. The crawler file is located here
Hong Kong consists of 4 parts: Hong Kong Island, Kowloon, New Territory and Lantau Island.  For this project I will focus on property transactions on Hong Kong Island.

* Address: Address of the transacted unit in string format
* Transaction Date: Date of transaction in yyyy-mm-dd (ranging date based on the time of crawler being run)
* B. Age: Age of the building the unit transacted in years
* Transaction price: Sale price of unit in terms of HKD in millions
* Saleable Area: Size of the unit in squarefeet
* Building Name: Name of the building the transacted unit is located at
* Area: Location of the transacted unit
* Price(000)/sqft: Transaction price/Saleable Area, a metric to standardize the comparison of prices between different areas.

## Results and charts
The transaction period ranges from July 16 2020 to January 8 2021. In this 6 months, September is the most active month with 544 transactions, whereas January has the lowest due to the lack of data collected in the short timeframe. 
The number of transaction in January is the least because the data only covers first 8 days of the month. This is one of the limitations of this study and more data will be collected in April to verify this trend.
The mean number of transaction across 10 locations is 294. The area that has the most transaction is Shaukeiwan(626), followed by Northpoint(512) and Kennedy Town/SYP(497). 
According to the chart below the number of transaction has been steadily increasing from July to September but plateued in October to December. ![graph](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/graphs/Change%20in%20price%20over%206%20months.png)

On the other hand, the price per squarefoot shows a cyclical trend. If the price/sqft has gone up too high, it will experience a correction and falls back down. Hence showing a cyclical pattern. Price per squarefoot implies the true supply and demand during that period. Therefore this metric will be used as the true indicator of market demand instead of number of transaction.

One question we want to study is which area has the highest retention value. We define area that has high retention value when the price per sqft for buildings beyond 30yo does 
not drop significantly with building age. A building beyond 30yo is considered an old building by Hong Kong standard. The mean of the building age in our data is 30.8.  
Based on the charts below, our data shows that the transactions in Sheung Wan, Mid Levels West,
Mid Level North Point and Happy Valley, have the least fluctuation with building age. 
![graph1](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/graphs/Buidling%20age%20vs%20price.png)
![graph2](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/graphs/Buidling%20age%20vs%20price2.png)

In other areas such as KennedyTown/SYP and Shaukeiwan, it can be seen that the price/sqft constantly decreases with building age. 
However these transaction prices only reflect the retention value of the areas within this period. The retention value will vary from buildings to buildings, which explains the presence of outliers in area such as Quarrybay, Northpoint, Midlevelwest and MidLevelCentral.
A more accurate study would be to look at the price change in individual buildings over time. 


We moved on to study the correlation between variables in this data set.
We plotted a correlationship between all 10 areas to study what are the relationships between area in this period. ![graph1](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/graphs/corr%20between%20areas.png) 

This helps to identify the areas that are ideal for investment if one thinks the overall housing market in Hong Kong will improve in the future. 
The chart shows that Sheung Wan area has the most positive correlations with other areas.

We then study the correlations between variables. Price/ per squarefeet has 0.49 correlationship with Saleable Area, and 0.37 with Area Code. ![corrmap](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/graphs/Correlation%20map.png)

The p-value for the two pairs of variables are significantly below 0.05 and hence can be concluded that Saleable Area and the Area Code are significant in affecting the Price/sqft.
Another strong positive correlationship pair would be Price/sqft and Transaction Price. But because Price/sqft is a function of Transaction Price and Saleable Area, we do not see the reason behind justifying the positive correlation.

Now can we predict housing prices?

Firstly we plot a pairplot against all variables to observe any patterns![pairplot](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/graphs/pairplot.png) 

The variable we are trying to predict is the Price/sqft, the independent variables are Building Age and 
Area Code. We predict using Random Forest Regression because the pairplot does not show any linearity between independent and dependent variables. After a few trial and errors, the most optimum parameters were test_size=0.05(95% of the data set is used to training) and num_estimator = 20(there are 20 decision trees). 
The R^2 score is 0.75. I am still trying to understand what is the significance of 0.75 and what are better models for this dataset.





