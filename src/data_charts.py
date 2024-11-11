import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# set display options for pandas
pd.set_option("display.max_columns", None)


def histogram(df, columns = None, type = None):
    """"
    Generates a histogram for each column of the dataset
    Generates a histogram for each of the specified columns 'participants_m' and 'participants_f'

    Parameters:
            df (DataFrame): pandas dataframe with event data
 
    Returns:
        histograms of relevant columns in the dataframe
    """

    # Create a histogram of the DataFrame with the specified conditions
    if columns and type:        # create a histogram of the specified columns only, one for each season
        for season in type:
            df_season = df[df['type'] == season]
            df_season[columns].hist()
    elif columns:         # create a histogram of the specified columns only; works due to truthiness of non-empty list
        df[columns].hist()
    else:       # create a histogram of the whole dataframe
        df.hist()
    
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
    # plt.savefig('bp_example.png')
    
    # Show the plots
    plt.show()      # last command as it is a blocking function; pauses execution of script

def timeseries(df):
    """"
    Generates a timeseries line chart 

    Parameters:
            df (DataFrame): pandas dataframe with event data
 
    Returns:
        boxplots of relevant columns in the dataframe
    """

    # sort values by date order
    df = df.sort_values(by='start')

    # Create a lineplot of participants over time
    df.plot(x='start' , y='participants', xlabel='Date', ylabel='# of participants', legend=False)
    # create separate lineplots for winter and summer events
    df.groupby('type').plot(x='start' , y='participants', xlabel='Date', ylabel='# of participants', legend=False)

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

    ### calls functions to plot figures relevant to the database 
    ##  calls histogram function
    # histogram(df_events)
    ## calls histogram for specified columns
    participant_columns = ['participants_m', 'participants_f']
    # histogram(df_events, participant_columns)
    ## calls histogram for specified columns and type
    seasons = ['summer', 'winter']
    # histogram(df_events, participant_columns, seasons)

    # calls boxplot function
    # boxplot(df_events)

    # calls timeseries function
    timeseries(df_events)


    return

if __name__ == "__main__":
    main()