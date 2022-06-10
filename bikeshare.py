import time
import pandas as pd
import numpy as np

"""

This python program analyzes travel patterns of shared bikes in three major US cities

"""


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input("Would you like to see data for Chicago. New York City or Washington?").lower()
        if city not in CITY_DATA.keys():
            print("Invalid Input. Please only chose from the list")
        else:
            break

    date_filter = input('Would you like to filter the data by month, day, or "none" for no time filter.').lower()
    month = ""
    day = ""
    if date_filter == "month":
        month = input("Which month - January, February, March, April, May, or June?").lower()
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?").lower()
    elif date_filter == "day":
        month = 'all'
        day = input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?").lower()
    elif date_filter == "none":
        month = 'all'
        day = 'all'
    else:
        print("Invalid answer. Please try again")

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print(f"The most popular month is: {popular_month}")

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print(f"The most popular day of the week is: {popular_day}")

    # TO DO: display the most common start hour

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]
    print(f"The most popular start hour is: {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"The most commonly used start station is: {common_start_station}")

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"\nThe most commonly used end station is: {common_end_station}")

    # TO DO: display most frequent combination of start station and end station trip
    df['Start And End'] = df['Start Station'].str.cat(df['End Station'], sep=' and ')
    start_end = df['Start And End'].mode()[0]
    print(f"\nThe most frequent combination of start and end stations are: {start_end}.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

    # TO DO: display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    min, sec = divmod(average_duration, 60)
    print(f"\nThe average trip duration is {min} minutes and {sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print(f"Types of User: \n{user_type}\n")

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"Gender Breakdown: \n{gender}\n")
    except:
        print("\nThere is no 'Gender' column in this file.")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"The earliest year of birth is: {earliest}\n")
        print(f"The most recent year of birth is: {recent}\n")
        print(f"The most common year of birth is: {common_year}")
    except:
        print("There are no birth year details in this file.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)

def display_data(df):

    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no: ").lower()
    start_loc =0
    if view_data == "yes":
        print(df.head())
    else:
        print("Continuing to summary stats")

    while view_data == "yes":
        more_data = input("Do you wish to view more raw data? Enter yes or no: ")
        start_loc += 5
        if more_data == "yes":
            print(df[start_loc:start_loc+5])
        else:
            print("Continuing to summary stats")
            break
    print('-' * 40)

#Main function to call all the previous functions

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()
