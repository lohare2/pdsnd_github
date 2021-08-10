import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    valid_city = ['c','n','w'] 
    valid_mth = list(range(0,13))
    valid_dow = list(range(0,8))
    
    while True:
        city = input("which city would you like to explore - type c for chicago, n for new-york or w for washington")
        month = int(input("which month do you want to filter by - type as integer 1 for Jan, 2 for Feb ... 12 for Dec or 0 for ALL"))
        day =  int(input("which day of the week do you want to filter by - type as integer 1 for Sunday, 2 for Monday ... 7 for Saturday or 0 for ALL"))       
                   
        if((city in valid_city) and (month in valid_mth) and (day in valid_dow)):
            print("Thanks for entering valid data")
            break
        else:
            print("you did not enter valid data please try again")
        
    print('Hello! Let\'s explore some US bikeshare data!')
    return city, month, day


def load_data(c, m, d):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    global selected_city
    selected_city = c    
    
    if(c == 'w'):
        df = pd.read_csv("washington.csv", na_values=' ')
    elif(c == 'n'):
        df = pd.read_csv("new_york_city.csv", na_values=' ')
    elif(c == 'c'):
        df = pd.read_csv("chicago.csv", na_values=' ')

    print (df.dtypes) 
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
        
    if(m == 0 and d == 0):
        # no filter  needed
        return df
    elif(m == 0 and d != 0):
        # filter by day
        df = df[df['Start Time'].dt.day == d]
        return df
    elif(m != 0 and d == 0):
        #filter by month
        df = df[df['Start Time'].dt.month == m]
        return df
    elif(m != 0 and d != 0):
        #filter by month and day
        df = df[df['Start Time'].dt.month == m]
        df = df[df['Start Time'].dt.day == d]
        return df
    
def time_stats(df):
    """Displays trip time statistics"""
    start_time = time.time()
    
    print('\nCalculating The shortest journey time...\n')
    print(df['Trip Duration'].min())
    
    print('\nCalculating The longest journey time...\n')
    print(df['Trip Duration'].max())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    start_time = time.time()
    
    print('\nCalculating The Number of departures per station..\n')
    print(df.groupby('Start Station')['Start Station'].count())

    print('\nCalculating The Most commonly used start station.\n')
    print(df['Start Station'].value_counts().idxmax())
    
    print('\nCalculating The Least commonly used start station.\n')
    print(df['Start Station'].value_counts().idxmin())
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_minutes = df['Trip Duration'].sum()
    
    # Get hours with floor division
    hours = total_minutes // 60

    # Get additional minutes with modulus
    minutes = total_minutes % 60

    time_string = "{}:{}".format(hours, minutes)
    print("Total trip Duration hrs: mins: ", time_string)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User Type Stats:', df.groupby('User Type')['User Type'].count())

    # washington has no user stats so return 
    if(selected_city == 'w'):
        return 0

    print('if w shoudl not be here')
    # Display counts of gender 
    print('Gender Stats:', df.groupby('Gender')['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    print('Birth Year stats:', 'Youngest:', int(df['Birth Year'].min()), 'Oldest:', int(df['Birth Year'].max()), 'Most Common: ', int(df['Birth Year'].value_counts().idxmax()))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# main method prompt for input repeat
def main():
    while True:
        print(CITY_DATA)
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
