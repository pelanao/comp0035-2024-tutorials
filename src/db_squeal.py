
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

    # Commit the changes
    conn.commit()
    # close connection
    conn.close()


def normal_db(db_path):
    """ Creates a normalised database and tables in a database file

        Parameters:
            db_path (Path): desired file name of new database
            table_name (str): desired table name within new database
 
        Returns:
            db (database): generated in src folder
    """

    # variable_sql = '''CREATE TABLE table_name_1
                    #  (
                    #       column_name_1 data_type PRIMARY KEY,
                    #       column_name_2 data_type CONDITIONS,
                    #       column_name_3 data_type cONDITIONS,
                    #       FOREIGN KEY (column_name_1) REFERENCES table_name_2 (column_name_1)
                    #   );
    # SQL commands stored as a string within a python variable
    # Add python strings containing SQL statements that define the tables, their keys and any constraints
    student_sql = '''CREATE TABLE student (
                            student_id INTEGER PRIMARY KEY,
                            student_name STRING NOT NULL,
                            student_email STRING NOT NULL UNIQUE);
                            '''
    teacher_sql = '''CREATE TABLE teacher (
                            teacher_id INTEGER PRIMARY KEY,
                            teacher_name STRING NOT NULL,
                            teacher_email STRING NOT NULL UNIQUE);
                                '''
    course_sql = '''CREATE TABLE course (
                            course_id INTEGER PRIMARY KEY,
                            course_name STRING NOT NULL,
                            course_code INTEGER NOT NULL,
                            course_schedule STRING,
                            course_location STRING);
                            '''
    enrollment_sql = '''CREATE TABLE enrollment(
                            student_id INTEGER NOT NULL, 
                            course_id INTEGER NOT NULL,
                            teacher_id INTEGER,
                            PRIMARY KEY (student_id, course_id, teacher_id),
                            FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE CASCADE ON UPDATE CASCADE,
                            FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE ON UPDATE CASCADE,
                            FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id) ON UPDATE CASCADE ON DELETE SET NULL);
                            '''
    
    # Create a connection to the database file path using sqlite3.
    conn = sqlite3.connect(db_path)
    # create a cursor object using the connection
    cursor = conn.cursor()
    # enable FOREIGN KEYS explicitly for each database
    cursor.execute('PRAGMA foreign_keys = ON;')
    # Commit the changes
    conn.commit()

    # drop table if they already exist; order opposite than when created
    cursor.execute('DROP TABLE IF EXISTS enrollment;')
    cursor.execute('DROP TABLE IF EXISTS course;')
    cursor.execute('DROP TABLE IF EXISTS teacher;')
    cursor.execute('DROP TABLE IF EXISTS student;')

    # run commands to create tables in database
    # The order is important, you cannot create a child table before the parent table where there are relationships.
    cursor.execute(student_sql)
    cursor.execute(teacher_sql)
    cursor.execute(course_sql)
    cursor.execute(enrollment_sql)

    # Commit the changes
    conn.commit()
    # close connection
    conn.close()


def add_data(df, db_path):
    """ Adds data from the pandas datafrane to the normalised tables in a database file

        Parameters:
            df (DataFrame): input dataframe
            db_path (Path): desired file name of new database
            table_name (str): desired table name within new database
 
        Returns:
            db (database): generated in src folder
    """
    conn = sqlite3.connect(db_path)                 # Create a connection to the database file path using sqlite3.
    cursor = conn.cursor()                          # create a cursor object using the connection
    cursor.execute('PRAGMA foreign_keys = ON;')     # enable FOREIGN KEYS explicitly for each database
    conn.commit()                                   # Commit the changes

    # add data to student table
    student_sql = 'INSERT INTO student (student_name, student_email) VALUES (?, ?)'
    student_df = df[['student_name', 'student_email']].drop_duplicates()
    student_data = student_df.values.tolist()
    cursor.executemany(student_sql, student_data)

    # add data to teacher table
    teacher_sql = 'INSERT INTO teacher (teacher_name, teacher_email) VALUES (?, ?)'
    teacher_df = df[['teacher_name', 'teacher_email']].drop_duplicates()
    teacher_data = teacher_df.values.tolist()
    cursor.executemany(teacher_sql, teacher_data)

    # add data to teacher table
    course_sql = 'INSERT INTO course (course_name, course_code, course_schedule, course_location) VALUES (?, ?, ?, ?)'
    course_df = df[['course_name', 'course_code', 'course_schedule', 'course_location']].drop_duplicates()
    course_data = course_df.values.tolist()
    cursor.executemany(course_sql, course_data)

    # Iterate all the rows in the dataframe to find student, teacher and course of of each
    for index, row in df.iterrows():
        # Find student_id by using student_email, unique for every student in the table
        student_email = row['student_email']    # Extract email value from the row being iterated
        # Define the sql select query.
        select_student_sql = f'SELECT student_id FROM student WHERE student_email = "{student_email}"'
        # select student_id based on the student_email, assign first tuple to a variable result
        result = cursor.execute(select_student_sql).fetchone()
        # Extract integer student_id from tuple by specifying the first value
        s_id = result[0]
        
        # Find teacher_id
        teacher_email = row['teacher_email']
        select_teacher_sql = f'SELECT teacher_id FROM teacher WHERE teacher_email = "{teacher_email}"'
        result = cursor.execute(select_teacher_sql).fetchone()
        t_id = result[0]
        
        
        # Find course_id
        course_code = row['course_code']
        select_course_sql =  f'SELECT course_id FROM course WHERE course_code = "{course_code}"'
        result = cursor.execute(select_course_sql).fetchone()
        c_id = result[0]
        
        # Insert new row into the enrollment table
        enrollment_insert_sql = 'INSERT INTO enrollment (student_id, course_id, teacher_id) VALUES (?, ?, ?)'
        student_values = (s_id, t_id, c_id)
        cursor.execute(enrollment_insert_sql, student_values)

    # Commit the changes
    conn.commit()
    # close connection
    conn.close()


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
    unnormal_db_name = Path(__file__).parent / 'tutorialpkg' / 'data_db_activity' / 'enrollments_unnormalised.db'

    # converts dataframe into an unnormalised table within sql database
    unnormal_db(df_student, unnormal_db_name, 'enrollments')

    # generates a normalised database in the file path specified
    normal_db_name = Path(__file__).parent / 'tutorialpkg' / 'data_db_activity' / 'enrollment_normalised.db'
    normal_db(normal_db_name)
    add_data(df_student, normal_db_name)  


if __name__ == "__main__":
    main()