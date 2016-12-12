#!/usr/bin/env python
"""
This file contains a script to run a regression on the solar data and
predict year end and month end solar totals.

MIDS W205, Fall 2016, Final Project
Team Sunshine
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
import pandas as pd
from sklearn import linear_model
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# Defining functions to modularize setup script.
def get_monthly_data():
    """
    This function connects to the postgres DB to pull weather data
    corresponding to each solar location and month.
    """
    # Set up connection to postgres tables
    db_loc = 'postgresql+psycopg2://teamsunshinedemo:oscarisawesome123'
    db_loc += '@teamsunshinedemo.coga7nzsvf0h.us-east-1.rds.amazonaws.com:'
    db_loc += '5432/solarenergy'
    engine = create_engine(db_loc)

    # get weather data
    query = """
            SELECT solar_fields.loc_id, full_date,
            CAST(solar_fields.latitude as decimal) as lat,
            CAST(solar_fields.longitude as decimal) as long,
            CAST(solar_radiation as decimal) as solar_radiation, mwh,
            FROM(
                (SELECT loc_id, wban_id, full_date, latitude, longitude,
                CAST(mwh as decimal) AS mwh,
                FROM generation JOIN closest_station
                ON generation.loc_id=closest_station.loc_id)
                ) AS solar_fields
            LEFT JOIN uscrn_monthly
            ON solar_fields.wban_id=uscrn_monthly.wban_id
            AND solar_fields.full_date=uscrn_monthly.month
            """
    data_df = pd.read_sql(query, engine, index_col = 'loc_id')

    return data_df

def data_cleaning(data_df):
    """
    This function takes a dataframe with full_date, lat, long and
    solar_radiation, splits out the month and recodes na
    values in solar radiation.
    """
    # making all types numeric and coding missing values as nan
    data_df['year'] = data_df.apply(lambda x: int(x['full_date'][:4]), axis=1)
    data_df['month'] = data_df.apply(lambda x: int(x['full_date'][4:]), axis=1)
    del df['full_date']
    data_df['solar_radiation'] = data_df.solar_radiation.fillna(-9999)
    return df

def predict_monthly_mwh(clean_df):
    """
    Function to run a regression on the relationship between solar radiation
    levels and energy production from solar field locations. The function
    returns a new df with weather data and predictions for each solar location.

    NOTE: in future versions of this architecture this regression could be
    used as a prediction tool for locations that don't yet have solar fields.
    For that, we'd want to add additional weather variables. For now we'll
    simply explore this relationship to better inform our audience.
    """
    # remove nans
    missing = clean_df.isnan(clean_df).any(axis=1)
    monthly_pred_df = clean_df[~missing]

    # selecting cols for regression
    cols=['solar_radiation','month','lat']
    X = monthly_pred_df.as_matrix(columns=cols)
    y = np.array(monthly_pred_df.mwh)

    # create and fit model
    lm = linear_model.LinearRegression()
    lm.fit(X, y)

    # add predicted values to a new dataframe column
    monthly_pred_df['predicted_mwh'] = lm.predict(X)

    # return the model for future use and predictions for serving layer
    return lm, monthly_pred_df

def forcast_yearend_mwh(clean_df):
    """
    Given a train_df with with loc_id, year, month, and mwh,
    this function returns a df with the loc_id and a year end forcast of
    total energy generated at that location.
    """
    # separate out this year's data
    current_year = max(clean_df.year)
    current_df = clean_df[clean_df.year == current_year]
    current_month = current_df.groupby('loc_id').max()['month']
    current_mwh = current_df.groupby('loc_id').sum()['mwh']

    # how does this compare to last year at this time?
    last_year = clean_df[clean_df.year == current_year - 1]
    this_time_last_year = last_year[last_year.month <= current_month]
    totals = last_year.groupby('loc_id').sum()
    partials = this_time_last_year.groupby('loc_id')
    percent = totals / partials

    # forcast = current total * percent
    forcast_df = current_mwh * percent
    return forcast_df


def load_to_postgres(monthly_pred_df, curr_year_forcast_df, verbose=False):
    """
    This function loads the input dataframe to a postgres table
    called predicted energy production.
    """
    # Set up connection to postgres tables
    db_loc = 'postgresql+psycopg2://teamsunshinedemo:oscarisawesome123'
    db_loc += '@teamsunshinedemo.coga7nzsvf0h.us-east-1.rds.amazonaws.com:'
    db_loc += '5432/solarenergy'
    engine = create_engine(db_loc)

    # load
    monthly_pred_df.to_sql("monthly_predictions", engine, if_exists='replace')
    if verbose:
        print('... loaded predictions table to serving layer DB.')


# Main script to be run at the command line
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'verbose':
        verbose = True
    else:
        verbose = False
    # call functions
    solar_df, uscrn_df = get_locations(verbose)
    closest_stations_df = create_closest_station_df(solar_df, uscrn_df)
    load_to_postgres(closest_stations_df, verbose)
