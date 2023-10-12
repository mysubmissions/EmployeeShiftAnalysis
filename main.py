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


# Less than 10 hours of time
# Function to check if an employee has less than 10 hours but more than 1 hour between shifts
def time_between_shifts(employee_data):
    time_diffs = employee_data['Time'].diff().dropna()
    for diff in time_diffs:
        if timedelta(hours=1) < diff < timedelta(hours=10):
            return True
    return False


# Filter the data for employees who have less than 10 hours but more than 1 hour between shifts
time_between_shifts_employees = df_sorted.groupby('Employee Name').filter(time_between_shifts)

# Extract unique employee names who have less than 10 hours but more than 1 hour between shifts
time_between_shifts_employee_names = time_between_shifts_employees['Employee Name'].unique()

# Worked for more than 14 hours in a single shift
# Convert the 'Timecard Hours (as Time)' column to timedelta format
df['Timecard Hours'] = pd.to_timedelta(df['Timecard Hours (as Time)'].str.replace(':', ' hours ') + ' minutes')

# Filter employees who have worked more than 14 hours in a single shift
long_shift_employees = df[df['Timecard Hours'] > timedelta(hours=14)]

# Extract unique employee names who have worked more than 14 hours in a single shift
long_shift_employee_names = long_shift_employees['Employee Name'].unique()


# Summarizing the results
output = """
Employees who have worked for 7 consecutive days:
-------------------------------------------------
{}

Employees who have less than 10 hours of time between shifts but greater than 1 hour:
--------------------------------------------------------------------------------------
{}

Employees who have worked for more than 14 hours in a single shift:
-------------------------------------------------------------------
{}
""".format(
    "\n".join(consecutive_employee_names),
    "\n".join(time_between_shifts_employee_names),
    "\n".join(long_shift_employee_names)
)

# Write the output to a text file
output_file_path = "output.txt"
with open(output_file_path, 'w') as f:
    f.write(output)
