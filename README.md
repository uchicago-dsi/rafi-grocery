# RAFI-USA

## Organization
Since its founding in 1990, nonprofit RAFI-USA (Rural Advancement Foundation International) has worked to advocate for rural communities and fight inequities in the food system through policy research and on-the-ground services. This summer project is in partnership with RAFI’s “Challenging Corporate Power” initiative, which seeks to reduce corporate concentration in agriculture.  Our main point of contact will be Todd Nief, a data scientist at the DSI.

## Problem Statement
Over the past three decades, the number of grocery retail stores has shrunk by more than one-third, and in 2021, just four companies (WalMart, Costco, Kroger, and Ahold Delhaize) controlled 65 percent of the market. This consolidation has resulted in higher food prices and fewer choices for consumers. This is also squeezing farmers, who are increasingly forced to sell their produce to large food distributors that use exclusive deals and predatory pricing, rather than directly to local grocers.

Last October, the grocery chains Kroger and Albertsons announced plans to merge, which would give them a 19 percent market share. RAFI hopes to join its partners in petitioning the Federal Trade Commission (FTC) to oppose the merger. To aid their efforts, we will help RAFI map the locations of all grocery stores in the U.S. over time, quantify the extent to which consumer choice has decreased for different geographic regions and demographic groups, and analyze how the merger would impact consumer choice if executed.

## Research Questions
- For the initial exploratory data analysis, how many parent companies exist in the dataset? How many grocery chains do they own, and how do these numbers change per year?
- To what extent is corporate concentration found today within the United States grocery industry? How does this vary by state or geographic region? How has the monopoly power of groceries’ parent companies changed over time?
- What are the demographics of the communities most affected by concentrated corporate power (e.g., racial, socioeconomic, etc.)? Is there a statistically significant relationship (or strong correlation) between these demographic variables and the number of grocery stores available within a given number of miles, driving distance, or driving time?
- How would the upcoming merger between Kroger and Albertsons affect the concentration of corporate power in the grocery industry if approved?

## Project Deliverables
- A Jupyter notebook showing time series consolidation in the grocery industry based upon the parent company for individual stores, including for the proposed merger.
- A Jupyter notebook that produces a map dividing an area of interest into regions according to how many grocery stores the population has access to.
- A Jupyter notebook that produces an analysis of the relation between demographic measures and the number of grocery store options.

## Data Description
The following datasets will be used for the project:
- InfoGroup Historical Business Data. Annual snapshots and locations of businesses in the United States from 1997 through the present. Available through the University of Chicago Library as a zip file. Each year is a CSV file of several gigabytes.
- U.S. Census Data. Counts of households, individuals, and individuals of different races at the census block or census block group level. Provided as CSV files, while block and block group boundaries are provided as GeoJSON files.

## Additional Reading
- [RAFI-USA Calls on the FTC to Oppose Mega Grocery Chain Merger](https://www.rafiusa.org/blog/rafi-usa-opposse-mega-grocery-chain-merger/)
- [Farm, Consumer, & Antimonopoly Groups All Urge the FTC to Oppose Kroger-Albertsons Merger](https://www.openmarketsinstitute.org/publications/farm-consumer-antimonopoly-groups-all-urge-the-ftc-to-oppose-kroger-albertsons-merger)
- [Revealed: The True Extent of America’s Food Monopolies, and Who Pays the Price](https://www.theguardian.com/environment/ng-interactive/2021/jul/14/food-monopoly-meals-profits-data-investigation)
Amir 