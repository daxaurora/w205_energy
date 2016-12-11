"""This script converts Postgres tables into CSV files in preparation for
uploading CSVs to Amazon S3 for persistent storage.  The CSV files are saved in
the /home/w205/ folder on the AMI on which this script will be executed."""

# Imports
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# Define database location in postgres
db_loc = 'postgresql+psycopg2://postgres:pass@localhost:5432/solarenergy'
engine = create_engine(db_loc)

# Read postgres table contents into pandas dataframes
plants_df = pd.read_sql('SELECT * FROM plants', engine, index_col = "plant_id")
solar_df = pd.read_sql('SELECT * FROM solar_locations', engine,
                        index_col = "loc_id")
generation_df = pd.read_sql('SELECT * FROM generation', engine,
                             index_col = "index")
stations_df = pd.read_sql('SELECT * FROM weather_stations', engine,
                           index_col = "wban_id")
uscrn_df = pd.read_sql('SELECT * FROM uscrn_monthly', engine)

# Read pandas dataframes into CSV files
plants_df.to_csv("/home/w205/plants.csv")
solar_df.to_csv("/home/w205/solar.csv")
generation_df.to_csv("/home/w205/generation.csv")
stations_df.to_csv("/home/w205/stations.csv")
uscrn_df.to_csv("/home/w205/uscrn.csv")
