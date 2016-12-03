"""
This python script loads NOAA data for Project Sunshine (W205 Final Project).
Before running this script please be sure that you have run setup.py to start
the postgres tables into which we'll put this data.
"""

# General Imports
from __future__ import absolute_import, print_function, unicode_literals
import os
import requests
import numpy as np
import pandas as pd
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy import create_engine

# Global Variables
STATIONS_URL = 'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/stations.tsv'

# Helper function to get url for individual months
def get_noaa_url(wban_id, stations_df):
    """ Function to take a wban number and output a url."""
    base = 'http://www1.ncdc.noaa.gov/pub/data/uscrn/products/monthly01/CRNM0102-'
    station = '_'.join(stations_df.loc[str(wban_id),['state', 'location', 'vector']])
    return base + station.replace(' ','_') + '.txt'


# Main functions to E - T - L NOAA Weather Data
def load_stations_table():
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

    # use a sql engine with psycopg2 to load the df into postgres
    db_loc = 'postgresql+psycopg2://postgres:pass@localhost:5432/solarenergy'
    engine = create_engine(db_loc)
    stations_df.to_sql("weather_stations", engine, if_exists='append')

# command line instructions
if __name__ == '__main__':
    # Adjust Working Directory - DO WE WANT TO DO THIS????
    # ... DEPENDS IF WE NEED TO IMPORT ANYTHING FROM OTHER FILES.
    #initial_directory = os.getcwd()
    #os.chdir('/home/w205/w205_energy')

    # load stations
    load_stations_table()
