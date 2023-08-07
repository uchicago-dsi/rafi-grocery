## Data Cleaning and Analysis
# Introduction
This project focuses on data cleaning, string matching, and business analysis of stores owned by target corporations in the Continental United States. The goal is to filter and process the data to identify relevant stores and perform market analysis.

# Data Cleaning
The data cleaning process involved the following steps:

Filtering Stores: The represented stores were filtered to include only those from the Continental United States since the majority of the target companies operate in this region.

String Matching: A string matching technique using thefuzz library was applied to compare all stores to the parent corporations' owned stores. A threshold of 77 was used to minimize store losses during the matching process. This generated a list of potential unique string matches.

Cleaning String Matches: The lists generated from the string matches were cleaned by removing supermarkets/companies that did not actually belong to the parent corporation. Manual checks were performed to validate the stores, but there may be a margin of error due to the large number of stores.

Filtering by SIC Code: To further refine the dataset, common SIC codes were identified among the filtered companies. These common SIC codes were used to filter the broader dataset, including only relevant store types such as grocers retail.

Parent Number Assignment: The dataframe was processed to assign parent numbers for companies. If the original parent number was NaN, a random parent number from 0-9999 was generated. If the same company appeared with a NaN parent number, it was assigned the same parent number as its counterpart. However, this approach does not account for cases where different corporations have companies with the same name, leading to grouping of unrelated organizations with the same parent number. This anomaly is infrequent and considered acceptable.

Store Type Assignment: Companies were assigned to different store types based on their characteristics. If a company was not of interest (i.e., not a target corporation) and the count of companies with the same parent number was greater than 4, it was classified as "Other." If the count was less than 4, it was classified as "Independent." The threshold of 4 was agreed upon by the group as the criteria for independent retailers.

Sales Volume Missing Values: Initially, a lasso regularized regression was run with an R^2 of 0.86 to predict the sales volume. However, explanatory variables required for the regression were NaN whenever the sales volume was NaN. To handle this, companies were divided into four subsets: "Other" (non-initial parent number, independent), "Independent" (no initial parent number, independent), "Other" (initial parent number), and "Independent" (initial parent number). NaN values were then filled for each respective subset using the median of the Sales Volume (9) - LOCATION column within a boundary of FIPS CODE. FIPS CODE was chosen to account for regional variations in median sales volume.

# Business Analysis
The following business analysis functionalities were developed:

Market Share Calculation: Functions were developed to calculate market share at both the county and state levels.

HHI (Herfindahl-Hirschman Index) Calculation: Functions were created to calculate the HHI index, which measures market concentration. The HHI index can be calculated at the county level or scaled up to the state level.

Chloropleth Map Visualization: A chloropleth map of the entire United States was generated to visualize HHI categories at the state level.

County-level HHI Calculation: A table was created to calculate the HHI index for each county in the United States.

Limitations
The string matching process is subject to manual validation errors, resulting in potential inaccuracies.
Companies with the same name but different parent corporations are grouped together, leading to anomalies in parent number assignments.
Sales volume missing values were filled using median values within a FIPS CODE boundary, assuming regional similarities.
The HHI index calculation relies on assumptions and may not capture all market dynamics accurately.
Please note that this README file provides an overview of the project's steps and functionalities. For detailed implementation and code explanations, please refer to the project's documentation or source code.