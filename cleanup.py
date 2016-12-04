#!/usr/bin/env python
"""
This file contains a script to clean up (delete) Postgres Database
and remove the user's API tokens from mytokens.py.
"""

# imports
from __future__ import absolute_import, print_function, unicode_literals
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# defining functions to modularize setup script
def delete_database():
    """Function to delete solarenergy databse"""
    conn = psycopg2.connect(database='postgres', user='postgres',
                            password='pass', host='localhost', port='5432')
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("DROP DATABASE IF EXISTS solarenergy")
    conn.close()


# main script to be run at the command line
if __name__ == '__main__':
    # Adjust Working Directory to import function from setup file
    INITIAL_DIRECTORY = os.getcwd()
    os.chdir('/home/w205/w205_energy')
    from setup import recreate_token_file

    # delete credentials
    print("... Preparing to delete your stored credentials.")
    print("... Typing yes below will prevent subsequent deployment of this application.")
    proceed = raw_input("Do you want to proceed at this time[y/n]: ")
    if proceed.strip(' ').lower() in ['y', 'yes']:
        recreate_token_file()
        print("... Credentials successfully deleted.")
    else:
        print("... OK. Credentials not deleted at this time.")

    # delete database/table
    proceed = raw_input("Do you want to delete the database that was created when you deployed this application? [y/n]: ")
    if proceed.strip(' ').lower() in ['y', 'yes']:
        delete_database()
        print("... Postgres database successfully deleted.")
    else:
        print("... OK. Your results remain stored in Postgres.")

    # return user to original location
    os.chdir(INITIAL_DIRECTORY)
