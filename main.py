import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file into a DataFrame
df = pd.read_csv('Assignment_Timecard.csv')

# Seven Consecutive days
# Convert 'Time' and 'Time Out' columns to datetime objects
df['Time'] = pd.to_datetime(df['Time'])
df['Time Out'] = pd.to_datetime(df['Time Out'])

# Sort the DataFrame by 'Employee Name' and 'Time'
df_sorted = df.sort_values(by=['Employee Name', 'Time'])


# Function to check if an employee worked for 7 consecutive days
def consecutive_days(employee_data):
    dates = employee_data['Time'].dt.date.unique()  # Extract unique dates
    for i in range(len(dates) - 6):  # Loop through dates to check for 7 consecutive days
        if dates[i + 6] - dates[i] == timedelta(days=6):
            return True
    return False


# Filter the data for employees who have worked for 7 consecutive days
consecutive_employees = df_sorted.groupby('Employee Name').filter(consecutive_days)

# Extract unique employee names who worked for 7 consecutive days
consecutive_employee_names = consecutive_employees['Employee Name'].unique()



