
import pandas as pd
import numpy as np
from scipy.stats import fisher_exact

# Reading the dataset
smoking_survey = pd.read_csv("smoking_survey.csv")

# Selecting the required columns
smoking_survey = smoking_survey[['smoking_status', 'diagnosis_codes']]

# Function to determine if a subject has lung cancer based on diagnosis codes
def has_lung_cancer(codes):
    if "C34.90" in codes or "C96.29" in codes:
        return "yes"
    else:
        return "no"

# Applying the function to the diagnosis_codes column
smoking_survey['lung_cancer'] = smoking_survey['diagnosis_codes'].apply(has_lung_cancer)

# Dropping the diagnosis_codes column
smoking_survey = smoking_survey[['smoking_status', 'lung_cancer']]

# Converting columns to categorical types
smoking_survey['lung_cancer'] = pd.Categorical(smoking_survey['lung_cancer'], categories=["yes", "no"])
smoking_survey['smoking_status'] = pd.Categorical(smoking_survey['smoking_status'], categories=["smoker", "non-smoker"])

# Creating a contingency table
smoking_table = pd.crosstab(smoking_survey['smoking_status'], smoking_survey['lung_cancer'])

# Calculating Odds Ratio and p-value
odds_ratio, p_value = fisher_exact(smoking_table, alternative='two-sided')

# Displaying the contingency table and Odds Ratio
smoking_table, odds_ratio, p_value

