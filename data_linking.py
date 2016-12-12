#!/usr/bin/env python
"""
MIDS W205, Fall 2016, Final Project -- Team Sunshine

This file contains a script to link solar locations with weather stations
using geographic distance. The script assumes that you have already performed
all ingest steps.

To run this script from the command line use:
    python data_linking.py
Or
    python data_linking.py verbose
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import sys
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine
import vincenty


#  Defining Functions to modularize data linkage script
def get_locations(verbose=False):
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
    solar_df = pd.read_sql(query, engine, index_col = 'loc_id')
    if verbose:
        print('... loaded locations for %s solar locations' % (len(solar_df)))

    # get weather locations
    query = """
            SELECT DISTINCT wban_id,
            CAST(latitude as decimal) AS latitude,
            CAST(longitude as decimal) AS longitude
            FROM weather_stations
            """
    uscrn_df = pd.read_sql(query, engine, index_col = 'wban_id')
    if verbose:
        print('... loaded locations for %s uscrn stations' % (len(uscrn_df)))

    return solar_df, uscrn_df


def find_closest_station(solar_loc, uscrn_df):
    """
    This is a helper function to find the closest weather station
    given solar location and a dataframe with weather station locations.
    """
    # start from subset of stations w.in a small radius
    neighbors =  uscrn_df[0:0]
    radius = 1
    while len(neighbors) == 0:
        # range of lat/long to search
        xmin, xmax = solar_loc[0] - radius, solar_loc[0] + radius
        ymin, ymax = solar_loc[1] - radius, solar_loc[1] + radius

        # pull stations in that range
        lat_r = (uscrn_df.latitude>=xmin)&(uscrn_df.latitude<=xmax)
        long_r = (uscrn_df.longitude>=ymin)&(uscrn_df.longitude<=ymax)
        neighbors = uscrn_df[lat_r & long_r]
        radius += 1

    # find closest neighbor
    closest_station = None
    dist_to_closest_station = np.inf
    for wban_id, (lat, lng) in neighbors.iterrows():
        dist = vincenty.vincenty((lat, lng), solar_loc)
        if dist < dist_to_closest_station:
            dist_to_closest_station = dist
            closest_station = wban_id

    return closest_station, dist_to_closest_station


def create_closest_station_df(solar_df, uscrn_df):
    """
    This function creates a new dataframe whose index are location ids
    and whose columns are wban_id and distance (of the closest station).
    """
    # iterate through solar locations to get closest station
    temp_lst=[]
    for loc_id, solar_loc in solar_df.iterrows():
        wban_id, distance = find_closest_station(solar_loc, uscrn_df)
        temp_lst.append([loc_id,wban_id, distance])

    # put results in a data frame
    cols = ['loc_id', 'wban_id','distance']
    closest_stations_df = pd.DataFrame(temp_lst, columns=cols)
    closest_stations_df = closest_stations_df.set_index('loc_id')
    return closest_stations_df


def load_to_postgres(closest_stations_df, verbose=False):
    """
    This function loads the input dataframe to a postgres table
    called closest_stations.
    """
    # Set up connection to postgres tables
    db_loc = 'postgresql+psycopg2://teamsunshinedemo:oscarisawesome123'
    db_loc += '@teamsunshinedemo.coga7nzsvf0h.us-east-1.rds.amazonaws.com:'
    db_loc += '5432/solarenergy'
    engine = create_engine(db_loc)

    # load table
    closest_stations_df.to_sql("closest_stations", engine, if_exists='replace')
    if verbose:
        print('... loaded closest_stations table to serving layer DB.')


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
