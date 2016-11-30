
# Project Sunshine
# Download EIA data

# DRAFT!!  NOT COMPLETE

# Right now this code is set up assuming this variable is previously defined
# in the Python environment:
# EIA_API_KEY = ''

# Imports
import os, requests, numpy as np, pandas as pd


# First download the list of states
# EIA list of states is here: http://www.eia.gov/opendata/qb.php?category=1017
category_states = '1017'
states_url = 'http://api.eia.gov/category/?api_key=' + EIA_API_KEY + \
             '&category_id=' + category_states
states = requests.get(states_url)

# Do we need to insert this error code or not?
# How would this fit with other scripts?
# Create a variable to hold the status code
states_status = states.status_code
# This code will return 200 as an integer if everything downloaded properly
if states_status != 200:
    print("The list of power plants did not download properly. " + \
          " Please run this script again.")
else:
    pass

# Turn the list of states into a dataframe.
states_dict = states.json()
states_json = pd.io.json.json_normalize(states_dict['category'])
states_df = pd.DataFrame(states_json['childcategories'][0],
                         columns = ["name", 'category_id'])

# For each state, download the list of all power plants in that state

# ### ER Diagram: PLANTS
# Dataframe created in this code can be used to create the "Plants" table in the ER diagram

# Create empty dataframe to hold the list of all power plants
# Columns = 1) Plant name; 2) Category_id for calling that plant's data via the API
columns = ["name", 'category_id']
all_plants_df = pd.DataFrame(columns = columns)

# Iterate over the category_id value for each state in the states_df dataframe
for state in states_df.itertuples():
    # Isolate the category_id for each state
    state_id = str(state[2])
    # Download the plant data
    plants_url = 'http://api.eia.gov/category/?api_key=' + EIA_API_KEY + \
                 '&category_id=' + state_id
    plants = requests.get(plants_url)
    # Turn the downloaded data into a dataframe
    plants_dict = plants.json()
    plants_json = pd.io.json.json_normalize(plants_dict['category'])
    plants_df = pd.DataFrame(plants_json['childcategories'][0],
                             columns = ["name", 'category_id'])
    # Append each state's list of plants to the master all plants datagrame
    temp_df = all_plants_df.append(plants_df, ignore_index = True)
    all_plants_df = temp_df

# Fix names to remove the numbers in parentheses that have indeterminate meaning
plants_name_temp1 = all_plants_df["name"].str.split(')').str.get(1)
plants_name_temp2 = pd.DataFrame(plants_name_temp1.str.split('(').str.get(0),
                                 columns = ["name"])
# plants_name_temp3 = pd.DataFrame(plants_name_temp2)
final_plants_df = pd.concat([plants_name_temp2, all_plants_df["category_id"]],
                             axis=1)
print(final_plants_df)

# NEXT: pull all locations with solar power from the list of plants
# Then pull electricity generation from those locations
# I'm working on these two things (Laura)
