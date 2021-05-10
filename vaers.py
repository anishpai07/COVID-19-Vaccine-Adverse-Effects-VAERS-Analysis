import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt



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
    Drops all data rows which has null values in the column passed in the function.

    :param dataframe:
    :param subset:
    :return: DATAFRAME OF EACH FILE DATA
    """
    subset_list = [subset]
    dataframe = dataframe.dropna(subset=subset_list)
    return dataframe


def reformating_vaccine_count_data(dataframe):
    modern_count = 0
    pfizer_count = 0
    Janssen_count = 0
    others = 0
    for x in dataframe['VAX_MANU']:
        if x == 'MODERNA':
            modern_count = modern_count + 1
        elif x == 'PFIZER\BIONTECH':
            pfizer_count = pfizer_count + 1
        elif x == 'JANSSEN':
            Janssen_count = Janssen_count + 1
        else:
            others = +1

    vaccination = {'vaccine_count': [modern_count, pfizer_count, Janssen_count, others],
                   'Vaccine_Brand': ['Moderna', 'Pfizer', 'Janssen', 'Other']}
    df = pd.DataFrame(vaccination, columns=['Vaccine_Brand', 'vaccine_count'])
    return df


def normalizing_columns(df):
    df1 = df.copy()

    #df1['vaccine_count'] = MinMaxScaler().fit_transform(np.array(df1['vaccine_count'].reshape(0, 1)))
    df1['vaccine_count'] = (df1['vaccine_count'] - df1['vaccine_count'].min()) / (df1['vaccine_count'].max() - df1['vaccine_count'].min())
    #print(df1)
    # Not working will check later
    fig = px.histogram(df1, x="Vaccine_Brand", width=650,
                       title="Number of Reported Adverse Cases By Vaccine Manufacturers")
    fig.update_xaxes(categoryorder="total descending", title_text="Vaccine Manufacturer")
    #fig.show()


def hypothesis_validation(dataframe: pd.DataFrame):
    """
    This functions is used to compare the data frame and count number of people having symptoms based on prior health conditions.

    :param dataframe:
    :return: list of count of people with and without symptoms
    """
    compare = np.where(dataframe['HISTORY'] == dataframe['ALLERGIES'], True, False)
    dataframe["Comparison"] = compare
    vaers_data_vax_v4 = dataframe[dataframe['Comparison'] == True]
    vaers_data_vax_v5 = dataframe[dataframe['Comparison'] == False]
    history_allergies_count = vaers_data_vax_v5.shape[0]
    no_history_allergies_count = vaers_data_vax_v4.shape[0]

    return ([no_history_allergies_count, history_allergies_count])


def hypothesis_visualization(count):
    """
     This function develops pie chart to test HYPOTHESIS 3

    :param count: List of total number of people who developed symptoms with/without having prior health symptoms
    """
    mylabels = ["Without prior allergy and medical history", " With prior allergy and medical history"]
    myexplode = [0.2, 0]
    mycolors = ["c", "y"]
    plt.pie(count, labels=mylabels, explode=myexplode, shadow=True, colors=mycolors)
    plt.legend(title="Number of Reported persons")
    #plt.show()


def replace_garbage_values_with_nan(dataframe: pd.DataFrame):
    """
    dummy
    Cleaning the data to normalize data in HISTORY and ALLERGIES columns in VAERSDATA dateset

    :param dataframe: vaer_data
    :return: cleaned data set
    """

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
    """
    :param df: Dataframe
    :return: Mean of the days between vaccine and onset of symptoms
    """
    mean = int(df["Days"].dt.days.mean())
    return mean

def time_to_int(t):
    return int(str(t).split(' ')[0])

def statewise_analysis(states_data):
    states_data.fillna(0)
    states_v1 = states_data.groupby(['Province_State', 'Vaccine_Type']).agg('sum')
    print(states_v1.columns)
    return states_v1
    #print(states_v1['Doses_admin'])
    #states_v2 = states_v1[['Province_State', 'Date', 'Vaccine_Type', 'Doses_admin']]
    #print(states_v2.head(10))

def state_abbreviations(df):
    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'American Samoa': 'AS',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'District of Columbia': 'DC',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Guam': 'GU',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Northern Mariana Islands': 'MP',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Puerto Rico': 'PR',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virgin Islands': 'VI',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY'
    }

    df1 = df.replace({"Province_State": us_state_abbrev})
    return df1


if __name__ == "__main__":
    # LOAD ALL VAERS DATASETS.
    vaers_data = create_dataframe("2021VAERSData.csv")
    vaers_symptoms = create_dataframe("2021VAERSSYMPTOMS.csv")
    vaers_vax = create_dataframe("2021VAERSVAX.csv")
    state_data = create_dataframe("vaccine_data_us_timeline.csv")
    statewise_analysis(state_data)
    state_data_v1 = state_abbreviations(state_data)
    #print(state_data_v1.head(100))


    # DATA CLEANING AND PREPROCESSING: VACCINATIONS PER STATE

    # DROP LOCATIONS WHICH ARE NOT A US STATE
    vaccinations_per_state = create_dataframe("us_state_vaccinations.csv")
    remove_locations = vaccinations_per_state['location'].isin(
        ['Bureau of Prisons', 'Dept of Defense', 'Long Term Care', 'United States', 'Indian Health Svc'])
    vaccinations_per_state_v1 = vaccinations_per_state[~remove_locations]

    # DROP ROWS WITH NAN VALUES IN THE TOTAL VACCINATIONS COLUMN
    vaccinations_per_state_v2 = drop_null_values(vaccinations_per_state_v1, 'total_vaccinations')

    # DATA CLEANING AND PREPROCESSING: VAERS VAX

    # GET ALL VACCINATION DATA FOR COVID-19 VACCINES ONLY.
    vaers_vax_v1 = vaers_vax[vaers_vax['VAX_TYPE'] == 'COVID19']
    vaers_vax_v2 = vaers_vax_v1[['VAERS_ID', 'VAX_TYPE', 'VAX_MANU']]

    # JOIN VAERS DATA WITH COVID-19 VAERS VAX
    vaers_data_vax = vaers_data.merge(vaers_vax_v2, on="VAERS_ID", how="left")

    # DATA CLEANING AND PREPROCESSING: VAERS DATA VAX

    # DROP ROWS WITH NAN VALUES IN THE AGE_YRS COLUMN
    vaers_data_vax_v1 = drop_null_values(vaers_data_vax, subset='AGE_YRS')
    vaers_data_vax_v2 = vaers_data_vax_v1[['VAERS_ID', 'VAX_MANU']]

    # CLEAN HISTORY AND ALLERGY COLUMNS
    vaers_data_vax_v3 = replace_garbage_values_with_nan(vaers_data_vax)

    # NORMALIZING THE DATASET FOR CORRECT ACCURACY
    normalizing_columns(reformating_vaccine_count_data(vaers_data_vax_v2))

    # VISUALIZE THE NUMBER OF REPORTED ADVERSE CASES BY VACCINE MANUFACTURERS.
    # Can remove this below code moved it to a function
    fig = px.histogram(vaers_data_vax_v2, x="VAX_MANU", width=650,
                       title="Number of Reported Adverse Cases By Vaccine Manufacturers")
    fig.update_xaxes(categoryorder="total descending", title_text="Vaccine Manufacturer")
    #fig.show()

    # HYPOTHESIS 2 VISUALIZATION
    output = hypothesis_validation(vaers_data_vax_v3)
    hypothesis_visualization(output)

    # HYPOTHESIS ONE VISUALISATION ## make a function for it
    vaers_symptoms_vax = vaers_symptoms.merge(vaers_vax, on='VAERS_ID', how='left')
    whole_dataset = vaers_symptoms_vax.merge(vaers_data, on='VAERS_ID',
                                             how='left')  # Whole dataset merged into a dataframe

    relevant_data = whole_dataset.filter(
        ['VAX_NAME', 'VAX_DATE', 'ONSET_DATE'])  # Extracted relevant columns from the dataframe

    relevant_data['ONSET_DATE'] = pd.to_datetime(relevant_data['ONSET_DATE'])  # convert columns into appropriate format
    relevant_data['VAX_DATE'] = pd.to_datetime(relevant_data['VAX_DATE'])

    relevant_data['Days'] = (relevant_data['ONSET_DATE'] - relevant_data[
        'VAX_DATE'])  # Finding number of days between vacc and symptoms

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
    vacc_date = '2020-1-1'
    moderna_after_2020 = moderna_v1['VAX_DATE'] >= vacc_date
    filtered_dates = moderna_v1.loc[moderna_after_2020]

    filtered_dates_1 = filtered_dates["Days"].astype('timedelta64[D]')

    fig1 = px.histogram(filtered_dates_1, x="Days", width=650,
                       title="Number of Reported Adverse Cases By Vaccine Manufacturers")
    #fig1.update_xaxes(categoryorder="total descending", title_text="Vaccine Manufacturer")
    #fig1.show()
