
# Hong Kong Housing Price: Analysis on housing price movement

Hong Kong is one of the most expensive cities in the world to own a house. An average price per squarefoot on Hong Kong island is $18,565 . The goals of this project are 
- Collect data from [Centaline] (https://hk.centanet.com/findproperty/en/list/transaction?q=mptTD0GZW0mpDQyHGtyob)
- What is the housing transaction trend in Hong Kong Island across this period of time?
- Which area(s) is/are the most popular?
- Average price/sqft analysis.
- Which area and what building age have the highest potential to retain value?

## Data 
The data used here is from Centaline 
I have built a crawler to collect the data from all region in Hong Kong Island from March 4th to Aug 2nd. The crawler file is located [here](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/data/crawler.py). The crawler is built using selenium for dynamic webpage.

Hong Kong consists of 4 parts: Hong Kong Island, Kowloon, New Territory and Lantau Island.  For this project I will focus on property transactions on Hong Kong Island. The cleaned .csv is located [here](https://github.com/Kirsteenng/Data-Science/blob/master/Hong%20Kong%20House%20Price/data/cleaned_total_named_extract.csv).The followings are the columns of the dataset 


* Date: Date of transaction in yyyy-mm-dd (ranging date based on the time of crawler being run)
* Area: Location of the transacted unit
* Name: Name of the transacted building unit in string format
* Years: Age of the building the unit transacted in years
* Price(mm): Sale price of unit in terms of HKD in millions
* Size(sqft): Size of the unit in squarefeet
* Price/sqft: Transaction price/Saleable Area, a metric to standardize the comparison of prices between different areas.

