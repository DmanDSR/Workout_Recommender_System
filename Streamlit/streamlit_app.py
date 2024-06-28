import streamlit as st
import pandas as pd
import os
from pathlib import Path

# os.path.exists(csv_file_path)
# Load the dataset
# Workout_Recommender_System/Streamlit/all_workouts_fixed.csv


csv_file_path = 'https://raw.githubusercontent.com/DmanDSR/Workout_Recommender_System/blob/main/Streamlit/all_workouts_fixed.csv'
# obj = Path(csv_file_path)
# if obj.exists:
all_workouts_fixed = pd.read_csv(csv_file_path)
# else:
#     st.error("CSV file not found. Please check the path.")

def to_lower(df: pd.DataFrame, column: str) -> pd.DataFrame:
    if column in df.columns:
        df[column] = df[column].apply(lambda x: x.lower() if isinstance(x, str) else x)
    return df

def create_column_based_on_dict(df: pd.DataFrame, target_column: str, new_column: str, dict_column: dict, delimiter=',') -> pd.DataFrame:
    def get_value(x):
        if delimiter is None:
            if x in dict_column:
                return dict_column[x]
            else:
                return 'Unknown'
        else:
            for value in x.split(delimiter):
                value = value.strip()
                if value in dict_column:
                    return dict_column[value]
            return 'Unknown'

    df[new_column] = df[target_column].apply(get_value)
    return df

# Fill NaN values in a column with a specified value.
def fill_nan(df: pd.DataFrame, column:str, value:any)-> pd.DataFrame:
    df[column].fillna(value, inplace=True)
    return df

# Apply cleaning functions
def apply_cleaning(df):
    force_categories = {'Cardio': 'N/A'}
    df = fill_nan(df, 'force', 'N/A')
    df = to_lower(df, 'muscle_group')
    df = to_lower(df, 'body_group')
    df = to_lower(df, 'force')
    df = to_lower(df, 'equipment')
    
    return df

all_workouts_fixed = apply_cleaning(all_workouts_fixed)

# Dictionary of user options
user_options = {'Body Group': None, 'Force': None, 'Muscle Group': None, 'Equipment': None}

# Filtering based on user inputs
def user_data(df: pd.DataFrame, user_options: dict) -> pd.DataFrame:
    user_set = df.copy()
    for key, value in user_options.items():
        if value and value != 'none':
            column = key.replace(" ", "_").lower()
            if value != 'any':
                user_set = user_set[user_set[column] == value]
    return user_set

# Goal details
goal_details = {
    'strength': {'reps': '1-5', 'sets': '3-6', 'rest': '2-5 min', 'weight': 'Heavy'},
    'growth': {'reps': '6-12', 'sets': '3-6', 'rest': '60-90 sec', 'weight': 'Middle'},
    'endurance': {'reps': '12-20', 'sets': '2-3', 'rest': '30-60 sec', 'weight': 'Light'},
    'power': {'reps': '1-5 (Explosive)', 'sets': '3-5', 'rest': '2-5 min', 'weight': 'Heavy'},
    'weight loss': {'reps': '10', 'sets': '3', 'rest': '90 sec', 'weight': 'Middle-Light'},
    'general fitness': {'reps': '12-15', 'sets': '1-3', 'rest': '30-90 sec', 'weight': 'Middle-Light'}
}

# Apply goal details
def u_goal_details(row, goal):
    sets = goal_details[goal]['sets']
    reps = goal_details[goal]['reps']
    rest = goal_details[goal]['rest']
    weight = goal_details[goal]['weight']
    row['goal'] = goal
    row['weight'] = weight
    row['sets'] = sets 
    row['reps'] = reps 
    row['rest'] = rest
    
    return row

# Streamlit app title
st.title("Exercise Data Interactive Dashboard")

# User inputs in sidebar
st.sidebar.header("User Inputs")
body_group = st.sidebar.selectbox("Select Body Group", options=['any'] + list(all_workouts_fixed['body_group'].unique()))
force = st.sidebar.selectbox("Select Force", options=['any'] + list(all_workouts_fixed['force'].unique()))
muscle_group = st.sidebar.selectbox("Select Muscle Group", options=['any'] + list(all_workouts_fixed['muscle_group'].unique()))
equipment = st.sidebar.selectbox("Select Equipment", options=['any'] + list(all_workouts_fixed['equipment'].unique()))
goal = st.sidebar.selectbox("Select Goal", options=list(goal_details.keys()))
days = st.sidebar.number_input("How many days can you workout?", min_value=1, max_value=7, value=3)

# Update user_options dictionary
user_options['Body Group'] = body_group if body_group != 'any' else None
user_options['Force'] = force if force != 'any' else None
user_options['Muscle Group'] = muscle_group if muscle_group != 'any' else None
user_options['Equipment'] = equipment if equipment != 'any' else None

# Apply filtering
filtered_exercises = user_data(all_workouts_fixed, user_options)

# Apply goal details
filtered_exercises = filtered_exercises.apply(u_goal_details, goal=goal, axis=1)

filtered_exercises.reset_index(drop=True, inplace=True)
# Display the filtered dataset
st.header("Recommended Exercises")
st.write(filtered_exercises)

# Option to download the filtered data
csv = filtered_exercises.to_csv(index=False)
st.download_button("Download Recommended Exercises", data=csv, file_name='recommended_exercises.csv', mime='text/csv')
