import pandas as pd
import numpy as np
import plotly.express as px

def calculate_market_share(df):
    """
    Calculate market share based on the input dataframe.
    Total Market Volume is calculated by the summation of each company's total sales volume by location and grouped under parent number.
    Include the corresponding STORE TYPE from the supermarkets dataframe.
    """

    market_share = df.groupby('PARENT NUMBER')[["SALES VOLUME (9) - LOCATION", 'STORE TYPE']].agg({"SALES VOLUME (9) - LOCATION":'sum',
                                                                                         'STORE TYPE': 'first'}).reset_index().rename(columns={"SALES VOLUME (9) - LOCATION": "TOTAL SALES"})
    market_share["PERCENT"] = (market_share["TOTAL SALES"] / market_share["TOTAL SALES"].sum()) * 100

    market_share_sorted = market_share.sort_values(by=["PERCENT"], ascending=False)

    return market_share_sorted

def hhi(num):
    """
    Calculates the HHI of the market 
    """
    return np.square(num).sum() 

def categorize_market_concentration(hhi_value):
    """
    Categorizations are based on the Antitrust Division of the US DOJ
    """
    if hhi_value > 2500:
        return 'HIGHLY CONCENTRATED'
    elif hhi_value > 1500:
        return 'MODERATELY CONCENTRATED'
    else:
        return 'NOT CONCENTRATED'

def calculate_state_hhi(df):
    """
    Calculates the HHI of every state within the nation; takes on the specific year dataframe as a parameter
    """
    states = df["STATE"].unique().tolist()
    hhi_values = []
    for state in states:
        df_state = df.loc[df["STATE"] == state]
        market_share_state = calculate_market_share(df_state)
        hhi_value = hhi(market_share_state["PERCENT"])
        market_concentration = categorize_market_concentration(hhi_value)
        hhi_values.append((state, hhi_value, market_concentration))
    hhi_df = pd.DataFrame(hhi_values, columns=["STATE", "HHI", "MARKET CONCENTRATION"])
    return hhi_df

def calculate_county_hhi(df):
  """
  Calculate the HHI of every county within the nation; takes on the specific year dataframe as a parameter
  """

  states = df["STATE"].unique()
  
  state_hhi_df = pd.DataFrame(columns=["STATE", "COUNTY CODE", "HHI", "MARKET CONCENTRATION"])

  for state in states:
  
    df_state = df.loc[df["STATE"] == state]
  
    state_counties = df_state["COUNTY CODE"].unique().tolist()

    for county in state_counties:
    
      df_county = df_state.loc[df_state["COUNTY CODE"] == county]
      
      market_share_county = calculate_market_share(df_county)

      hhi_value_county = hhi(market_share_county["PERCENT"])

      market_concentration_county = categorize_market_concentration(hhi_value_county)

      new_row = pd.DataFrame({"STATE": state, 
                              "COUNTY CODE": county,
                              "HHI": hhi_value_county,
                              "MARKET CONCENTRATION": market_concentration_county}, index=[0])
                              
      state_hhi_df = pd.concat([state_hhi_df, new_row])

  return state_hhi_df

def calculate_hhi_USA(df):
    """
    Calculates the Average HHI at the National 
    """
    market_share_total = calculate_market_share(df)
    hhi_value = hhi(market_share_total["PERCENT"])
    return hhi_value

def avg_state_hhi(df):
    """
    Calculates the Average HHI at the State Level
    """
    state_hhi = calculate_state_hhi(df)
    return state_hhi["HHI"].mean()

def avg_county_hhi(df):
    """
    Calculates the average HHI at the county level
    """
    county_hhi = calculate_county_hhi(df)
    return county_hhi["HHI"].mean()

def calculate_concentration_ratio(df, num_firms_list=[4, 10, 20]):
    """
    Calculate concentration ratio for different number of firms based on the input dataframe.
    The dataframe should contain columns: PARENT NUMBER, TOTAL SALES, STORE TYPE, and PERCENT.
    """
    market_share = calculate_market_share(df) 
    sorted_df = market_share.sort_values('TOTAL SALES', ascending=False)
    
    concentration_ratios = []
    
    for num_firms in num_firms_list:
        selected_firms = sorted_df.head(num_firms)
        total_market_share = selected_firms['PERCENT'].sum()
        concentration_ratios.append(total_market_share)
    concentration_ratios.insert(0,df['ARCHIVE VERSION YEAR'].unique()[0])
    return concentration_ratios

def avg_hhi(df_list):
    """
    Generates a dataframe of the average hhi value for each corresponding level; takes on the list of dataframes as a parameter
    """
    data = {}
    for df in df_list:

        year = df['ARCHIVE VERSION YEAR'].unique()[0]

        state_hhi = avg_state_hhi(df)
        county_hhi = avg_county_hhi(df)
        country_hhi = calculate_hhi_USA(df)
        data[year] = {'Nationwide HHI':country_hhi,'State HHI': state_hhi, 'County HHI': county_hhi}

    df = pd.DataFrame(data).reset_index()
    df = df.T.reset_index()
    df.columns = df.iloc[0]
    df = df.tail(-1)
    df = df.rename(columns={"index":"Year"})
    df["Year"] = df["Year"].astype(int)
    df.sort_values(by="Year",ascending=False,inplace=True)
    return df

def yearly_cr(df_list):
    """ 
    Generates a dataframe of Concentration Ratios across different years
    """
    result_dataframes = []

    for df in df_list:
        concentration_ratios = calculate_concentration_ratio(df)
        df_dict = {
            'Year': [concentration_ratios[0]],
            'CR4': [concentration_ratios[1]],
            'CR10': [concentration_ratios[2]],
            'CR20': [concentration_ratios[3]]
        }
        df_result = pd.DataFrame(df_dict)    
        result_dataframes.append(df_result)

    final_dataframe = pd.concat(result_dataframes, ignore_index=True)
    final_dataframe["Year"] = final_dataframe["Year"].astype(int)
    final_dataframe.sort_values(by="Year",ascending=False,inplace=True)
    return final_dataframe

def calculate_hhi_USA(df):
    """
    Calculates the Nationwide HHI Level
    """
    market_share_total = calculate_market_share(df)
    hhi_value = hhi(market_share_total["PERCENT"])
    return hhi_value

def avg_hhi_plot(df_list):   
    """
    Plot the average hhi across different years; takes on the list of supermarket dataframes as a parameter
    """    
    df = avg_hhi(df_list)
    fig = px.line(df, x='Year', y=df.columns[1:], title='Average HHI', 
                  labels={'variable': ' ', 'value': 'HHI Value'}, range_y=(0, 5000))
    fig.update_layout(yaxis=dict(
        tickvals=list(range(0, 5001, 500)),  
        dtick=500  
    ))
    fig.update_layout(xaxis=dict(
        tickvals=list(range(df["Year"].min(), df["Year"].max()+1, 1)),  
        dtick=1 
    ))
    fig.update_layout(
        plot_bgcolor='white',  \
        xaxis=dict(linecolor='black'), 
        yaxis=dict(linecolor='black'), 
        showlegend=True,  # Show legend
        legend=dict(orientation='h', x=0.3, y=-0.3), 
        margin=dict(b=100) 
    )
    fig.update_layout(title_font=dict(size=24))
    fig.update_layout(xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
                      yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'))

    return fig.show()

def plot_concentration_ratios(df_list):
    """
    Plot the concentration ratio across different years; takes on the list of supermarket dataframes as a parameter
    """
    df = yearly_cr(df_list)
    fig = px.line(df, x='Year', y=df.columns[1:], title=f'National {df.columns[1]}, {df.columns[2]}, and {df.columns[3]} ratios for food sales',
                  labels={'variable': ' ', 'value': 'Percent Sales'}, range_y=(0, 100))

    fig.update_layout(yaxis=dict(
        tickvals=list(range(0, 101, 10)),  
        dtick=10 
    ))

    fig.update_layout(xaxis=dict(
        tickvals=list(range(df["Year"].min(), df["Year"].max()+1, 1)), 
        dtick=1
    ))

    fig.update_layout(
        plot_bgcolor='white',
        xaxis=dict(linecolor='black'),
        yaxis=dict(linecolor='black'),
        showlegend=True, 
        legend=dict(orientation='h', x=0.5, y=-0.2), 
        margin=dict(b=100) 
    )

    fig.update_layout(title_font=dict(size=24))

    fig.update_layout(xaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
                      yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'))

    return fig.show()

def county_hhi_ts(df_list, state, county):
    """
    Returns a time series dataframe of the HHI values for a specific county
    """
    result_dataframes = []

    for df in df_list:
        hhi = calculate_county_hhi(df) 

        df_dict = {
            'Year': df['ARCHIVE VERSION YEAR'].unique()[0],
            'State': state,
            'County': county,
            'HHI': hhi.loc[(hhi["COUNTY CODE"] == county) & (hhi["STATE"] == state), "HHI"].unique()[0],
            'Market Concentration': hhi.loc[(hhi["COUNTY CODE"] == county) & (hhi["STATE"] == state), "MARKET CONCENTRATION"].unique()[0]
        }

        df_result = pd.DataFrame(df_dict, index=[0])
        result_dataframes.append(df_result)

    final_dataframe = pd.concat(result_dataframes, ignore_index=True)
    final_dataframe["Year"] = final_dataframe["Year"].astype(int)
    final_dataframe.sort_values(by="Year", ascending=False, inplace=True)
    return final_dataframe

def state_hhi_ts(df_list):
    """
    Return a time series dataframe of state level hhi
    """
    result_dataframes = []

    for df in df_list:
        hhi = g.calculate_state_hhi(df) 
        hhi["Year"] = df['ARCHIVE VERSION YEAR'].unique()[0]
        result_dataframes.append(hhi)

    final_dataframe = pd.concat(result_dataframes, ignore_index=True)
    final_dataframe["Year"] = final_dataframe["Year"].astype(int)
    final_dataframe.sort_values(by="Year", ascending=False, inplace=True)
    return final_dataframe
