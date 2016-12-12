#!/usr/bin/env python
"""
This file contains a script to run a regression on the solar data and
predict year end and month end solar totals

MIDS W205, Fall 2016, Final Project
Team Sunshine
"""

# Imports
from __future__ import absolute_import, print_function, unicode_literals
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


# fxn to pull monthly numbers from postgres

# regression1 (predict monthly solar rad from weather)
# regression2 (predict monthly solar rad from partial)

# fxn to predict solar production given hypothedical field's weather conditions

# fxn to project monthly totals (& store in postgres)

# fxn to project year end totals (& store in postgres)
