import pandas as pd
from scipy import stats
import numpy as np

# 1. Read CSV file
df = pd.read_csv("Belfast_Suicide_Counts.csv")


# 2. Reshape to long format
long_df = df.melt(id_vars=['Assembly Area'], var_name='Year', value_name='Count')

# 3. Spread to wide format
wide_df = long_df.pivot(index='Year', columns='Assembly Area', values='Count')

# The easy way to perform a t-test
t_test_result = stats.ttest_ind(wide_df['Belfast North'].dropna(), wide_df['Belfast South'].dropna(), equal_var=False)

print(f"T-test result: statistic={t_test_result.statistic}, p-value={t_test_result.pvalue}")

# Calculating means, standard deviations, sample sizes, standard error of the difference, t-statistic, degrees of freedom, and p-value manually
mean_north = np.mean(wide_df['Belfast North'])
mean_south = np.mean(wide_df['Belfast South'])
sd_north = np.std(wide_df['Belfast North'], ddof=1)
sd_south = np.std(wide_df['Belfast South'], ddof=1)
n_north = wide_df['Belfast North'].count()
n_south = wide_df['Belfast South'].count()

se_difference = np.sqrt(sd_north**2 / n_north + sd_south**2 / n_south)
t_statistic = (mean_north - mean_south) / se_difference
df = ((sd_north**2 / n_north + sd_south**2 / n_south)**2) / ((sd_north**4 / (n_north**2 * (n_north - 1))) + (sd_south**4 / (n_south**2 * (n_south - 1))))
p_value = 2 * stats.t.cdf(-abs(t_statistic), df)

print(f"T-statistic: {t_statistic}\nP-value: {p_value}")
