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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("\n\nPlease input the city you want to check the data for:").lower()
    while (city not in CITY_DATA):
        print ("\nWhoops! You entered an incorrect city... Please choose one from chicago, new york city, washington\n")
        city = input("\nPlease input the city you want the data for: ").lower()
        
    filter_option=input("\nAwesome! Thank you. Now, Would you like to filter by month or day or all? \n").lower()
    if (filter_option=='month'):
    # TO DO: get user input for month (all, january, february, ... , june)
        month = input("\nAlrighty then! Let's get you data by month:  ").lower()
        months=['january','february','march','april','may','june']
        day='all'
        while (month not in months):
            print ("\nWhoops! You entered a month we have no data about... Please choose from Jan-June: ")
            month = input("\nPlease enter the month").lower()
    elif (filter_option=='day'):
        day = input("\nAlrighty then! Let's get you data by day of week: ").lower()
        days_of_week=['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        month='all'
        while (day not in days_of_week):
            print ("\nWhoops! Looks like there's a mistake. ")
            day = input("\nPlease enter a day of week: ").lower()
    elif (filter_option=='all'):
        month = input("\nSure. We will filter by both.Please enter a month between Jan-June: ").lower()
        months=['january','february','march','april','may','june']
        while (month not in months):
            print ("\nWhoops! You entered a month we have no data about... Please choose from Jan-June")
            month = input("\nPlease enter a month: \n").lower()
        day = input("\nCool. Now, Enter a day: ").lower()
        days_of_week=['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        while (day not in days_of_week):
            print ("\nWhoops! Looks like there's a mistake. ")
            day = input("\nPlease enter a day: ").lower()
    else:
        filter1= input("Hmmm.. Looks like there's a mistake. No worries. Let's try it again. Would you like to filter by month, day or all?\n")
        

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)


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
        df - pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month']=df['Start Time'].dt.month_name()
    
    common_month = df['month'].mode().max()
    print('Most commom month: ',common_month)

    # TO DO: display the most common day of week
    df['days_of_week']=df['Start Time'].dt.weekday_name
    common_day_of_week = df['days_of_week'].mode().max()
    print('Most commom day of week: ',common_day_of_week)

    # TO DO: display the most common start hour
    df['hour']=df['Start Time'].dt.hour
    common_hour = df['hour'].mode().max()
    print('Most common hour: ',common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode().max()
    print('Most commonly used start station: ',common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode().max()
    print('Most commonly used end station: ',common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['Start Stop Combo'] = df['Start Station']+" || "+ df['End Station']
    common_start_stop_combo=df['Start Stop Combo'].value_counts().idxmax()
    print('Most frequent combination of start station and end station trip: ',common_start_stop_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_time(seconds, granularity=2):
    intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time=[]
    # TO DO: display total travel time
    total_travel_time_df= df['Trip Duration'].sum()
    total_travel_time = display_time(total_travel_time_df)
    print ("Total travel time = {}".format(total_travel_time))
    # TO DO: display mean travel time
    mean_travel_time_df= df['Trip Duration'].mean()
    mean_travel_time = display_time(mean_travel_time_df)
    print ("Mean travel time = {}".format(mean_travel_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def age(year):
	"""This function gives the age of the customer"""
    return(int((pd.datetime.now().year)-year))

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nUser Types and their counts:\n",user_types)

    # TO DO: Display counts of gender
    if (city!='washington'):
        gender = df['Gender'].value_counts()
        print("\n\nGender and their counts:\n",gender)

    # TO DO: Display earliest, most recent, and most common year of birth
        print("\nDifferent age group of users using this bike share :")
        oldest_age=age(df['Birth Year'].min())
        youngest_age=age(df['Birth Year'].max())
        average_age=age(df['Birth Year'].mean())
        common_birth_year=int(df['Birth Year'].value_counts().max())
        print("Oldest User is {}".format(oldest_age))
        print("Youngest User is {}".format(youngest_age))
        print("Average age of Users is {}".format(average_age))
        print("\n\nMost common year of birth is {}".format(common_birth_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
def display_data(df):
	 """Displays individual data"""
    individual_data = input('\nWould you like to see individual data? Enter yes or no.\n')
    start=0
    end=5
    while (individual_data.lower()=='yes'):

        print(df.iloc[start:end,3:9])
        start+=5
        end+=5
        individual_data = input('\nWould you like to see more individual data? Enter yes or no.\n')

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
