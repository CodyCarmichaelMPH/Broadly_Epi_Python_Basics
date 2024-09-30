# Step 0: Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'Depression_and_Population_Data.csv'
data = pd.read_csv(file_path)

# Step 1: Data Cleaning
# ----------------------

# 1.1 Check for missing values (optional, for verification)
print(data.isnull().sum())

# 1.2 Check the data types (ensure correct format)
print(data.dtypes)

# 1.3 Convert population and depression cases to float (for precision)
data['Total Population'] = data['Total Population'].astype(float)
data['Diagnosed Depression Cases by Region Year'] = data['Diagnosed Depression Cases by Region Year'].astype(float)

# Step 2: Calculate Incidence Rate for Each Year and Region
# ---------------------------------------------------------

# Calculate incidence rate (per 1000 population)
data['Incidence Rate (per 1000)'] = (data['Diagnosed Depression Cases by Region Year'] / data['Total Population']) * 1000

# Step 3: Calculate Year-Over-Year Change in Incidence Rate
# ----------------------------------------------------------

# Sort the data by Region and Year for correct sequential calculation
data = data.sort_values(by=['Region', 'Year']).reset_index(drop=True)

# Create a new column to store the change in incidence rate
data['Change in Incidence Rate (per 1000)'] = 0.0

# Calculate the year-over-year change in incidence rate by region
regions = data['Region'].unique()

for region in regions:
    # Filter data for the specific region
    regional_data = data[data['Region'] == region]
    for i in range(1, len(regional_data)):
        # Get the current and previous row
        current_row = regional_data.iloc[i]
        previous_row = regional_data.iloc[i - 1]

        # Calculate the change in incidence rate
        change_in_incidence = current_row['Incidence Rate (per 1000)'] - previous_row['Incidence Rate (per 1000)']

        # Set the value in the main dataframe
        data.loc[(data['Region'] == region) & (data['Year'] == current_row['Year']), 'Change in Incidence Rate (per 1000)'] = change_in_incidence

# Step 4: Incidence and Change in Incidence by Year and Region
# ------------------------------------------------------------

# 4.1 Calculate the average incidence rate by Year
incidence_by_year = data.groupby('Year')['Incidence Rate (per 1000)'].mean().reset_index()

# 4.2 Calculate the average incidence rate by Region
incidence_by_region = data.groupby('Region')['Incidence Rate (per 1000)'].mean().reset_index()

# 4.3 Calculate the average change in incidence rate by Year (excluding the first year)
change_in_incidence_by_year = data.groupby('Year')['Change in Incidence Rate (per 1000)'].mean().reset_index()

# 4.4 Calculate the average change in incidence rate by Region (excluding the first year)
change_in_incidence_by_region = data.groupby('Region')['Change in Incidence Rate (per 1000)'].mean().reset_index()

# Display the tables for verification
print("Incidence Rate by Year")
print(incidence_by_year)
print("\nIncidence Rate by Region")
print(incidence_by_region)
print("\nChange in Incidence Rate by Year")
print(change_in_incidence_by_year)
print("\nChange in Incidence Rate by Region")
print(change_in_incidence_by_region)

# Step 5: Visualizations
# -----------------------

# Visualization 1: Line plot of Incidence Rate by Year
plt.figure(figsize=(10, 6))
plt.plot(incidence_by_year['Year'], incidence_by_year['Incidence Rate (per 1000)'], marker='o', color='blue')
plt.title('Average Depression Incidence Rate by Year')
plt.xlabel('Year')
plt.ylabel('Incidence Rate (per 1000)')
plt.grid(True)
plt.show()

# Visualization 2: Bar plot of Incidence Rate by Region
plt.figure(figsize=(10, 8))
plt.bar(incidence_by_region['Region'], incidence_by_region['Incidence Rate (per 1000)'], color='green')
plt.title('Average Depression Incidence Rate by Region')
plt.xlabel('Region')
plt.ylabel('Incidence Rate (per 1000)')
plt.xticks(rotation=45)
plt.show()

# Visualization 3: Line plot of Change in Incidence Rate by Year
plt.figure(figsize=(10, 6))
plt.plot(change_in_incidence_by_year['Year'], change_in_incidence_by_year['Change in Incidence Rate (per 1000)'], marker='o', color='red')
plt.title('Average Yearly Change in Depression Incidence Rate by Year')
plt.xlabel('Year')
plt.ylabel('Change in Incidence Rate (per 1000)')
plt.grid(True)
plt.show()

# Visualization 4: Bar plot of Change in Incidence Rate by Region
plt.figure(figsize=(10, 6))
plt.bar(change_in_incidence_by_region['Region'], change_in_incidence_by_region['Change in Incidence Rate (per 1000)'], color='purple')
plt.title('Average Change in Depression Incidence Rate by Region')
plt.xlabel('Region')
plt.ylabel('Change in Incidence Rate (per 1000)')
plt.xticks(rotation=45)
plt.show()
