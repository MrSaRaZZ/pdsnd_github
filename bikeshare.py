################################################################################################################
##
##  Description..: US Bike Share Data Analysis program
##  Author.......: Ben Saragozza
##  Date.........: 15th July 2020
##  GitHub Repo..: https://github.com/MrSaRaZZ/pdsnd_github
##
################################################################################################################

import time
import datetime
import pandas as pd
import numpy as np

# Set is_debug flag to display some helpfull print statements, which may help with development and finding some errors!
is_debug = 0

# Set-up some dictionary helpers
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
          'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12}

DAY_OF_WEEK = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}


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
        try:    
            city = input("Please enter your preferred city 'chicago', 'new york city' or 'washington': ")
            if city.lower() not in CITY_DATA:
                print("Invalid city, only 3 cities are currently supported 'chicago', 'new york city' or 'washington'.")
                continue
            else:
                break
        except Exception as e:
            print("An exception has occured: {}".format(e))

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter a single month to filter by or enter the keyword all (eg: all, january, february, ... , june): ")
            if (month.title() in MONTHS) or (month.title() == 'All'):
                break
            else:
                print("Invalid month, please enter the full month name eg: 'january', or 'all' if you want to view all months.")
                continue
        except Exception as e:
            print("An exception has occured: {}".format(e))
        

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Please enter a single day of the week to filter by or enter the keyword all (eg: all, monday, tuesday, ... , sunday): ")
            if (day.title() in DAY_OF_WEEK) or (day.title() == 'All'):
                break
            else:
                print("Invalid day of week, please enter the full day of week name eg: 'monday', or 'all' if you want to view all days of the week.")
                continue
        except Exception as e:
            print("An exception has occured: {}".format(e))

    print('-'*40)
    
    print("You have entered the following filters:")
    print('\nCity...: {}\nMonth..: {}\nDay....: {}\n'.format(city.title(), month.title(), day.title()))
    print("-"*40)
    
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
    
    try:
        filename = CITY_DATA.get(city, 'NO_CITY_KEY_FOUND')
        if filename != 'NO_CITY_KEY_FOUND':
            df = pd.read_csv('./{}'.format(filename))
            
            # Apply month filter
            if month.title() != 'All':
                month_number = MONTHS.get(month.title(), 'NO_MONTH_KEY_FOUND')
                if month_number != 'NO_MONTH_KEY_FOUND':
                    df['Start Time'] = pd.to_datetime(df['Start Time'])  # Convert 'Start Time' column to date time
                    df = df[df['Start Time'].dt.month == month_number]
                else:
                    print("Something has gone wrong with the month filter.")

            # Apply day of week filter
            if day.title() != 'All':
                day_number = DAY_OF_WEEK.get(day.title(), 'NO_DAY_KEY_FOUND')
                if day_number != 'NO_DAY_KEY_FOUND':
                    df['Day Of Week'] = df['Start Time'].dt.day_name() # Add a new column with the day name in it
                    df = df[df['Day Of Week'] == day.title()]
                else:
                    print("Something has gone wrong with the day filter.")

        else:
            print('Filename could not be found for the city specified')
    
    except Exception as e:
            print("An exception has occured: {}".format(e))
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])  # Convert 'Start Time' column to date time to use dt accessor methods

    # display the most common month
    df['Month'] = df['Start Time'].dt.month_name()
    popular_month = df['Month'].value_counts().nlargest(1)
    print("Most frequent travel month is {}, with {} instances.".format(popular_month.index[0], popular_month.iloc[0]))

    # display the most common day of week
    df['Day Of Week'] = df['Start Time'].dt.day_name()
    popular_day = df['Day Of Week'].value_counts().nlargest(1)
    print("Most frequent travel day of week is {}, with {} instances.".format(popular_day.index[0], popular_day.iloc[0]))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour                
    popular_hour = df['Hour'].value_counts().nlargest(1) 
    print("Most frequent travel start hour is {}, with {} instances.".format(popular_hour.index[0], popular_hour.iloc[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    if is_debug: print("HEAD:\n", df.head(5))



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    top_x = 5 # Change for top x number i.e. 5 for top 5

    # display most commonly used start station
    popular_start = df['Start Station'].value_counts().nlargest(top_x)
    print("The top {} most popular start stations are: ".format(top_x))
    for i in range(len(popular_start)):
        print("  {}. {}, with {} instances.".format(i+1, popular_start.index[i], popular_start.iloc[i]))

    # display most commonly used end station
    popular_end = df['End Station'].value_counts().nlargest(top_x)
    print("\nThe top {} most popular end stations are: ".format(top_x))
    for i in range(len(popular_end)):
        print("  {}. {}, with {} instances.".format(i+1, popular_end.index[i], popular_end.iloc[i]))
    
    # display most frequent combination of start station and end station trip
    popular_trip = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Counts')
    popular_trip = popular_trip.sort_values(by='Counts', ascending=False).head(1)

    print("\nMost frequent start and end station combination is:")
    print("  Start......: {}".format(popular_trip['Start Station'].iloc[0]))
    print("  End........: {}".format(popular_trip['End Station'].iloc[0]))
    print("  Instances..: {}".format(popular_trip['Counts'].iloc[0]))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("Total travel time is..: {:.0f} seconds (or {}).".format(df['Trip Duration'].sum(), datetime.timedelta(seconds=float(df['Trip Duration'].sum()))))
   
    # display mean travel time
    print("Mean travel time is...: {:.2f} seconds (or {}).".format(df['Trip Duration'].mean(),datetime.timedelta(seconds=float(df['Trip Duration'].mean()))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...')
    start_time = time.time()

    # Display counts of user types
    print()
    if 'User Type' in df.columns:
        df_user_types = df['User Type'].value_counts()
        for i in range(len(df_user_types)):
            print("User type {}, has {} instances.".format(df_user_types.index[i], df_user_types.iloc[i]))
    else:
        print("Sorry but no 'User Type' column was found in the dataset.")

    # Display counts of gender
    print()
    if 'Gender' in df.columns:
        df_genders = df['Gender'].value_counts()
        for i in range(len(df_genders)):
            print("User gender {}, has {} instances.".format(df_genders.index[i], df_genders.iloc[i]))
    else:
        print("Sorry but no 'Gender' column was found in the dataset.")

    # Display earliest, most recent, and most common year of birth
    print()
    if 'Birth Year' in df.columns:
        df_birth_year = df['Birth Year'].value_counts().nlargest(1)
        print("The earliest birth year is {:.0f}.".format(df['Birth Year'].min()))
        print("The most recent birth year is {:.0f}.".format(df['Birth Year'].max()))
        print("The most common year of birth is {:.0f}, with {} instances.".format(df_birth_year.index[0], df_birth_year.iloc[0]))

    else:
        print("Sorry but no 'Birth Year' column was found in the dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



    
def basic_stats(df):
    """Displays basic statistics on bikeshare users."""

    print('\nCalculating Basic Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Size: {}\n".format(df.size))
    print("Head: {}\n".format(df.head(10)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        if is_debug: basic_stats(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Provide user with the option to view X rows of data at a time from the data frame.
        show_x_rows = 10
        show_count = 1
        show_data = input("\nWould you like to see {} rows of raw data? Enter yes or no.\n".format(show_x_rows))
        while True:
            if show_data.lower() == "yes":
                print(df.head(show_count * show_x_rows))
                show_data = input("\nWould you like to add another {} rows? Enter yes or no.\n".format(show_x_rows))
                show_count += 1
                continue
            else:
                break

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break



if __name__ == "__main__":
	main()
