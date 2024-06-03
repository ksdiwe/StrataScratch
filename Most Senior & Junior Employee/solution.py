# Import your libraries
import pandas as pd

# Filtering the dataset to include only employees who still work for the company (termination date is null):
result = uber_employees[uber_employees.termination_date.isna()]

# finding the hiring date of the employee(s) with the most recent hire date and counting the number of employees:
max_date = (
    result[result.hire_date == max(result.hire_date)][["id", "hire_date"]]
    .groupby("hire_date")["id"]
    .count()
    .reset_index(name="shortest_tenured_count"))

# Finding the hiring date of the employee(s) with the earliest hire date and counting the number of employees:    
min_date = (
    result[result.hire_date == min(result.hire_date)][["id", "hire_date"]]
    .groupby("hire_date")["id"]
    .count()
    .reset_index(name="longest_tenured_count"))
    
# combining the 'max_date' and 'min_date' into a single dataframe
result = pd.concat(
    [
        max_date.rename(columns={'hire_date': "most_hire_date"}),
        min_date.rename(columns={'hire_date': "least_hire_date"}),
        ],
        axis = 1)
        
# calculating the number of days between the longest and least tenured employees's hiring date
result['days_diff'] = (
    result["most_hire_date"] - result["least_hire_date"]).dt.days
    
# selecting the required columns for the final output
result[["shortest_tenured_count", "longest_tenured_count", "days_diff"]]
