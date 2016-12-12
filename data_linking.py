#!/usr/bin/env python
"""
This file contains a script to link solar locations with weather stations
using geographic distance.

MIDS W205, Fall 2016, Final Project
Team Sunshine
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
from geopy.distance import vincenty


# fxn to pull solar locations & USCRN locations from Postgres
def get_locations():
    """
    This function connect to the postgres DB to pull locations for
    solar locations and for weather stations. It returns two dataframes.
    """
    # Set up connection to postgres tables
    db_loc = 'postgresql+psycopg2://teamsunshinedemo:oscarisawesome123'
    db_loc += '@teamsunshinedemo.coga7nzsvf0h.us-east-1.rds.amazonaws.com:'
    db_loc += '5432/solarenergy'
    engine = create_engine(db_loc)

    # get solar locations
    query = """
            SELECT DISTINCT loc_id,
            CAST(latitude as decimal) AS latitude,
            CAST(longitude as decimal) AS longitude
            FROM generation
            """
    solar_locations_df = pd.read_sql(query, engine, index_col = 'loc_id')

    # get weather locations
    query = """
            SELECT DISTINCT wban_id,
            CAST(latitude as decimal) AS latitude,
            CAST(longitude as decimal) AS longitude
            FROM weather_stations
            """
    weather_locations_df = pd.read_sql(query, engine, index_col = 'loc_id')

    return solar_locations_df, weather_locations_df

# fxn to id closest station
def find_closest_station(loc_id, solar_df, uscrn_df):
    """
    This is a helper function to find the closest weather station
    given the id of a solar location.
    """
    # store coordinates of solar location
    solar_loc = solar_df.latitude[loc_id], solar_df.longitude[loc_id]

    # stations w.in a small radius
    neighbors =  uscrn_df[uscrn_df.latitude == solar_loc[0] and
                          uscrn_df.longitude == solar_loc[1]]
    radius = 1
    while len(neighbors) == 0:
        # range of lat/long to search
        min_lat, max_lat = solar_lat - radius, solar_lat + radius
        min_long, max_long = solar_long - radius, solar_long + radius

        # pull stations in that range
        lat_r = (uscrn_df.latitude >= min_lat) * (uscrn_df.latitude <= mxn_lat)
        long_r = (uscrn_df.longitude >= min_long) * (uscrn_df.longitude <= max_long)
        neighbors = weather_loc_df[in_lat_range * in_long_range]
        radius += 1

    # find closest neighbor
    closest_station = None
    dist_to_closest_station = np.inf
    for nbr in neighbors.wban_id:
        weather_loc = (uscrn_df.latitude[nbr], uscrn_df.longitude[nbr]
        dist = vincenty(weather_loc, solar_loc)
        if dist < dist_to_closest_station:
            dist_to_closest_station = dist
            closest_station = nbr

    return closest_station, dist_to_closest_station


# fxn to put closest station back into postgres.


# Main script to be run at the command line
if __name__ == '__main__':
    # Prep postgres database and table
    create_database()
    create_tables()
    print("... Created new Postgres database and table for solar energy.")
    # Request the user's API tokens
    credentials = get_user_credentials()
    if credentials:
        filepath = recreate_token_file()
        print("... Empty credentials file created: ", filepath)
        with open(filepath, 'a') as f:
            f.write(credentials)
        print("... Credentials successfully stored.")
        print("... You are now ready to deploy your application.")
    else:
        print("... OK. No credentials stored at this time.")
        print("... Please re-run setup.py to store your credentials before" +
              "deploying your application.")
