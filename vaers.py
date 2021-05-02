import pandas as pd
import numpy as np


def create_dataframe(filename:str):
    """Takes the filename as a parameter and loads the data and returns its DataFrame.

    param filename: Name of the file for which the DataFrame will be created.
    :return: The DataFrame with all its rows and columns.

    """
    df = pd.read_csv(filename, engine='python')

    return df


def drop_null_values(dataframe, subset):
    subset_list = [subset]
    dataframe = dataframe.dropna(subset=subset_list)
    return dataframe



if __name__ == "__main__":

    # LOAD ALL VAERS DATASETS.
    vaers_data = create_dataframe("2021VAERSData.csv")
    vaers_symptoms = create_dataframe("2021VAERSSYMPTOMS.csv")
    vaers_vax = create_dataframe("2021VAERSVAX.csv")
    #print(vaers_vax)

    # VACCINATIONS PER STATE DATA CLEANING AND PREPROCESSING.

    # DROP LOCATIONS WHICH ARE NOT A US STATE
    vaccinations_per_state = create_dataframe("us_state_vaccinations.csv")
    remove_locations = vaccinations_per_state['location'].isin(
        ['Bureau of Prisons', 'Dept of Defense', 'Long Term Care', 'United States', 'Indian Health Svc'])
    vaccinations_per_state_v1 = vaccinations_per_state[~remove_locations]

    # DROP ROWS WITH NAN VALUES IN THE TOTAL VACCINATIONS COLUMN
    #vaccinations_per_state_v2 = vaccinations_per_state_v1.dropna(subset=['total_vaccinations'])
    vaccinations_per_state_v2 = drop_null_values(vaccinations_per_state_v1, 'total_vaccinations')
    #print(vaccinations_per_state_v1.location.unique())
    print(vaccinations_per_state_v2['total_vaccinations'])

