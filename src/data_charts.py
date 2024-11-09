import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# set display options for pandas
pd.set_option("display.max_columns", None)


def histogram(df):
    """"
    Generates a histogram for each column of the dataset
    Generates a histogram for each of the specified columns 'participants_m' and 'participants_f'

    Parameters:
            df (DataFrame): pandas dataframe with event data
 
        Returns:
            histograms of relevant columns in the dataframe
    """
    
    # Create a histogram of the DataFrame
    df.hist()

    # Create a histogram of the specified columns in the DataFrame
    # df[['participants_m', 'participants_f']].hist()
    df.loc[:,['participants_m', 'participants_f']].hist()

    # Filter the DataFrame to select only rows where 'type' is 'summer' or 'winter respectively
    ### syntax: df = df[df['column_name'] == filter_value]
    summer_df = df[df['type'] == 'summer']
    winter_df = df[df['type'] == 'winter']
    # generate respective histograms
    summer_df.loc[:,['participants_m', 'participants_f']].hist()
    winter_df.loc[:,['participants_m', 'participants_f']].hist()

    # Show the plots
    plt.show()


def boxplot(df):
    """"
    Generates a boxplot 

    Parameters:
            df (DataFrame): pandas dataframe with event data
 
        Returns:
            boxplots of relevant columns in the dataframe

    """
    
    # Create a boxplot of the DataFrame
    df.plot.box(subplots = True, sharey = False)
    # df.boxplot(subplots = True, sharey = False)       # pd.boxplot doesn't work with the parameters subplots or sharey.

    # acknowledge duration outlier
    print(df[['host','duration']])      # host has two names as paralympics were set in two locations

    # save to png image file
    plt.savefig('bp_example.png')
    
    # Show the plots
    plt.show()      # last command as it is a blocking function; pauses execution of script


def main():
    """"
    Main logic for the program
    Reads the provided databases into DataFrame format    
    """
    try:
        events_prepared_csv = Path(__file__).parent / 'tutorialpkg' / 'data' /'paralympics_events_prepared.csv'
        df_events = pd.read_csv(events_prepared_csv)                                                      # read csv file into DataFrame
    except FileNotFoundError as e:
        print(f"CSV file not found. Please check the file path. Error: {e}")
        exit()

    # calls functions to plot figures relevant to the database 
    # histogram(df_events)
    boxplot(df_events)

    return

if __name__ == "__main__":
    main()