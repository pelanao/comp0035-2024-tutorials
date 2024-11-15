
import pathlib
import pandas as pd

def describe_dataframe(DataFrame):
    """ Describe an imported data file stored in DataFrame format. Will print the shape, the head and tail
        the label of all columns, the data type of ech column, the dataframe information and descriptive statistics.
 
        Parameters:
            DataFrame (DataFrame): an imported csv or excel in dataframe format, to be described
 
        Returns:
            None
    """
    print(f"\nShape of the DataFrame: \n{DataFrame.shape}\n")
    print(f"\nFirst 5 rows of the DataFrame: \n{DataFrame.head()}")
    print(f"\nLast 5 rows of the DataFrame: \n{DataFrame.tail()}\n" )
    print(f"\nColumn names: \n{DataFrame.columns}\n")
    print(f"\nData types of the columns: \n{DataFrame.dtypes}\n")
    print(f"\nInfo about the DataFrame: \n{DataFrame.info()}\n")
    print(f"\nSummary statistics: \n{DataFrame.describe()}\n")


def change_datatype(df):
    """ Change datatype of columns to desired format.
        Columns in float64 are changed to int, columns related to dates are changed to datetime64,
        and columns are standardised to avoid categorisation issues
 
        Parameters:
            DataFrame (DataFrame): an imported csv or excel in dataframe format, to be modified
 
        Returns:
            modified dataframe
    """

    # change all float64 datatypes to int
    for column in df:
        # method1: change all columns in float64 datatype to int
        if df[column].dtypes == 'float64':
            # print(f"change {column}")
            df[column] = df[column].astype(int)

    # change date columns into appropriate DataFrame date format
    df['start'] = pd.to_datetime(df['start'], format='%d/%m/%Y')
    df['end'] = pd.to_datetime(df['end'], format='%d/%m/%Y')

    # standardise 'type' column by removing whitespace and changing to lowercase
    df['type'] = df['type'].str.strip()
    df['type'] = df['type'].str.lower()
    return df


def main():
    """"
    Main logic for the program
    Reads the provided databases into DataFrame format
    """

    # read paralympics_events.csv file into DF
    try:
        db_events_csv = pathlib.Path(__file__).parent/'tutorialpkg'/'data_db_activity'/'paralympics_events.csv'      # store provided .csv file
        df_events = pd.read_csv(db_events_csv)     # read csv file into DataFrame
    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")
        exit()

    # describe_dataframe(df_events)
    df_events = change_datatype(df_events)
    print(df_events.dtypes)
    




if __name__ == "__main__":
    main()