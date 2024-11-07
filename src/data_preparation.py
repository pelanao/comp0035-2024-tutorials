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
    pd.set_option("display.max_columns", None)
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
            print(f"change {column}")
            # df[column] = df[column].astype(int)

        # method2: change columns given to int datatype
        if column in columns_to_change:
            print(f"change {column}")
            # df[column] = df[column].astype(int)

    # change date columns into appropriate DataFrame date format
    df['start'] = pd.to_datetime(df['start'], format='%d/%m/%Y')
    df['end'] = pd.to_datetime(df['end'], format='%d/%m/%Y')
    # print(df.loc[:,['start','end']] )

    return[df]


def main():
    """"
    Main logic for the program
    Reads the provided databases into DataFrame format
    """

    try:
        paralympics_events_csv = pathlib.Path(__file__).parent/'tutorialpkg'/'data'/'paralympics_events_raw.csv'      # store provided .csv file
        paralympics_events = pd.read_csv(paralympics_events_csv)                                                      # read csv file into DataFrame
    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")
        exit()

    try:
        paralympics_all_xlsx = pathlib.Path(__file__).parent / 'tutorialpkg' /'data' / 'paralympics_all_raw.xlsx'            # store provided .xlsx file name
        paralympics_all = pd.read_excel(paralympics_all_xlsx, sheet_name=0)                                                  # read first sheet of Excel file into DataFrame
        medal_standings = pd.read_excel(paralympics_all_xlsx, sheet_name=1)                                                  # read second sheet of Excel file into DataFrame
    except FileNotFoundError as e:
        print(f"Excel file not found. Please check the file path. Error: {e}")
        exit()
    
    # # call the function to describe the dataframe
    # describe_dataframe(paralympics_events)
    # describe_dataframe(paralympics_all)
    # describe_dataframe(medal_standings)

    change_datatype(paralympics_events)

    # print(paralympics_events.loc[:,['start', 'end']])
    # print(paralympics_all.loc[:,['start', 'end']])



if __name__ == "__main__":
    main()