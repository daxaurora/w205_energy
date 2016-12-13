#!/usr/bin/env python
"""
This file contains a script to create a master table to facilitate
easy visualization in our serving layer.

MIDS W205, Fall 2016, Final Project
Team Sunshine
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import sys
import numpy as np
import pandas as pd
from sklearn import linear_model
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine


# These two queries create master tables upon which we'll build our visualiztion
def get_master_data():
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
            SELECT generation.loc_id AS loc_id,
                   solar_locations.plant_name AS plant_name,
                   closest_stations.wban_id AS wban_id,
                   weather_stations.name AS station_name,
                   generation.latitude AS g_lat,
                   generation.longitude AS g_lon,
                   weather_stations.latitude AS w_lan,
                   weather_stations.longitude AS w_lon,
                   weather_stations.location AS w_location,
                   weather_stations.state AS w_state,
                   weather_stations.elevation AS w_elevation
            FROM generation
            INNER JOIN solar_locations ON generation.loc_id = solar_locations.loc_id
            INNER JOIN closest_stations ON generation.loc_id = closest_stations.loc_id
            INNER JOIN weather_stations ON weather_stations.wban_id = closest_stations.wban_id
            GROUP BY 1,3,2,4,5,6,7,8,9,10,11
            """
    data_df = pd.read_sql(query, engine, index_col = 'loc_id')
    return data_df

def get_history():
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
            SELECT generation.loc_id AS loc_id,
                CAST(generation.mwh AS decimal) AS mwh,
                CAST(uscrn_monthly.solar_radiation AS decimal) AS solar_radiation,
                CAST(generation.mwh AS decimal)/CAST(uscrn_monthly.solar_radiation AS decimal) AS mwh_per_rad,
                   generation.full_date AS full_date
            FROM generation
            INNER JOIN full_details ON generation.loc_id = full_details.loc_id
            INNER JOIN uscrn_monthly ON uscrn_monthly.wban_id = full_details.wban_id
            AND uscrn_monthly.month = generation.full_date
            WHERE uscrn_monthly.solar_radiation <> '-9999.0'
            GROUP BY 1,2,3,4,5
            """
    data_df = pd.read_sql(query, engine, index_col = 'loc_id')
    return data_df

def get_avg():
    """
    This function connects to the postgres DB to pull aggregate stats.
    """
    # Set up connection to postgres tables
    db_loc = 'postgresql+psycopg2://teamsunshinedemo:oscarisawesome123'
    db_loc += '@teamsunshinedemo.coga7nzsvf0h.us-east-1.rds.amazonaws.com:'
    db_loc += '5432/solarenergy'
    engine = create_engine(db_loc)

    # get weather data
    query = """
            SELECT loc_id,
                   AVG(mwh) AS mwh_avg,
                   SUM(mwh) AS mwh_sum,
                   AVG(solar_radiation) AS sr_avg,
                   SUM(solar_radiation) AS sr_sum,
                   AVG(mwh_per_rad) AS mwh_per_rad_avg,
                   SUM(mwh_per_rad) AS mwh_per_rad_sum,
                   COUNT(DISTINCT full_date)/12 AS years_in_op,
                   MIN(full_date) AS oldest_update,
                   MAX(full_date) AS newest_update
            FROM full_history
            WHERE full_date >'201012'
            GROUP BY loc_id
            HAVING MAX(full_date) > '201606'
            """
    data_df = pd.read_sql(query, engine, index_col = 'loc_id')
    return data_df


def load_to_postgres(data_df, table_name, verbose=False):
    """
    This function loads the input dataframe to a postgres table
    called predicted energy production.
    """
    # Set up connection to postgres tables
    db_loc = 'postgresql+psycopg2://teamsunshinedemo:oscarisawesome123'
    db_loc += '@teamsunshinedemo.coga7nzsvf0h.us-east-1.rds.amazonaws.com:'
    db_loc += '5432/solarenergy'
    engine = create_engine(db_loc)

    # load regression results
    data_df.to_sql(table_name, engine, if_exists='replace')
    if verbose:
        print('... loaded master table "%s" to serving layer DB.'%(table_name))


# Main script to be run at the command line
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'verbose':
        verbose = True
    else:
        verbose = False
    # call functions
    data_df = get_master_data()
    load_to_postgres(data_df, 'full_details', verbose)
    history_df = get_history()
    load_to_postgres(history_df, 'full_history', verbose)
    avg_df = get_avg()
    load_to_postgres(avg_df, 'historic_avg', verbose)
