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
