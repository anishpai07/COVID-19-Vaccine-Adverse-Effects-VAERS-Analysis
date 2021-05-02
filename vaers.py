import pandas as pd
import numpy as np


def create_dataframe(filename: str):
    """
    Takes the filename as a parameter and loads the data and returns its DataFrame.

    param filename: Name of the file for which the DataFrame will be created.
    :return: The DataFrame with all its rows and columns.

    """
    df = pd.read_csv(filename, engine='python')

    return df


def drop_null_values(dataframe: pd.DataFrame, subset: str):
    """

    :param dataframe:
    :param subset:
    :return:
    """
    subset_list = [subset]
    dataframe = dataframe.dropna(subset=subset_list)
    return dataframe


if __name__ == "__main__":

    # LOAD ALL VAERS DATASETS.
    vaers_data = create_dataframe("2021VAERSData.csv")
    vaers_symptoms = create_dataframe("2021VAERSSYMPTOMS.csv")
    vaers_vax = create_dataframe("2021VAERSVAX.csv")
    # print(vaers_vax)

    # DATA CLEANING AND PREPROCESSING: VACCINATIONS PER STATE

    # DROP LOCATIONS WHICH ARE NOT A US STATE
    vaccinations_per_state = create_dataframe("us_state_vaccinations.csv")
    remove_locations = vaccinations_per_state['location'].isin(
        ['Bureau of Prisons', 'Dept of Defense', 'Long Term Care', 'United States', 'Indian Health Svc'])
    vaccinations_per_state_v1 = vaccinations_per_state[~remove_locations]

    # DROP ROWS WITH NAN VALUES IN THE TOTAL VACCINATIONS COLUMN
    vaccinations_per_state_v2 = drop_null_values(vaccinations_per_state_v1, 'total_vaccinations')
    # print(vaccinations_per_state_v1.location.unique())

    # GET ALL VACCINATION DATA FOR COVID-19 VACCINES ONLY.
    vaers_vax_v1 = vaers_vax[vaers_vax['VAX_TYPE'] == 'COVID19']
    vaers_vax_v2 = vaers_vax_v1[['VAERS_ID', 'VAX_TYPE', 'VAX_MANU']]
    # print(vaers_vax_v2.info)

    # JOIN VAERS DATA WITH COVID-19 VAERS VAX
    vaers_data_vax = vaers_data.merge(vaers_vax_v2, on="VAERS_ID", how="left")
    # print(vaers_data_vax.isnull().sum())

    # DATA CLEANING AND PREPROCESSING: VAERS DATA VAX

    # DROP ROWS WITH NAN VALUES IN THE AGE_YRS COLUMN
    vaers_data_vax_v1 = drop_null_values(vaers_data_vax, subset='AGE_YRS')
    print(vaers_data_vax_v1)

