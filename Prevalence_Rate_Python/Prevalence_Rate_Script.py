# Import necessary libraries
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

# 1.3 Optional: Convert population and depression cases to float (for precision)
data['Total Population'] = data['Total Population'].astype(float)
data['Diagnosed Depression Cases by Region Year'] = data['Diagnosed Depression Cases by Region Year'].astype(float)

# Step 2: Calculating Prevalence
# -------------------------------

# Prevalence Formula: (Diagnosed Depression Cases / Total Population) * 100
# This step adds a new column "Prevalence (%)" to the dataset
data['Prevalence (%)'] = (data['Diagnosed Depression Cases by Region Year'] / data['Total Population']) * 100

# Step 3: Prevalence by Year and Region
# --------------------------------------

# 3.1 Calculate the average prevalence by Year
prevalence_by_year = data.groupby('Year')['Prevalence (%)'].mean().reset_index()

# 3.2 Calculate the average prevalence by Region
prevalence_by_region = data.groupby('Region')['Prevalence (%)'].mean().reset_index()

# Display the tables for verification
print("Prevalence by Year")
print(prevalence_by_year)
print("\nPrevalence by Region")
print(prevalence_by_region)

# Step 4: Visualizations
# -----------------------

# Visualization 1: Line plot of Prevalence by Year
plt.figure(figsize=(10, 6))
plt.plot(prevalence_by_year['Year'], prevalence_by_year['Prevalence (%)'], marker='o', color='blue')
plt.title('Average Depression Prevalence by Year')
plt.xlabel('Year')
plt.ylabel('Prevalence (%)')
plt.grid(True)
plt.show()

# Visualization 2: Bar plot of Prevalence by Region
plt.figure(figsize=(10, 6))
plt.bar(prevalence_by_region['Region'], prevalence_by_region['Prevalence (%)'], color='green')
plt.title('Average Depression Prevalence by Region')
plt.xlabel('Region')
plt.ylabel('Prevalence (%)')
plt.xticks(rotation=45)
plt.show()
