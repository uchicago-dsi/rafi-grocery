import itertools
import numpy as np
import pandas as pd
from geopy import distance
import math

def proximity_function(df, dist=2.5, print_store_pairs=False, print_employees=True):
    """
    Filter a DataFrame of stores based on their proximity and lowest sales.

    This function calculates the proximity between all store pairs in a DataFrame using their coordinates
    and filters out the stores that have a distance less than or equal to a specified threshold. For each
    pair of stores within the proximity threshold, it identifies the store with the lowest sales and removes
    those stores from the DataFrame.
    """
    df_copy = df.copy()

    stores = df_copy["Coordinates"].tolist()
    store_combinations = itertools.combinations(stores, 2)
    combos = list(store_combinations)

    coordinate_to_store = {coord: store for coord, store in zip(df_copy["Coordinates"], df_copy["Store"])}

    distance_list = []

    for pair in combos:
        distance_between_points = distance.distance(pair[0], pair[1]).miles
        distance_list.append(distance_between_points)

    distance_array = np.array(distance_list)
    indices_within_distance = np.where(distance_array <= dist)[0].tolist()

    pairs_within_distance = [combos[index] for index in indices_within_distance]

    if print_store_pairs:
        print("\nStores associated with each pair:")
        for i, stores_in_pair in enumerate(pairs_within_distance):
            print(f"Pair {i + 1}: {[coordinate_to_store[coord] for coord in stores_in_pair]}")
    sum_of_employee_size_removed = 0

    for pair_stores in pairs_within_distance:
        store1, store2 = [coordinate_to_store[coord] for coord in pair_stores]
        sales_store1 = df_copy.loc[df_copy['Store'] == store1]["Sales"].values
        sales_store2 = df_copy.loc[df_copy['Store'] == store2]["Sales"].values
        if len(sales_store1) > 0 and len(sales_store2) > 0:
            sales_store1 = sales_store1[0]
            sales_store2 = sales_store2[0]
            if sales_store1 < sales_store2:
                lowest_sales_store = store1
            else:
                lowest_sales_store = store2
            df_copy = df_copy[df_copy['Store'] != lowest_sales_store]

            sum_of_employee_size_removed += df.loc[df['Store'] == lowest_sales_store]["EMPLOYEE SIZE (5) - LOCATION"].sum()

    if print_employees:
        print(f"Predicted Number of Employees Displaced: {sum_of_employee_size_removed}")
    
    df_copy["STORE TYPE"] = df_copy["STORE TYPE"].replace("ALBERTSONS", "KROGER-ALBERTSONS")
    df_copy["STORE TYPE"] = df_copy["STORE TYPE"].replace("KROGER", "KROGER-ALBERTSONS")
    df_copy["PARENT NUMBER"] = df_copy["PARENT NUMBER"].replace(5995907.0,7521503.0)
    
    return df_copy

def remove_10pct(df, seed_value=124):
    """
    10% of Stores shut down after a merger; this function randomly drops 10% of Kroger and Albertson owned stores on a national scale.
    It calculates and prints the sum of "EMPLOYEE SIZE (5) - LOCATION" from the removed rows before returning the DataFrame.
    """
    np.random.seed(seed_value)

    merger_subset = df.loc[(df["STORE TYPE"] == "KROGER") | (df["STORE TYPE"] == "ALBERTSONS")]

    remove_n = math.ceil(merger_subset.shape[0] * 0.1)

    drop_indices = np.random.choice(merger_subset.index, remove_n, replace=False)

    # Calculate and print the sum of "EMPLOYEE SIZE (5) - LOCATION" from the removed rows
    sum_of_employee_size_removed = df.loc[drop_indices]["EMPLOYEE SIZE (5) - LOCATION"].sum()
    print(f"Predicted Number of Employees Displaced: {sum_of_employee_size_removed}")

    df = df.drop(drop_indices)
    
    df["STORE TYPE"] = df["STORE TYPE"].replace("ALBERTSONS", "KROGER-ALBERTSONS")
    df["STORE TYPE"] = df["STORE TYPE"].replace("KROGER", "KROGER-ALBERTSONS")
    df["PARENT NUMBER"] = df["PARENT NUMBER"].replace(5995907.0,7521503.0)

    return df