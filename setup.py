#!/usr/bin/env python
"""
This file contains a script to set up a Postgres Database and tables.
It will also create a credentials file to store the users API keys
for reference in subsequent code.
"""

# imports
from __future__ import absolute_import, print_function, unicode_literals
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# defining functions to modularize setup script
def create_database():
    """Function to create solarenergy databse"""
    conn = psycopg2.connect(database='postgres', user='postgres',
                            password='pass', host='localhost', port='5432')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS solarenergy")
    cur.execute("CREATE DATABASE solarenergy")
    conn.close()

def create_tables():
    """Function to create tables within DB"""
    conn = psycopg2.connect(database='solarenergy', user='postgres',
                            password='pass', host='localhost', port='5432')
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS plants")
    cur.execute("""CREATE TABLE plants
                (plant_id TEXT PRIMARY KEY NOT NULL,
                 name TEXT NOT NULL)""")
    conn.commit()
    cur.execute("DROP TABLE IF EXISTS solar_locations")
    cur.execute("""CREATE TABLE solar_locations
                (loc_id TEXT PRIMARY KEY NOT NULL,
                 plant_id TEXT NOT NULL,
                 latitude TEXT NOT NULL,
                 longitude TEXT NOT NULL)""")
    conn.commit()
    cur.execute("DROP TABLE IF EXISTS generation")
    cur.execute("""CREATE TABLE generation
                (index TEXT PRIMARY KEY NOT NULL,
                 series_id TEXT NOT NULL,
                 year TEXT NOT NULL,
                 month TEXT NOT NULL,
                 mwh TEXT NOT NULL)""")
    conn.commit()
    cur.execute("DROP TABLE IF EXISTS weather_stations")
    cur.execute("""CREATE TABLE weatherstations
                (wban_id TEXT PRIMARY KEY NOT NULL,
                 name TEXT NOT NULL,
                 location TEXT NOT NULL,
                 vector TEXT NOT NULL,
                 state TEXT NOT NULL,
                 latitude TEXT NOT NULL,
                 longitude TEXT NOT NULL,
                 elevation TEXT NOT NULL)""")
    conn.commit()
    cur.execute("DROP TABLE IF EXISTS uscrn_monthly")
    cur.execute("""CREATE TABLE uscrn_monthly
                (month TEXT PRIMARY KEY NOT NULL,
                 wban_id TEXT NOT NULL,
                 max_temp TEXT NOT NULL,
                 min_temp TEXT NOT NULL,
                 mean_temp TEXT NOT NULL,
                 precipitation TEXT NOT NULL,
                 solar_radiation TEXT NOT NULL)""")
    conn.commit()
    conn.close()

def recreate_token_file(filepath="~/w205_energy/certs/mytokens.py"):
    """
    Function to recreate the file to store credentials.
    """
    doc = '#!/usr/bin/env python\n'
    doc += '"""\n'
    doc += 'This file is a temporary location for EIA and NOAA credentials \n'
    doc += 'needed for the data ingest.\n'
    doc += 'NOTE: contents of this file will be populated & deleted by the \n'
    doc += 'setup & clean up scripts associated with this project.'
    doc += '\n"""\n'
    with open(filepath, 'w') as f:
        f.write(doc)
    print("... Empty credentials file created: ", filepath)

def get_user_credentials():
    """
    Function to solicit the user's EIA and NOAA credentials to allow storm
    to access the climate and energy data. This function returns a string of
    credentials to be appended to a file in the certs folder.
    """
    print("... WARNING: As part of the setup process you will need to provide",
          "the following credentials: EIA API key & NOAA CDO access token.")
    proceed = raw_input("... Do you wish to proceed at this time?[y/n] ")
    if proceed.strip(' ').lower() in ['y','yes']:
        credentials = "\nEIA_API_KEY = \'"
        credentials += raw_input('Enter your EIA API key: ').strip(' ')
        credentials += "\'\nNOA_CDO_TOKEN = \'"
        credentials += raw_input('Enter your NOAA CDO token: ').strip(' ')
        credentials += "\'\n"
        print("... You have entered the following credentials: ", credentials)
        submit = raw_input("Please confirm these are correct[y/n]: ").strip(' ')
        if submit.lower() in ['y', 'yes']:
            return credentials
    return None

# main script to be run at the command line
if __name__ == '__main__':
    # prep postgres database and table
    create_database()
    create_tables()
    print("... Created new Postgres database and table for solar energy.")
    # request the user's API tokens
    credentials = get_user_credentials()
    if credentials:
        recreate_token_file()
        with open(filepath, 'a') as f:
            f.write(credentials)
        print("... Credentials successfully stored.")
        print("... You are now ready to deploy your application.")
    else:
        print("... OK. No credentials stored at this time.")
        print("... Please re-run setup.sh to store your credentials before deploying your application.")
