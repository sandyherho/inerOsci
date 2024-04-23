#!/usr/bin/env python

"""
traject_plot.py

Plot Trajectory of A Fluid Parcel

Sandy Herho <sandy.herho@email.ucr.edu>
04/22/2024
"""


import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('bmh')

def main():
    # Read the data from the text file
    with open('output1.txt', 'r') as file:
        data = file.read().strip().split('\n')[1:]  # Skip the first line

    # Create lists to store the values
    x_values = []
    y_values = []
    time_values = []

    # Iterate through the data and append values to the lists
    for row in data:
        values = row.split()
        x_values.append(float(values[0]))
        y_values.append(float(values[1]))
        time_values.append(float(values[2]))

    # Create the DataFrame
    df = pd.DataFrame({
        'x': x_values,
        'y': y_values,
        'time': time_values
    })

    print("DataFrame Head:")
    print(df.head())  # Print the first few rows of the DataFrame

    # Plot x-position over time
    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['x'], color="#3297c9", marker="o", linestyle="--")
    plt.xlim(df['time'].min(), df['time'].max())
    plt.ylim(df['x'].min() - 2, df['x'].max() + 2)
    plt.xlabel('Time [seconds]', fontsize=14)
    plt.ylabel(r'$x$-position [cm]', fontsize=14)
    plt.tight_layout()
    plt.savefig('./figs/fig1a.png', dpi=450)

    # Plot y-position over time
    plt.figure(figsize=(12, 6))
    plt.plot(df['time'], df['y'], color="#f04337", marker="o", linestyle="--")
    plt.xlim(df['time'].min(), df['time'].max())
    plt.ylim(df['y'].min() - 2, df['y'].max() + 2)
    plt.xlabel('Time [seconds]', fontsize=14)
    plt.ylabel(r'$y$-position [cm]', fontsize=14)
    plt.tight_layout()
    plt.savefig('./figs/fig1b.png', dpi=450)

    # Plot x-y positions
    plt.figure(figsize=(10, 10))
    plt.plot(df['x'], df['y'], marker=">", color="#2a9e1b", linestyle="--")
    plt.xlim(df['x'].min(), df['x'].max())
    plt.ylim(df['y'].min(), df['y'].max())
    plt.xlabel(r'$y$-position [cm]', fontsize=18)
    plt.ylabel(r'$x$-position [cm]', fontsize=18)
    plt.tight_layout()
    plt.savefig('./figs/fig2.png', dpi=450)

if __name__ == "__main__":
    main()

