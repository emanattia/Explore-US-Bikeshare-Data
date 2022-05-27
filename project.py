# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 19:27:45 2021

@author: a
"""


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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Which city would you like to explore? (New York City, Chicago or Washington)\n")
        city=city.lower()
        if city not in ('new york city', 'chicago', 'washington'):
            print("Invalid Input, please try again.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month would you like to explore? (all, January, February, ... , June)\n")
        month=month.capitalize()
        #print (month)
        if month not in ('All','January', 'February', 'March', 'April', 'May', 'June'):
            print("Invalid Input, please try again.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day would you like to know more about? (all, Monday, Tuesday, ... Sunday)\n")
        day=day.capitalize()
        if day not in ('All','Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'):
            print("Invalid Input, please try again.")
            continue
        else:
            break
    

    print('-'*40)
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
    
    #load data in df
    df=pd.read_csv(CITY_DATA[city])
    
    #convert the data type of Start Time column to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #create new column contain the month
    df['month'] = df['Start Time'].dt.month_name()
    
    #create new column contain the week day
    df['day'] = df['Start Time'].dt.day_name()
    
    #filter the data by month
    if month !='All':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        for x in months:
            if x==month:
                #df=df[df['month']=month]
                df = df[df.month == month]
                
    #filter by the day
    if day != 'All':
        df = df[df.day == day]
        
    print("Done!!")

    return df

def time_stats(df,day,month):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'All':
        most_common_month=df['month'].dropna().mode()[0]
        print ('The most common month to start is :', most_common_month)
    else:
        print('enter All in months to get the most common month instead of {}'.format(month))

    # display the most common day of week
    if day == 'All':
        most_common_day=df['day'].dropna().mode()[0]
        print ('The most common day to start is :', most_common_day)
    else:
        print('enter All in day of the week to get the most common day instead of{}'.format(day))
        
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('The most common hour to start is :', most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start= df['Start Station'].value_counts().idxmax()
    print('Most Commonly used start station:', common_start)

    # display most commonly used end station
    common_end= df['End Station'].value_counts().idxmax()
    print('\nMost Commonly used end station:', common_end)

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).idxmax()
    print('The most commonly used combination of start station and end station trip:', combination)
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)  

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time:', mean_travel_time/60, " Minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('counts of user types:\n', user_types)

    # Display counts of gender
    try:
        gender_types = df['Gender'].value_counts()
        print('counts of gender:\n', gender_types)    
    except:
        print('counts of gender:\n,There is No gender data avaliable for Tihs city')

    # Display earliest, most recent, and most common year of birth
    
    #earliest year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        print('\nEarliest year:', earliest_birth)
        
        #most recent year of birth
        most_recent_year = df['Birth Year'].max()
        print('\nMost recent year:', most_recent_year)
        
        #most common year of birth
        most_common_year = df['Birth Year'].value_counts().idxmax()
        print('\nMost common year:', most_common_year)
    except:
        print('counts of gender:\n,There is No year of birth data avaliable for Tihs city')
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    # Ask user if they want to display a rows of data.
    start_data = 0
    end_data = 5
    df_length = len(df.index)
    
    while start_data < df_length:
        data_row = input("\nWould you like to see some rows of the data? Enter 'yes' or 'no'.\n")
        data_row=data_row.lower()
        if data_row == 'yes':
            print("\nDisplaying only 5 rows of data.\n")
            if end_data > df_length:
                end_data = df_length
            print(df.iloc[start_data:end_data])
            start_data += 5
            end_data += 5
        else:
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        show_data(df)
        time_stats(df,day,month)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()