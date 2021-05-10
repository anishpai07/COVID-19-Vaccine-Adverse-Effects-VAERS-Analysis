import pandas as pd
import numpy as np
from numba import jit
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns


def create_dataframe(filename: str):
    """
    Takes the filename as a parameter and loads the data and returns its DataFrame.

    param filename: Name of the file for which the DataFrame will be created.
    :return: The DataFrame with all its rows and columns.

    >>> create_dataframe("test.csv")
      Entities  Values
    0    Mango     NaN
    1   Banana     1.0
    2    Apple     2.0
    3   Orange     3.0

    """
    df = pd.read_csv(filename, engine='python')

    return df


def drop_null_values(dataframe: pd.DataFrame, subset: str):
    """
    Drops all data rows which has null values in the column passed in the function.

    :param dataframe:
    :param subset:
    :return: DATAFRAME OF EACH FILE DATA

    >>> a = create_dataframe("test.csv")
    >>> drop_null_values(a, subset= "Values")
      Entities  Values
    1   Banana     1.0
    2    Apple     2.0
    3   Orange     3.0

    """
    subset_list = [subset]
    dataframe = dataframe.dropna(subset=subset_list)
    return dataframe


@jit(forceobj=True)
def reformating_vaccine_count_data(dataframe):
    """
    Classify each doses of vaccine in numbers to do normalization


    :param dataframe: dataframe containing vaccine doses data
    :return: dataframe: Dataframe consisting of vaccines and its number of doses given till date
    """
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
    """
    Normalizing the the total count of vaccines for each vaccine manufacturer

    :param df: DataFrame consisting of count of vaccines administered of each manufacturer
    :return: Generates visualization for total vaccince count against total number of adverse
     effect reported for each manufacturer type.
    """
    df1 = df.copy()
    df1['vaccine_count'] = (df1['vaccine_count'] - df1['vaccine_count'].min()) / (
            df1['vaccine_count'].max() - df1['vaccine_count'].min())

    fig = px.histogram(df1, x="Vaccine_Brand", width=650,
                       title="Number of Reported Adverse Cases By Vaccine Manufacturers")
    fig.update_xaxes(categoryorder="total descending", title_text="Vaccine Manufacturer")


def hypothesis_validation(dataframe: pd.DataFrame):
    """
    This functions is used to compare the data frame and count number of people having symptoms based on prior health conditions.

    :param dataframe: dataframe consisting of symptoms data
    :return: A list of count of people with and without symptoms
    """
    compare = np.where(dataframe['HISTORY'] == dataframe['ALLERGIES'], True, False)
    dataframe["Comparison"] = compare
    vaers_data_vax_v4 = dataframe[dataframe['Comparison'] == True]
    vaers_data_vax_v5 = dataframe[dataframe['Comparison'] == False]
    history_allergies_count = vaers_data_vax_v5.shape[0]
    no_history_allergies_count = vaers_data_vax_v4.shape[0]

    return [no_history_allergies_count, history_allergies_count]


def hypothesis_2_visualization(count):
    """
     This function develops pie chart to test HYPOTHESIS 3

    :param count: List of total number of people who developed symptoms with/without having prior health symptoms
    """
    mylabels = ["Without prior allergy and medical history", " With prior allergy and medical history"]
    myexplode = [0.2, 0]
    mycolors = ["c", "y"]
    plt.pie(count, labels=mylabels, explode=myexplode, shadow=True, colors=mycolors)
    plt.legend(title="Number of Reported persons")
    plt.show()


def hypothesis_4_visualization(dataframe1, vaers_symptoms):
    """
    Functions displays visualization of different types of symptoms administered for each vaccine type

    :param count:
    """
    vaers_vax_v2 = dataframe1[['VAERS_ID', 'VAX_TYPE', 'VAX_MANU']]
    vaer_symptoms_vax = vaers_symptoms.merge(vaers_vax_v2, on="VAERS_ID", how="left")
    vaer_symptoms_moderna = vaer_symptoms_vax[vaer_symptoms_vax['VAX_MANU'] == 'MODERNA']
    vaer_symptoms_pfizer = vaer_symptoms_vax[vaer_symptoms_vax['VAX_MANU'] == 'PFIZER\BIONTECH']
    vaer_symptoms_jannsen = vaer_symptoms_vax[vaer_symptoms_vax['VAX_MANU'] == 'JANSSEN']

    # Graph for Moderna
    figure1 = px.histogram(vaer_symptoms_moderna, x="SYMPTOM1", width=650,
                           color_discrete_sequence=px.colors.diverging.Spectral[4::-2]
                           , title="Count of Different symptoms reported for Moderna")
    figure1.update_xaxes(categoryorder="total descending", title_text="Symptom Types")
    figure1.show()

    # Graph for Pfizer
    figure2 = px.histogram(vaer_symptoms_pfizer, x="SYMPTOM1", width=650,
                           color_discrete_sequence=px.colors.diverging.Spectral[-4::-3]
                           , title="Count of different Symptoms for Pfizer")
    figure2.update_xaxes(categoryorder="total descending", title_text="Symptom Types")
    figure2.show()

    # Graph for Jannsen
    figure3 = px.histogram(vaer_symptoms_jannsen, x="SYMPTOM1", width=650,
                           color_discrete_sequence=px.colors.diverging.Spectral[3::1],
                           title="Count of Different Symptoms reported for Johnson & Johnson")
    figure3.update_xaxes(categoryorder="total descending", title_text="Symptom Types")
    figure3.show()


def replace_garbage_values_with_nan(dataframe: pd.DataFrame):
    """
    Cleaning the data to normalize data in HISTORY and ALLERGIES columns in VAERSDATA dateset

    :param dataframe: vaer_data
    :return: cleaned data set

    >>> a = create_dataframe("test1.csv")
    >>> replace_garbage_values_with_nan(a)
      PATIENT ALLERGIES  HISTORY
    0    Andy    Gluten      NaN
    1   Wayne       NaN      NaN
    2    Colt       NaN      NaN
    3   Aaron    Pollen  5 years

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
    mean = int(df["Days"].mean())
    return mean


@jit(forceobj=True)
def time_to_int(t):
    """
     Converts time from String data type to Integer.

    :param t: Time in string format
    :return: Time in int data type
    """
    return int(str(t).split(' ')[0])


def statewise_analysis(states_data):
    """
    Grouping the state and vaccine type for each state and then calculating the sum total.
    Also visualizing vaccines provided of each type per state.

    :param states_data: Vaccinations data of each state
    :return:
    """
    states_data.fillna(0)
    states_v1 = states_data.groupby(['Province_State', 'Vaccine_Type']).agg('sum')
    states_v1 = states_data.groupby(['Province_State', 'Vaccine_Type']).agg('sum')
    states_v1["Doses"] = states_v1["Doses_admin"] / states_v1["Doses_alloc"]
    states_v1.replace([np.inf, -np.inf], np.nan, inplace=True)
    states_v1.replace([np.nan], 0, inplace=True)

    x = states_v1.index.map(lambda t: t[0])
    y = states_v1.index.map(lambda t: t[1])
    sns.set_palette("Set1", 8, .75)
    doses = states_v1["Doses"]
    df = pd.DataFrame({'states': x, 'vaccine': y, 'doses': doses})
    sns.set(rc={'figure.figsize': (12.7, 9)})
    ax = sns.histplot(df, x='states', hue='vaccine', weights='doses',
                      multiple='stack', shrink=0.6)
    ax.set_ylabel('doses')
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=60)
    plt.xticks(rotation=90)
    legend = ax.get_legend()
    legend.set_bbox_to_anchor((1, 1))
    plt.show()
    # return states_v1


def state_abbreviations(df):
    """
    Mapping of state initials to corresponding state name.
    ONLY THIS DICT (NOT FUNCTION) WAS REFERENCED FROM https://gist.github.com/rogerallen/1583593

    :param df: data frame consisting of States Initials
    :return: Correctly mapped State names as per initials
    """
    #
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
    state_data_v1 = state_data[state_data['Date'] > "2021-01-01"]
    state_data_v2 = state_abbreviations(state_data)
    state_data_v3 = statewise_analysis(state_data_v2)
    print(state_data_v1['Date'])

    # print(state_data_v2.head(200))

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
    vax_dict = {'MODERNA': 'Moderna', 'PFIZER\BIONTECH': 'Pfizer'}
    vaers_vax_v2 = vaers_vax_v1.replace({"VAX_MANU": vax_dict})
    vaers_vax_v3 = vaers_vax_v2[['VAERS_ID', 'VAX_TYPE', 'VAX_MANU']]

    # JOIN VAERS DATA WITH COVID-19 VAERS VAX
    vaers_data_vax = vaers_data.merge(vaers_vax_v2, on="VAERS_ID", how="left")

    # DROP ROWS WITH NAN VALUES IN THE AGE_YRS COLUMN
    vaers_data_vax_v1 = drop_null_values(vaers_data_vax, subset='AGE_YRS')
    vaers_data_vax_v2 = vaers_data_vax_v1[['VAERS_ID', 'VAX_MANU']]

    # CLEANING HISTORY AND ALLERGY COLUMNS
    vaers_data_vax_v3 = replace_garbage_values_with_nan(vaers_data_vax)

    # NORMALIZING THE DATASET FOR CORRECT ACCURACY
    normalizing_columns(reformating_vaccine_count_data(vaers_data_vax_v2))

    # VISUALIZE THE NUMBER OF REPORTED ADVERSE CASES BY VACCINE MANUFACTURERS.
    # Can remove this below code moved it to a function

    fig = px.histogram(vaers_data_vax_v2, x="VAX_MANU", width=650,
                       title="Vaccines Administered vs Reported Adverse Effects", barmode="overlay")
    fig.update_xaxes(categoryorder="total descending", title_text="Vaccine Manufacturer")
    fig1 = px.bar(state_data_v2, x="Vaccine_Type", y="Doses_admin", width=650,
                  title="Total Number of Vaccines", barmode="overlay", color="Vaccine_Type")
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig1.data[1])
    fig.add_trace(fig1.data[2])
    fig.show()


    # HYPOTHESIS 2 VISUALIZATION
    output = hypothesis_validation(vaers_data_vax_v3)
    hypothesis_2_visualization(output)

    # HYPOTHESIS 4 VISUALIZATION
    hypothesis_4_visualization(vaers_vax_v1, vaers_symptoms)

    # HYPOTHESIS ONE VISUALISATION
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

    # moderna_onset = avg_onset(moderna_v1)
    # print(moderna_onset)
    # pfizer_onset = avg_onset(pfizer_v1)
    # print(pfizer_onset)
    # janssen_onset = avg_onset(janssen_v1)
    # print(janssen_onset)
    vacc_date = '2020-1-1'
    moderna_after_2020 = moderna_v1['VAX_DATE'] >= vacc_date
    filtered_dates = moderna_v1.loc[moderna_after_2020]

    filtered_dates_1 = filtered_dates["Days"].astype('timedelta64[D]')

    fig1 = px.histogram(filtered_dates_1, x="Days", width=650,
                        title="Number of Reported Adverse Cases By Vaccine Manufacturers")
    # fig1.update_xaxes(categoryorder="total descending", title_text="Vaccine Manufacturer")
    # fig1.show()
