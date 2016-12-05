"""
This python script loads NOAA data for Project Sunshine (W205 Final Project).
Before running this script please be sure that you have run setup.py to start
the postgres tables into which we'll put this data.

To run this script from the command line use:
    python data_ingest_noaa.py
Or
    python data_ingest_noaa.py verbose
"""

# General Imports
from __future__ import absolute_import, print_function, unicode_literals
import os
import sys
import requests
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

# Global Variables
STATIONS_URL = 'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/stations.tsv'

# Helper function to get url for individual months
def get_noaa_url(state, location, vector):
    """ Function output a url given state, location & vector of a station."""
    base = 'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/monthly01/CRNM0102-'
    station = '_'.join([state, location, vector])
    return base + station.replace(' ','_') + '.txt'

# Helper Function to get a list of WBAN stations in the postgres table
def get_stations_from_postgres():
    """ Function reads wban_id, state, location and vector from postgres."""
    conn = psycopg2.connect(database='solarenergy', user='postgres',
                            password='pass', host='localhost', port='5432')
    cur = conn.cursor()
    cur.execute("SELECT wban_id, state, location, vector from weather_stations")
    stations = cur.fetchall()
    conn.commit()
    return stations

# Helper Function to get list of column names for monthly files
def get_monthly_data_header():
    url = 'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/monthly01/HEADERS.txt'
    headers = requests.get(url)
    return headers.text.split('\n')[1].split()

# Main functions to E - T - L NOAA Weather Data
def load_stations_table(verbose=False):
    """ Function to load stations information into postgres table."""
    # load USCERN stations indexed by their WBAN ID numbers
    stations_df = pd.read_csv(STATIONS_URL, sep = '\t', header=0, index_col = 'WBAN')

    # select the columns that we'll use & rename them to fit the postgres table
    cols = ['NAME','LOCATION','VECTOR','STATE','LATITUDE','LONGITUDE','ELEVATION']
    stations_df = stations_df[cols]
    stations_df.index.names = ['wban_id']
    stations_df = stations_df.rename(index=str, columns={c:c.lower() for c in cols})

    # remove duplicate rows
    stations_df = stations_df[-stations_df.duplicated()]

    # communicate progress
    if verbose:
        print("... %s stations' loaded from NOAA" % (len(stations_df)))

    # use a sql engine with psycopg2 to load the df into postgres
    db_loc = 'postgresql+psycopg2://postgres:pass@localhost:5432/solarenergy'
    engine = create_engine(db_loc)
    stations_df.to_sql("weather_stations", engine, if_exists='append')

def load_monthly_data(verbose=False):
    """ Function to load monthly weather data into postgres table."""
    # pull station information from postgres
    stations = get_stations_from_postgres()

    # selecting only the columns we want for postgres table
    cnames = get_monthly_data_header()
    newcolnames = {'WBANNO':'wban_id', 'LST_YRMO':'month', 'T_MONTHLY_MAX':'max_temp',
            'T_MONTHLY_MIN':'min_temp', 'T_MONTHLY_MEAN':'mean_temp',
            'P_MONTHLY_CALC':'precipitation', 'SOLRAD_MONTHLY_AVG':'solar_radiation'}
    usecols = [str(c) for c in newcolnames.keys()] 

    # connect to database using sql alchemy engine
    db_loc = 'postgresql+psycopg2://postgres:pass@localhost:5432/solarenergy'
    engine = create_engine(db_loc)

    # iterate through stations
    for wban_tup in stations:
        url = get_noaa_url(*wban_tup[1:])
        df = []
        # load monthly data (if it exits)
        try:
            df = pd.read_csv(url, sep = '\s+', header=None, index_col = 'WBANNO',
                                names=cnames, usecols=usecols)
        except Exception, e:
            if verbose:
                print('... failed to load %s' %(wban_tup[0]))
                print('... ERROR:', e)
        # put data into postgres (if it exists)
        if len(df) > 0:
            df.index.names = ['wban_id']
            df = df.rename(index=str, columns=newcolnames)
            df.to_sql("uscrn_monthly", engine, if_exists='append')
            if verbose:
                print('...loaded %s rows from station %s' %(len(df), wban_tup[0]))

# command line instructions
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1].lower() == 'verbose':
        verbose = True
    else:
        verbose = False

    # load stations
    load_stations_table(verbose)

    # load monthly data
    load_monthly_data(verbose)
