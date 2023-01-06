import datetime as dt
import pandas as pd
import time

#             LOCATING THE DATA [ Please make sure all data has been downloaded from github source]

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# SELECTING WHAT DATA SET TO LOAD AND WHICH FILTERS TO APPLY

def get_filters():
    month = ''
    day = ''
    # GETTING AND CHECKING THE INPUT FOR THE CITY SELECTION
    print("Hello! Let's explore some US bikeshare data!")
    city_input = input(
        "Please enter which city you wish to see the data for: Chicago, New York or Washington:\n").lower()

    while city_input.lower() not in ['chicago', 'new york', 'washington']:
        print("Unfortunately we dont have any data on {}".format(city_input))
        city_input = input(
            "Please enter which city you wish to see the data for: Chicago, New York or Washington\n").lower()

    print("Fetching data for {}".format(city_input.title()))
    city = city_input

    # GETTING AND CHECKING THE INPUT FOR FILTER TYPES

    filter_input = input(
        "Please select how you would like to filter the data: month, day, both, or not at all. Please type \"none\" for no time filter:\n").lower()
    filter_input = filter_input

    while filter_input not in ['month', 'day', 'both', 'none']:
        print("Unfortunately the data cannot be filtered by {}".format(filter_input.lower()))
        filter_input = input(
            "Please select how you would like to filter the data: month, day, both, or not at all. Please type \"none\" for no time filter\n").lower()
    else:
        print("Chosen filter: {}".format(filter_input.title()))
        filter = filter_input

# GETTING AND CHECKING THE INPUT FOR MONTH ONLY DATA

    if filter == 'month':
        month_input = input(
            "Please select which month would you like data for: january, february, march, april, may or june\n").lower()
        while month_input not in ['january', 'february', 'march', 'april', 'may', 'june']:
            print("You've entered an invalid response (remember it's only for the first six months). Please try again")
            month_input = input(
                "Please select which month would you like data for: january, february, march, april, may or june\n").lower()
            month_input = month_input.lower()

        print("Filtering data by {}".format(month_input.title()))
        month = month_input
        day = 'all'

    # GETTING AND CHECKING THE INPUT FOR DAY ONLY DATA

    elif filter == 'day':
        day_input = input(
            "Please select which day you would like to data for: monday, tuesday, wednesday, thursday, friday, saturday, sunday\n").lower()
        while day_input not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print("You've entered an invalid response. Please correct your input")
            day_input = input(
                "Please select which day you would like to data for: monday, tuesday, wednesday, thursday, friday, saturday, sunday\n").lower()

        print("Filtering data by {}".format(day_input.title()))
        day = day_input
        month = 'all'

    # GETTING AND CHECKING THE INPUT FOR DAY AND MONTH DATA

    elif filter == 'both':
        month_input = input(
            "Please select which month would you like data for: january, february, march, april, may or june\n").lower()
        while month_input not in ['january', 'february', 'march', 'april', 'may', 'june']:
            print("You've entered an invalid response (remember it's only for the first six months). Please try again")
            month_input = input(
                "Please select which month would you like data for: january, february, march, april, may or june\n").lower()
        month = month_input
        print("{} selected".format(month.title()))

        day_input = input(
            "Please select which day you would like to data for: monday, tuesday, wednesday, thursday, friday, saturday, sunday\n").lower()
        while day_input not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
            print("You've entered an invalid response. Please correct your input")
            day_input = input(
                "Please select which day you would like to data for: monday, tuesday, wednesday, thursday, friday, saturday, sunday\n").lower()
        day = day_input
        print("{} selected".format(day.title()))

        print("Filtering data by {} and {}".format(day.title(), month.title()))
    # SELECTING FILTERS IF NONE CHOSEN
    else:
        print("No time filters applied")
        day = 'all'
        month = 'all'

    print("You've selected the data from {} with the following time filters: month:{}, day:{}.".format(city.title(), month.title(), day.title()))



    print('-'*40)
    return city, month, day

#LOADING THE DATA
def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city], parse_dates=["Start Time", "End Time"])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_of_week
#CHECKING CORRECT MONTH INPUT
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_ser = pd.Series(data=[1, 2, 3, 4, 5, 6], index=months)
        month = month_ser[month]

        df = df[df['month'].values == month]
# CHECKING CORRECT DAY INPUT
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_ser = pd.Series(data=[0, 1, 2, 3, 4, 5, 6], index=days)
    if day != 'all':
        day = day_ser[day]

        df = df[df['day_of_week'].values == day]

    return df

def time_stats(df):

#DISPLAYING USER TIME STATISTICS
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most common month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of the week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most common hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    # DISPLAYING STATION STATISTICS

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    top_start_station = df['Start Station'].mode()[0]
    top_start_station_count = df['Start Station'].value_counts()[df['Start Station'].mode()[0]]
    print("The most commonly used Start Station was {} with {} uses".format(top_start_station, top_start_station_count))

    # display most commonly used end station

    top_end_station = df['End Station'].mode()[0]
    top_end_station_count = df['End Station'].value_counts()[df['End Station'].mode()[0]]
    print("The most commonly used End Station was {} with {} uses".format(top_start_station, top_start_station_count))

    # display most frequent combination of start station and end station trip

    df['route'] = df['Start Station'] + " to " + df['End Station']
    top_route = df['route'].mode()[0]
    top_route_count = df['route'].value_counts()[df['route'].mode()[0]]
    print("The most commonly used route was {} with {} uses".format(top_route, top_route_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):

#DISPLAYING USER ROUTE STATISTICS

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_secs = df['Trip Duration'].sum()

    total_travel_duration = dt.timedelta(seconds=int(total_travel_secs))

    print("In total the bikes were hired for {}".format(total_travel_duration))

    mean_travel_secs = df['Trip Duration'].mean()

    mean_travel_duration = dt.timedelta(seconds=int(mean_travel_secs))

    print("On average our bikes were hired for {}".format(mean_travel_duration))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    # DISPLAYING USER STATISTICS
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    if 'Gender' in df.columns:
        gender_count = df['Gender'].value_counts()
        print("The count of gender for each ride is as follows: ")
        print()
        print(gender_count)
    else:
        print("No gender data available for this dataset")
    print()
    print()

    if 'Birth Year' in df.columns:
        earlist_by = int(df['Birth Year'].min())
        recent_by = int(df['Birth Year'].max())
        common_by = int(df['Birth Year'].mode()[0])
        print(
            "The ago profile of these riders is as follows:\n The oldest rider was born on {}, the youngest rider was born on {}\n and the most common year of birth for our riders was {}".format(
                earlist_by, recent_by, common_by))
    else:
        print("No Brith Year data available for this dataset")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

#PROVIDING OPTION TO SEE RAW DATA

def raw_data(df):
    get_raw_data = input('\nWould you like to see the raw data? Enter yes or no.\n')
    while get_raw_data.lower() not in ['yes', 'no']:
        print("You've entered an invalid response. Please correct your input")
    if get_raw_data.lower() == 'yes':
        count_upper = 5
        count_lower = 0
    while get_raw_data.lower() == 'yes':
        print(df.iloc[count_lower:count_upper])
        count_upper += 5
        count_lower += 5
        get_raw_data = input('\nWould you like to see more raw data? Enter yes or no.\n')
        while get_raw_data.lower() not in ['yes', 'no']:
            print("You've entered an invalid response. Please correct your input")

    print("Ending output of raw data")
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
