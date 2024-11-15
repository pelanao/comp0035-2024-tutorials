
import pathlib
from pathlib import Path 

import pandas as pd
import sqlite3

def squeal(df, db_path=None):
    """ Creates an un-normalised table from a dataframe and saves it to a database file

        Parameters:
            df (DataFrame): dataframe with student_data.csv
 
        Returns:
            squeal.db (database): generated in src folder
    """
    # file name for database
    db_path = Path(__file__).parent / 'squeal.db'

    # Create a connection to the database using sqlite3.
    conn = sqlite3.connect(db_path)

    # create 'enrollments' table using dataframe.to_sql to save the dataframe to a table called
    df.to_sql('enrollments', conn, if_exists='replace', index=False)

    # close connection
    conn.close()
    return

def main():
    """"
    Main logic for the program
    Reads the provided csv files into DataFrame format
    """
    try:
        student_data_csv = Path(__file__).parent / 'tutorialpkg' / 'data_db_activity' / 'student_data.csv'
        db_squeal = pd.read_csv(student_data_csv)
    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")

    # converts dataframe into sql database
    squeal(db_squeal)



if __name__ == "__main__":
    main()