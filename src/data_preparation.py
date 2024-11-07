import pathlib
import pandas as pd

def describe_dataframe(DataFrame):
    """docstrings
    convert imported file to a DataFrame format
    
    
    """
    print()
    return



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

    try:
        paralympics_all_xlsx = pathlib.Path(__file__).parent / 'tutorialpkg' /'data' / 'paralympics_all_raw.xlsx'            # store provided .xlsx file name
        paralympics_all = pd.read_excel(paralympics_all_xlsx, sheet_name=0)                                                  # read first sheet of Excel file into DataFrame
        medal_standings = pd.read_excel(paralympics_all_xlsx, sheet_name=1)                                                  # read second sheet of Excel file into DataFrame
    except FileNotFoundError as e:
        print(f"Excel file not found. Please check the file path. Error: {e}")

if __name__ == "__main__":
    main()