
import pathlib
from pathlib import Path 

import pandas as pd
import sqlite3

def unnormal_db(df, db_path=None, table_name=None):
    """ Creates an un-normalised table from a dataframe and saves it to a database file

        Parameters:
            df (DataFrame): input dataframe
            db_path (Path): desired file name of new database
            table_name (str): desired table name within new database
 
        Returns:
            db (database): generated in src folder
    """
    if not db_path or not table_name:
        return      # if any arguments are missing, return to main
    
    # Create a connection to the database file path using sqlite3.
    conn = sqlite3.connect(db_path)

    # save df as table_name table within db_path file using dataframe.to_sql
    df.to_sql(table_name, conn, if_exists='replace', index=False)

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
        df_student = pd.read_csv(student_data_csv)
    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")

    # store desired path src/tutorialpkg/data_db_activity/enrollments_unnormalised.db
    db_name = Path(__file__).parent / 'tutorialpkg' / 'data_db_activity' / 'enrollments_unnormalised.db'

    # converts dataframe into an unnormalised table within sql database
    unnormal_db(df_student, db_name, 'enrollments')


if __name__ == "__main__":
    main()