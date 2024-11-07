

import pathlib
import pandas as pd

def describe_dataframe(DataFrame):
    """docstrings
    convert imported file to a DataFrame format
    
    
    """
    print()
    return



if __name__ == '__main__':
    describe_dataframe("file")
    paralympics_events_csv = pathlib.Path(__file__).parent / 'tutorialpkg' / 'data' / 'paralympics_events_raw.csv'      # store provided .csv file name
    paralympics_events = pd.read_csv(paralympics_events_csv)                                                            # read csv file into DataFrame

    paralympics_all_xlsx = pathlib.Path(__file__).parent / 'tutorialpkg' /'data' / 'paralympics_all_raw.xlsx'            # store provided .xlsx file name
    paralympics_all = pd.read_excel(paralympics_all_xlsx, sheet_name=0)                                                  # read first sheet of Excel file into DataFrame
    medal_standings = pd.read_excel(paralympics_all_xlsx, sheet_name=1)                                                  # read second sheet of Excel file into DataFrame

    print()
