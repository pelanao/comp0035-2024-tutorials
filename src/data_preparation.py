import pathlib
import pandas as pd

def describe_dataframe(DataFrame):
    """ Describe an imported data file stored in DataFrame format. Will print the shape, the head and tail
        the label of all columns, the data type of ech column, the dataframe information and descriptive statistics.
 
        Parameters:
            DataFrame (DataFrame): an imported csv or excel in dataframe format, to be described
 
        Returns:
            none
    """
    print(DataFrame.shape, "\n")
    print(DataFrame.head(), "\n", DataFrame.tail(), "\n", sep="",)
    print(DataFrame.columns, "\n")
    print(DataFrame.dtypes, "\n")
    print(DataFrame.info(), "\n")
    print(DataFrame.describe(), "\n")
    return

def change_datatype(df):
    """ Change datatype of columns to desired format.
        Columns in float64 are changed to int (requires debugging),
        and columns related to dates are changed to datetime64
 
        Parameters:
            DataFrame (DataFrame): an imported csv or excel in dataframe format, to be modified
 
        Returns:
            modified dataframe
    """

    # change all float64 datatypes to int
    columns_to_change= ['countries', 'events', 'participants_m', 'participants_f', 'participants']
    for column in df:
        # method1: change all columns in float64 datatype to int
        if df[column].dtypes == 'float64':
            # print(f"change {column}")
            # df[column] = df[column].astype(int)
            return

        # method2: change columns given to int datatype
        if column in columns_to_change:
            # print(f"change {column}")
            # df[column] = df[column].astype(int)
            return

    # change date columns into appropriate DataFrame date format
    df['start'] = pd.to_datetime(df['start'], format='%d/%m/%Y')
    df['end'] = pd.to_datetime(df['end'], format='%d/%m/%Y')
    # print(df.loc[:,['start','end']] )
    return[df]

def merge_npc(raw, npc):
    """ Merge event data with the npc codes and prepare for further processing

        Parameters:
            raw (DataFrame): pandas dataframe with event data
            npc (DataFrame): pandas dataframe with country codes
 
        Returns:
            merged(DataFrame): merged dataframe
    """
    # fix incompatible country names in the raw file
    raw = country_name(raw)

    # merge events_raw with npc_codes 
    merged = raw.merge(npc, how='left', left_on='country', right_on='Name')
    # print(f"\nMerged database country/codes: \n{merged.loc[:,['country', 'Code', 'Name']]}\n")

    # delete unwanted columns
    df_prepared = merged.drop(columns=['URL', 'disabilities_included', 'highlights', 'Name'], axis=1)

    # print number of missing values in merged dataframe df_prepared
    # print(f"\nMissing values in whole dataframe: \n{df_prepared.isna()}")

    # delete unwanted rows
    df_prepared = df_prepared.drop(index=[0,17,31])     #  drop rows for Rome 1960 and events set in the future due to missing data
    df_prepared = df_prepared.reset_index(drop=True)   # reset index of DF to skip dropped rows
    missing_rows = df_prepared[df_prepared.isna().any(axis=1)]  
    # print(f"\nMissing rows:\n{missing_rows}\n")     # confirm no rows have missing data


def country_name(DF):
    """ Replace country abbreviations with compatible names

        Parameters:
            DF (DataFrame): an imported csv or excel in dataframe format, to be modified
 
        Returns:
            fixed_DF (DataFrame): modified dataframe with compatible country names
    """
    replacement_names = {                               # dictionary of abbreviations and respective country names
        'UK': 'Great Britain',
        'USA': 'United States of America',
        'Korea': 'Republic of Korea',
        'Russia': 'Russian Federation',
        'China': "People's Republic of China"
    }
    fixed_DF = DF.replace(to_replace=replacement_names)     # replace abbrreviations with values found in the dictionary
    return(fixed_DF)

def main():
    """"
    Main logic for the program
    Reads the provided databases into DataFrame format
    """
    # set display ooptions for pandas
    pd.set_option("display.max_columns", None)

    # read events_raw.csv file into DF
    try:
        paralympics_events_csv = pathlib.Path(__file__).parent/'tutorialpkg'/'data'/'paralympics_events_raw.csv'      # store provided .csv file
        paralympics_events = pd.read_csv(paralympics_events_csv)                                                      # read csv file into DataFrame
    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")
        exit()

    #  read all.xlsx file into DF
    try:
        paralympics_all_xlsx = pathlib.Path(__file__).parent / 'tutorialpkg' /'data' / 'paralympics_all_raw.xlsx'            # store provided .xlsx file name
        paralympics_all = pd.read_excel(paralympics_all_xlsx, sheet_name=0)                                                  # read first sheet of Excel file into DataFrame
        medal_standings = pd.read_excel(paralympics_all_xlsx, sheet_name=1)                                                  # read second sheet of Excel file into DataFrame
    except FileNotFoundError as e:
        print(f"Excel file not found. Please check the file path. Error: {e}")
        exit()
    
    # read npc_codes.csv file into DF
    try:
        npc_codes_csv = pathlib.Path(__file__).parent/'tutorialpkg'/'data'/'npc_codes.csv'      # store provided .csv file
        npc_codes = pd.read_csv(npc_codes_csv, encoding='utf-8', encoding_errors='ignore', usecols=['Code', 'Name'])    # read csv file into DataFrame, accounting for encoding errors in csv file
    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")
        exit()
    
    # call function to merge with npc codes
    merge_npc(paralympics_events, npc_codes)

    # # call the function to describe the dataframe
    # describe_dataframe(paralympics_events)
    # describe_dataframe(paralympics_all)
    # describe_dataframe(medal_standings)
    # describe_dataframe(npc_codes)

    # # change datatypes into desired format
    # change_datatype(paralympics_events)
    # change_datatype(paralympics_all)


if __name__ == "__main__":
    main()