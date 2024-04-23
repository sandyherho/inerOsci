#!/usr/bin/env python

"""
exec_time_plot.py

Plot & Calculate Stats of Execution Time

Sandy Herho <sandy.herho@email.ucr.edu>
04/22/2024
"""


import pandas as pd
import scipy.stats as stats
import scikit_posthocs as sp
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def main():
    # Read the CSV file into a DataFrame
    df = pd.read_csv('./multi_lang_execution_log_1000_runs.csv')

    # Separate the data based on the programming language
    fortran_df = df[df['Script'].str.endswith('.f95')].reset_index()
    python_df = df[df['Script'].str.endswith('.py')].reset_index()
    julia_df = df[df['Script'].str.endswith('.jl')].reset_index()
    octave_df = df[df['Script'].str.endswith('.m')].reset_index()
    r_df = df[df['Script'].str.endswith('.R')].reset_index()

    # Create a separate DataFrame for execution times
    execution_times_df = pd.DataFrame({
        'Fortran': fortran_df['Execution Time'],
        'Python': python_df['Execution Time'],
        'Julia': julia_df['Execution Time'],
        'Octave': octave_df['Execution Time'],
        'R': r_df['Execution Time']
    })

    print("Execution Times DataFrame:")
    print(execution_times_df)

    # Save the execution times DataFrame to a CSV file
    execution_times_df.to_csv('./tidy_exec_time.csv', index=False)

    # Save descriptive statistics of execution times to a CSV file
    round(execution_times_df.describe(), 3).to_csv('./stats_exec_time.csv')

    # Array of all groups for easy access
    all_data = [execution_times_df['Fortran'], execution_times_df['Python'], execution_times_df['Julia'], execution_times_df['Octave'], execution_times_df['R']]
    labels = ['Fortran', 'Python', 'Julia', 'Octave', 'R']

    # Prepare data for Dunn's test by creating a DataFrame
    data_stacked = np.concatenate(all_data)
    groups = np.concatenate([[label] * len(data) for data, label in zip(all_data, labels)])
    df_dunn = pd.DataFrame({'Execution Time': data_stacked, 'Group': groups})

    # Visualizations for each group
    # Create and save a Boxplot
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='Group', y='Execution Time', data=df_dunn)
    plt.xticks(ticks=np.arange(len(labels)), labels=labels, fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Computing Environment', fontsize=18)
    plt.ylabel('Execution Time [seconds]', fontsize=18)
    plt.tight_layout()
    plt.savefig('./figs/fig3.png', dpi=450)

    alpha = 0.05

    # Perform the Kruskal-Wallis test
    kw_stat, kw_pvalue = stats.kruskal(*all_data)

    # Print the Kruskal-Wallis test results
    print(f'Kruskal-Wallis test statistic: {kw_stat:.3f}, p-value: {kw_pvalue:.3f}')
    if kw_pvalue < alpha:
        print("Significant differences found among the groups.")
        print("This indicates that at least one group's median significantly differs from the others.")
    else:
        print("No significant differences found among the groups.")
        print("This suggests that there is no statistical evidence to conclude that the groups differ in median.")

    # Proceed with Dunn's post-hoc test if significant
    if kw_pvalue < alpha:
        # Dunn's post-hoc test with Bonferroni adjustment
        dunn_pvalues = sp.posthoc_dunn(df_dunn, val_col='Execution Time', group_col='Group', p_adjust='bonferroni')

        # Print Dunn's test results
        print("Dunn's test p-values (Bonferroni adjusted):")
        print(dunn_pvalues.round(3))
        print("Values below 0.05 indicate pairs of groups with statistically significant differences in medians.")

        # Visualize Dunn's test results using a heatmap with black border lines
        plt.figure(figsize=(10, 8))
        ax = sns.heatmap(dunn_pvalues, cmap='binary_r', fmt=".3f",
                         xticklabels=labels, yticklabels=labels,
                         linecolor='black', linewidths=1)
        colorbar = ax.collections[0].colorbar
        colorbar.set_label('p-values', fontsize=22)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.savefig('./figs/fig4.png', dpi=450)

if __name__ == "__main__":
    main()

