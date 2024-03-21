import pandas as pd

# Load the data
data = pd.read_csv('smoking_survey.csv')

def has_lung_cancer(codes):
    # Check if the lung cancer codes are present in the diagnosis codes string
    lung_cancer_codes = ['C34.90', 'C96.29']
    return 'yes' if any(code in codes for code in lung_cancer_codes) else 'no'

# Reapply the function considering the grepl-like approach
data['lung_cancer'] = data['diagnosis_codes'].apply(has_lung_cancer)

# create the filtered data with the adjusted lung cancer identification
filtered_data = data[['smoking_status', 'lung_cancer']]

# Ensure the order of factors by sorting the DataFrame before creating the contingency table
filtered_data['smoking_status'] = pd.Categorical(filtered_data['smoking_status'], categories=['smoker', 'non-smoker'], ordered=True)
filtered_data['lung_cancer'] = pd.Categorical(filtered_data['lung_cancer'], categories=['yes', 'no'], ordered=True)

# create the contingency table with the adjusted data
contingency_table = pd.crosstab(filtered_data['smoking_status'], filtered_data['lung_cancer'])

# calculate Relative Risk using the contingency table from the grepl-like approach
rr_table = Table2x2(contingency_table.values)
rr = rr_table.riskratio
rr_ci_lower, rr_ci_upper = rr_table.riskratio_confint()

# Display the adjusted results
contingency_table, rr, rr_ci_lower, rr_ci_upper
