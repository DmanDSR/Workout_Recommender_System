""" This File is Made by Dylan Sedeno to help with cleaning files for
for data analytics. Started: 6/21/2024 Last Modified: 6/2024"""

# Imports Needed.
import pandas as pd

# Reading a csv file to a data frame. 
def read_csv(name):
    file = pd.read_csv(name)
    return file

# changes the column name to lowercase.
def col_low(df):
    df.columns = df.columns.str.lower()



