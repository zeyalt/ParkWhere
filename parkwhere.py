import numpy as np
import requests
import pandas as pd
from datetime import datetime, timedelta

def parse_date(date_string):
    """Parse a date string in YYYY-MM-DD format as a datetime object."""
    
    return datetime.strptime(date_string, '%Y-%m-%d').date()

def get_ph_and_eve(year='2021'):
    """Return lists of parsed dates for Singapore's public holidays and public holday eves."""
    
    if year == '2021':
        url = 'https://data.gov.sg/api/action/datastore_search?resource_id=550f6e9e-034e-45a7-a003-cf7f7e252c9a&'
    
    elif year == '2022':
        url = 'https://data.gov.sg/api/action/datastore_search?resource_id=04a78f5b-2d12-4695-a6cd-d2b072bc93fe&'
    
    data = requests.get(url).json()
    ph_parsed = [parse_date(ele['date']) for ele in data['result']['records']]
    eve_parsed = [parse_date(ele['date']) - timedelta(days=1) for ele in data['result']['records']]
    
    return ph_parsed, eve_parsed

def extract_all_features(data, year='2021'):
    """Extract all features given a DataFrame containing a datetime string in YYYY-MM-DD HH:MM:SS format."""
    
    df = data.copy()
    # df['date_time'] = pd.to_datetime(df['date_time'], format='%d/%m/%Y %H:%M')
    # df['date_time'] = pd.to_datetime(df['date_time'])

    
    # Create new features from `date_time`
    df['year'] = df['date_time'].dt.year
    df['month'] = df['date_time'].dt.month
    df['day'] = df['date_time'].dt.day
    df['day_of_week'] = df['date_time'].dt.weekday
    df['hour'] = df['date_time'].dt.hour
    df['minute'] = df['date_time'].dt.minute
    df['date'] = df['date_time'].dt.date
    df['time'] = df['date_time'].dt.strftime('%H:%M')
    df['hour_min'] = round(df['hour'] + (df['minute'] / 60), 1)
   
    # Convert `month` to categorical
    df['month'].replace({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
                         7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}, inplace=True)
    df['month'] = df['month'].astype('category') 
    df['month'].cat.set_categories(new_categories=['Jan', 'Feb', 'Mar', 
                                                   'Apr', 'May', 'Jun', 
                                                   'Jul', 'Aug', 'Sep', 
                                                   'Oct', 'Nov', 'Dec'], 
                                   ordered=True, inplace=True)

    # Convert `day_of_week` to categorical
    df['day_of_week'].replace({0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}, inplace=True)
    df['day_of_week'] = df['day_of_week'].astype('category') 
    df['day_of_week'].cat.set_categories(new_categories=['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'], 
                                         ordered=True, inplace=True)

    # Convert `hour` to categorical
    df['hour'] = df['hour'].astype('category') 
    df['hour'].cat.set_categories(new_categories=list(range(24)), ordered=True, inplace=True)

    # Create features for dates of public holidays and public holiday eves
    ph, eve = get_ph_and_eve(year=year)
    df['ph'] = np.where(df['date'].isin(ph), 'ph', '')
    df['eve'] = np.where(df['date'].isin(eve), 'eve', '')
    df['ph_eve'] = df['ph'] + df['eve']
    df['ph_eve'].replace('', 'nil', inplace=True)

    # Select and rearrange columns
    try:
        df = df[['date', 'time', 'month', 'day', 'day_of_week', 'hour', 'minute', 'hour_min', 'ph_eve', 'parking_zone']] 

    except KeyError:
        df = df[['date', 'time', 'month', 'day', 'day_of_week', 'hour', 'minute', 'hour_min', 'ph_eve']] 
          
    return df