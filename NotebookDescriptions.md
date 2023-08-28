# Data Exploration Week 1

This notebook includes all the Data exploration work done in Week 1 with a focus on:

Cleaning, further filtering and grouping the 2022 business data to just look at the grocery stores.
Some preliminary answers to Research Question 1 ( Looking at parent companies within the data set and companies they own ) and 3 ( calculating HHI for market concentraion of the grocery industry )and notes the findings and interesting things found within the dataset as it relates to grouping by SIC codes and looking at parent numbers and companies in the dataset.
It also goes into observing nationwide data to filter independent stores under the assumption that they NAN values for parent number were independent stores and checks the top 50 stores by employee size and see if their name has any of the popular stores (like Krogers, Walmart etc). It also experiments with Thefuzz and its process function to find out string matches within all independent stores's name and try to match only the top 10 parent names.

## Limitations:

Data may have been filtered incorrectly. Eg. Costco only has 29 stores within the dataset.

# Data Exploration Week 2

This notebook contains further Data exploration with a focus on :

Choosing which SIC/NAICS code we would use to filter out the data and experimenting on grouping grocery stores excluding convenience stores using NAICS codes.
String matching the companies to their Parent companies (Big 4) and then utilize this process to create the filtered grocery dataframe.
It also goes into some initial mapping to begin answering research question 2 (corporate concentration found today within the United States grocery industry) and has a density map showing sales volume of the parent companies across the US as well as a the location of all parent companies across the US as well.

## Limitations:

Grouping by NAICS codes does not account for all Walmarts with many of their store counts missing and the string matching contains some inaccuracies that can maybe be fixed by implementing .contains in the code.

# Data Exploration Week 3

This notebook reads in 4 years of filtered data ( 2018, 2019, 2020, 2022 ) using the String matching method to do a store count for each of the years to see what is in each of the datasets. It also explores an initial scatter mapbox plot for these 4 years to do some expirementation with the time series of just those 4 years for the major grocery stores.

## Limitations:

As of now, the data is still filtered incorrectly from infogroup as the numbers for the parent companies still have some skewness in terms of lower numbers that don't match the true allocation across the US.
