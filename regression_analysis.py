#!/usr/bin/env python
"""
This file contains a script to run a regression on the solar data and
predict year end and month end solar totals

MIDS W205, Fall 2016, Final Project
Team Sunshine
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import numpy as np
import pandas as pd
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
            SELECT solar_fields.loc_id, solar_fields.wban_id, full_date, mwh,
            CAST(solar_radiation as decimal) as solar_radiation,
            FROM(
                (SELECT loc_id, closest_station, full_date,
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

def run_regression(data_df):
    """
    Function to run a regression on the relationship between solar radiation
    levels and energy production from solar field locations.
    """
    pass
# regression1 (predict monthly solar rad from weather)
# regression2 (predict monthly solar rad from partial)

# fxn to predict solar production given hypothedical field's weather conditions

# fxn to project monthly totals (& store in postgres)

# fxn to project year end totals (& store in postgres)
