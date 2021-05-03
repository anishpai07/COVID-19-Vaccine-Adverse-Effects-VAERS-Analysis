import pandas as pd
import numpy as np
import plotly.express as px


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


def hypothesis_validation(dataframe: pd.DataFrame):
    """

    :param dataframe:
    :return:
    """
    compare = np.where(dataframe['HISTORY'] == dataframe['ALLERGIES'], True, False)
    dataframe["Comparison"] = compare
    vaers_data_vax_v4 = dataframe[dataframe['Comparison'] == True]
    vaers_data_vax_v5 = dataframe[dataframe['Comparison'] == False]
    history_allergies_count = vaers_data_vax_v5.shape[0]
    no_history_allergies_count = vaers_data_vax_v4.shape[0]
    # vaers_data_vax_v5 = vaers_data_vax_v4[['VAERS_ID', 'HISTORY', 'ALLERGIES', 'Comparison']]

    print(no_history_allergies_count, history_allergies_count)



def replace_garbage_values_with_nan(dataframe: pd.DataFrame):
    """

    :param dataframe: vaer_data
    :return: cleaned data set
    """
    # print(dataframe)
    dataframe['ALLERGIES'] = dataframe['ALLERGIES'].replace(
        ['Na', 'None', 'N/A', 'none', 'N/a', 'n/a', 'None known', 'No', 'None according to consent form she filled out',
         'no known allergies', '',
         'No known allergies', '0', '----', '-', 'No known allergies', 'None Stated', 'No history of allergies',
         'None reported', '#Name?', '(Blank)', 'No Known Allergies to medication', 'none that I am aware of',
         'None according to consent form she filled out',
         'no known allergies', 'None reported', 'no known', 'No known', 'Not that I know of.', 'No known allergies',
         'Not that I know of', 'None noted', 'NONE LISTED', 'unknown', 'Unknown', 'none known',
         'NO KNOWN ALLERGIES', 'No allergies', 'No known drug allergies', 'No Known Allergies', 'None disclosed', 'NO',
         'None per patient report', 'no', 'None stated', 'NONE', 'NO Known Allergies', 'none on file', '-none-',
         'None that the patient reported', 'No known defined allergies.', 'No confirmed allergies.',
         'Non that I?m aware of', 'No previous known Allergies', 'No severe allergies reported on questionaire',
         'No known drug/food allergies',
         'No any allergies', 'No Known Drug Allergies', 'no allergies'], 'NaN')

    dataframe['HISTORY'] = dataframe['HISTORY'].replace(
        ['Na', 'None', 'NONE', 'N/A', 'none', 'N/a', 'n/a', 'None known', 'No',
         'None according to consent form she filled out', 'no known allergies', '',
         'None on record', '0', '----', '-', 'not available', 'None Stated',
         'None per client', 'None reported', 'none applicable', '(Blank)',
         'None reported', 'none that I am aware of',
         'None according to consent form she filled out',
         'NONE TO SPEAK OF', 'None reported', 'no known', 'No known', 'Unknown', 'none known',
         'None identified', 'NONE NOTED', 'Not that I know of', 'None noted',
         'NONE LISTED', 'unknown',
         ], 'NaN')

    return dataframe


def avg_onset(df):
    '''

    :param df: Dataframe
    :return: Mean of the days between vaccine and onset of symptoms
    '''
    mean = int(df["Days"].dt.days.mean())
    return mean


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
    vaers_data_vax_v2 = vaers_data_vax_v1[['VAERS_ID', 'VAX_MANU']]
    #print(vaers_data_vax_v1)

    # CLEANING HISTORY AND ALLERGY COLUMNS
    vaers_data_vax_v3 = replace_garbage_values_with_nan(vaers_data_vax)



    # VISUALIZE THE NUMBER OF REPORTED ADVERSE CASES BY VACCINE MANUFACTURERS.
    fig = px.histogram(vaers_data_vax_v2, x="VAX_MANU", width=650,
                       title="Number of Reported Adverse Cases By Vaccine Manufacturers")
    fig.update_xaxes(categoryorder="total descending", title_text="Vaccine Manufacturer")
    fig.show()


    # VEDANT VISUALIZATION
    hypothesis_validation(vaers_data_vax_v3)



    # ANISH VIZ

    vaers_symptoms_vax = vaers_symptoms.merge(vaers_vax, on='VAERS_ID', how='left')
    whole_dataset = vaers_symptoms_vax.merge(vaers_data, on='VAERS_ID', how='left') #Whole dataset merged into a dataframe

    relevant_data = whole_dataset.filter(['VAX_NAME', 'VAX_DATE', 'ONSET_DATE']) #Extracted relevant columns from the dataframe

    relevant_data['ONSET_DATE'] = pd.to_datetime(relevant_data['ONSET_DATE']) #convert columns into appropriate format
    relevant_data['VAX_DATE'] = pd.to_datetime(relevant_data['VAX_DATE'])

    relevant_data['Days'] = (relevant_data['ONSET_DATE'] - relevant_data['VAX_DATE']) #Finding number of days between vacc and symptoms
    #print(relevant_data)

    moderna = relevant_data.loc[relevant_data['VAX_NAME'] == 'COVID19 (COVID19 (MODERNA))']
    moderna_v1 = moderna[moderna.Days.notnull()]

    pfizer = relevant_data.loc[relevant_data['VAX_NAME'] == 'COVID19 (COVID19 (PFIZER-BIONTECH))']
    pfizer_v1 = pfizer[pfizer.Days.notnull()]

    janssen = relevant_data.loc[relevant_data['VAX_NAME'] == 'COVID19 (COVID19 (JANSSEN))']
    janssen_v1 = janssen[janssen.Days.notnull()]

    moderna_onset = avg_onset(moderna_v1)
    # print(moderna_onset)
    pfizer_onset = avg_onset(pfizer_v1)
    # print(pfizer_onset)
    janssen_onset = avg_onset(janssen_v1)
    # print(janssen_onset)
