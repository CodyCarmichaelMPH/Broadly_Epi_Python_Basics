# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


# Load the dataset
data_path = 'Data/disease_dataset.csv'  # Adjust path as needed
df = pd.read_csv(data_path)


# Examine the data
print(df.head())

# Data cleaning and preparation
# Filter out irrelevant diseases and summarize distances
def group_by_distance(df, disease_str):
    filtered_df = df[df['Disease'] == disease_str]
    grouped_df = filtered_df.groupby('Distance from Well A').size().reset_index(name='count_A')
    return grouped_df

# Creating separate dataframes for each disease of interest
flu_distance = group_by_distance(df, 'Influenza')
cholera_distance = group_by_distance(df, 'Cholera')


# Calculate correlation
flu_corr = np.corrcoef(flu_distance['Distance from Well A'], flu_distance['count_A'])[0, 1]
cholera_corr = np.corrcoef(cholera_distance['Distance from Well A'], cholera_distance['count_A'])[0, 1]

print(f'Influenza Correlation: {flu_corr}')
print(f'Cholera Correlation: {cholera_corr}')



# Static graph for Influenza
plt.figure(figsize=(10, 6))
sns.regplot(x='Distance from Well A', y='count_A', data=flu_distance)
plt.title('Correlation between Distance from Well A and Count of Influenza Cases')
plt.xlabel('Distance from Well A (miles)')
plt.ylabel('Count of Influenza Cases')
plt.show()

# Static graph for Cholera
plt.figure(figsize=(10, 6))
sns.regplot(x='Distance from Well A', y='count_A', data=cholera_distance)
plt.title('Correlation between Distance from Well A and Count of Cholera Cases')
plt.xlabel('Distance from Well A (miles)')
plt.ylabel('Count of Cholera Cases')
plt.show()

# Interactive graph for Cholera using Plotly
fig = px.scatter(cholera_distance, x='Distance from Well A', y='count_A', trendline='ols',
                 title='Correlation between Distance from Well A and Count of Cholera Cases')
fig.show()
