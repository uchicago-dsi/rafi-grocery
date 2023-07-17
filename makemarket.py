import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point
import seaborn as sns
import fiona
import math #Hi testing
import plotly.express as px
from thefuzz import fuzz
from thefuzz import process
import random
from sklearn.linear_model import LassoCV
import statsmodels.api as sm

def filter_supermarkets(df):
    """
    Applies the found walmarts and costcos and accepted NAICS codes to the larger dataset to ensure all relevant store types are present
    """
    supermarkets = df.loc[(df["PRIMARY NAICS CODE"].isin(find_naics(df))) | (df["COMPANY"].isin(find_walmarts(df))) |(df["COMPANY"].isin(find_costcos(df)))]
    return supermarkets

def find_naics(df):
    """
    Finds the relevant NAICS codes for grocery stores
    """
    naics_codes = df.loc[df.loc[:, ["PRIMARY NAICS CODE"]].astype(str).apply(lambda x: x.str.startswith('44511')).any(axis=1)]
    return naics_codes["PRIMARY NAICS CODE"].unique()
    
                         
def find_walmarts(df):
    """
    String matches Walmart owned companies within the larger dataset and locates the dataset's specific name for Walmart owned companies
    These values will be used to make sure walmart's are found within the data
    """
    known_companies = ['WALMART',"SAM'S CLUB"]
    companies = df["COMPANY"]
    companies

    x = companies.str.contains('walmart',case=False)
    x.loc[lambda x: x ==True].index

    companies[9]

    walmart_companies = []
    for item in known_companies: 
        
        stcon = companies. str. contains (item, case=False) #check if item is contained in companies (item represents each company owned)

        index_match = stcon. loc [lambda x: x == True]. index #takes the location of the string matches if close

        for result in index_match: #now that we know the matches, add the simiar ones into the array
            
            if companies[result] not in walmart_companies:
                walmart_companies. append (companies [result]) #adds into the array
    
    return walmart_companies

def find_costcos(df):
    """
    String matches Costco owned companies within the larger dataset and locates the dataset's specific name for Costco owned companies
    These values will be used to make sure Costco's are found within the data
    """
    known_companies = ['COSTCO',"COSTCO DELI"]
    companies = df["COMPANY"]
    companies

    x = companies.str.contains('costco',case=False)
    x.loc[lambda x: x ==True].index

    companies[9]

    costco_companies = []
    for item in known_companies: 
        
        stcon = companies. str. contains (item, case=False) #check if item is contained in companies (item represents each company owned)

        index_match = stcon. loc [lambda x: x == True]. index #takes the location of the string matches if close

        for result in index_match: #now that we know the matches, add the simiar ones into the array
            
            if companies[result] not in costco_companies:
                costco_companies. append (companies [result]) #adds into the array
    
    return costco_companies

def assign_parent_numbers(df):
    """
    Assigns parent numbers based on store type and generates unique float parent numbers for companies.
    """
    updated_df = df.copy()

    # Assign parent numbers based on store type (corporations of interest)
    for index, row in updated_df.iterrows():
        parent_num = row["PARENT NUMBER"]
        store = row["STORE TYPE"]
        if store == "WALMART":
            parent_num = 5889993.0
        elif store == "COSTCO":
            parent_num = 441311800.0
        elif store == "AHOLD DELHAIZE":
            parent_num = 238136725.0
        elif store == "KROGER":
            parent_num = 7521503.0
        elif store == "ALBERTSONS":
            parent_num = 5995907.0

        updated_df.at[index, "PARENT NUMBER"] = parent_num

    # Assign unique float parent numbers to companies not of corporations of interest
    companies = {}
    for index, row in updated_df.iterrows():
        company = row["COMPANY"]
        if row["STORE TYPE"] == "OTHER":
            if np.isnan(row["PARENT NUMBER"]):
                if company not in companies:
                    # Generate a unique float parent number if the company doesn't have one
                    parent_number = np.round(np.random.uniform(1, 9999), 2)
                    companies[company] = parent_number
                else:
                    # Reuse the existing parent number
                    parent_number = companies[company]

                updated_df.loc[index, "PARENT NUMBER"] = parent_number

    return updated_df

def sic_filter(df):
    """
    Locate the unique primary sic codes present within the supermarkets/companies owned by the parent corporations of interest
    These unique primary SIC codes will be used as the basis of how we filter the main dataset to include only relevant supermarkets/companies (ie. removing convenient stores)

    Filters the dataframe to keep only the stores with specific primary SIC codes,
    including NaN values. SIC codes are from the parent corporation's subsidiary's Primary SIC codes

    The function takes in an unfiltered dataframe as a parameter.
    The function returns a filtered dataframe.
    ***NOTE remove SIC Code 541103 since it contains the SIC code for convenient stores
    """
    parent_companies = ['WALMART', 'COSTCO', 'KROGER', 'AHOLD DELHAIZE','ALBERTSONS']
    filtered_df = df[df['STORE TYPE'].isin(parent_companies)]
    primary_sic_codes = filtered_df['PRIMARY SIC CODE']
    unique_sic_codes = primary_sic_codes.unique()
    unique_sic_codes = np.delete(unique_sic_codes,(np.where(unique_sic_codes == 541103)))
    sic_codes = unique_sic_codes
    filtered_df = df[df['PRIMARY SIC CODE'].isin(sic_codes) | df['PRIMARY SIC CODE'].isna()]

    return filtered_df

def parent_name(row):
    """
    Creates values for a new column called "STORE TYPE" based on the cleaned string match list
    The new column generalizes individual companies into their parent coporation (ie. Walmart, Krogers, etc.)
    Cleaned lists from the string matches of supermarkets/companies actually owned by the parent coprporation
    ***NOTE***There will be a margin of error from this process because stores were validated through manual checks
    ***NOTE***It was unrealistic to manually inspect every store generated this way so there will be supermarkets/companies that do not actually belong to the parent coporation
    ***NOTE***STOP AND SHOP SUPERMARKET was missing from string match so it was manually added
    """
    companies = row['COMPANY']
    parent = row["PARENT NUMBER"]
    
    #KROGERS FINAL
    kroger_clean = ["BAKER'S",
     'BAKERS', 
     'CITY MARKET',
     'DILLONS',
     'FOOD 4 LESS', 
     'FOODS CO', 
     'FRED MEYER', 
     "FRY'S FOOD",
     'GERBES SUPER MARKET',  
     'GERBES SUPER MARKETS', 
     'GERBES SUPERMARKET', 
     'HARRIS TEETER', 
     'JAYC', 
     'KING SOOPERS',
     'KROGER',
     "MARIANO'S",
     'METRO MARKET', 
     'PAY LESS SUPER MARKETS',
     "PICK'N SAVE", 
     'QFC', 
     'RALPHS', 
     'RULER FOODS', 
     "SMITH'S","KROGER PICK UP"]

    #Ahold Delhaize FINAL:
    ahold_clean = [ 'FOOD LION',
     'GIANT',
     'GIANT EAGLE',
     'GIANT FOOD',
     'HANNAFORD',
     'STOP & SHOP',
     'BFRESH MARKET',
     'EASTSIDE MARKETPLACE','STOP & SHOP SUPERMARKET']

    #WALMART FINAL:
    walmart_clean = ['WALMART GROCERY PICKUP',
     'WALMART GROCERY PKUP-DELIVERY', 
     "SAM'S CLUB DELI"]

    #COSTCO FINAL:
    costco_clean = ["COSTCO DELI"]

    #ALBERTSONS FINAL:
    albertsons_clean = ['ACME MARKETS',
    'ALBERTSONS',
    'ALBERTSONS MARKET',
    'AMIGOS UNITED',
    "ANDRONICO'S COMMUNITY MARKETS",
    'CARRS/SAFEWAY',
    'CARRS SAFEWAY',
    'HAGGEN',
    'HAGGEN FOOD & PHARMACY',
    'HAGGEN FOOD',
    'JEWEL-OSCO',
    'KINGS FOOD MARKETS',
    'KINGS FOOD MARKET',
    'MARKET STREET',
    "PAK 'N SAVE",
    'PAVILIONS',
    'RANDALLS',
    'SAFEWAY',
    'STAR MARKET',
    'TOM THUMB',
    'UNITED SUPERMARKETS',
    'VONS',
    'SUPER SAVER',
    'CARRS QUALITY CTR PALMER SHPG',"CARRS QUALITY CTR PALMER SHPG",
     "SAAR'S SUPER SAVER FOODS"]


    if companies in walmart_clean or parent == 5889993.0:
        return 'WALMART'
    if companies in costco_clean or parent == 441311800.0:
        return 'COSTCO'
    if companies in ahold_clean or parent == 238136725.0:
        return 'AHOLD DELHAIZE'
    if companies in kroger_clean or parent == 7521503.0:
        return 'KROGER'
    if companies in albertsons_clean or parent == 5995907.0:
        return 'ALBERTSONS'

    return 'OTHER'

def store_category(df):
    """
    Assigns a store category label in the STORE TYPE column. There are four different subsets: Other (Not assigned a parent number); Other (Assigned a parent number); Independent (Not assigned a parent number); Independent (Assigned a parent number). ***NOTE*** The group decided the arbitrary value of 3 stores to be the max number of stores an independent retailer is likely to own; Parent number assignment was determined if the parent number was less than 9999.
    """
    non_parent_num = df[df["PARENT NUMBER"] < 9999]
    non_parent_num_group = non_parent_num.groupby("PARENT NUMBER")[["COMPANY"]].count().reset_index()

    parent_num = df[df["PARENT NUMBER"] >= 9999]
    parent_num_group = parent_num.groupby("PARENT NUMBER")[["COMPANY"]].count().reset_index()

    for idx in df.index:
        row = df.loc[idx]

        if row["STORE TYPE"] == "OTHER":
            np_count = non_parent_num_group.loc[non_parent_num_group["PARENT NUMBER"] == row["PARENT NUMBER"], "COMPANY"].values
            p_count = parent_num_group.loc[parent_num_group["PARENT NUMBER"] == row["PARENT NUMBER"], "COMPANY"].values

            if np_count < 4:
                df.loc[idx, "STORE TYPE"] = "INDEPENDENT (NP)"
            elif np_count >= 4:
                df.loc[idx, "STORE TYPE"] = "OTHER (NP)"
            elif p_count < 4:
                df.loc[idx, "STORE TYPE"] = "INDEPENDENT (P)"
            elif p_count >= 4:
                df.loc[idx, "STORE TYPE"] = "OTHER (P)"


def assign_median(df,variable,level):
    """
    Generates the median sales volume per location value for each subset (ie. Kroger; Other Non-Parent; Independent Parent; etc.) at a given location level (ie. state or county)
    """
    median = df.loc[:, ['STORE TYPE', level, variable]].groupby(['STORE TYPE', level]).median().reset_index().rename(columns={variable: 'MEDIAN'})
    mergedf = pd.merge(df, median, how="left",on=[level,"STORE TYPE"])
    mergedf[variable] = np.where(mergedf[variable].isna(), mergedf['MEDIAN'], mergedf[variable])
    return mergedf.drop(columns=["MEDIAN"])

def supermarket_generator(file_path, naics_filter, change_na_to_median):
    """
    Accepts a file path of company data within the continental US for a given year and returns a cleaned dataframe of supermarkets within the US for the given year
    """
    stores_general = pd.read_csv(file_path)
    stores_general.drop(['Unnamed: 0'],inplace=True,axis=1)
    territories = ['PR', 'FM', 'MP', 'GU', 'VI', 'MH','AK','HI']
    stores_general = stores_general.drop(stores_general[stores_general['STATE'].isin(territories)].index)

    stores_general['STORE TYPE'] = stores_general.apply(parent_name, axis=1)
    
    if naics_filter:
        supermarkets = filter_supermarkets(stores_general)
    else:
        supermarkets = sic_filter(stores_general)
    
    supermarkets = assign_parent_numbers(supermarkets)
    
    store_category(supermarkets)
    
    if change_na_to_median:
        supermarkets = assign_median(supermarkets,"SALES VOLUME (9) - LOCATION","FIPS CODE")
        supermarkets = assign_median(supermarkets,"SALES VOLUME (9) - LOCATION","STATE")

        supermarkets = assign_median(supermarkets,"EMPLOYEE SIZE (5) - LOCATION","FIPS CODE")
        supermarkets = assign_median(supermarkets,"EMPLOYEE SIZE (5) - LOCATION","STATE")

    return supermarkets


