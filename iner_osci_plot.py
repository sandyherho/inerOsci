#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Set the 'bmh' style for aesthetic preference
plt.style.use('bmh')

# Load data from the text file
data = np.loadtxt('output2.txt', skiprows=1)
times = data[:, 2] / (24 * 3600)  # Convert seconds to days

# Set up the figure and axis
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(0, 30)  # Adjust these limits if necessary
ax.set_ylim(0, 30)
ax.set_xticks(np.arange(0, 31, 10))
ax.set_yticks(np.arange(0, 31, 10))
ax.set_xlabel('x (km)')
ax.set_ylabel('y (km)')
line, = ax.plot([], [], '-', linewidth=2)  # Line initialized empty

# Add a text element to display the time
time_text = ax.text(0.5, 0.02, '', transform=ax.transAxes, horizontalalignment='center',
                    verticalalignment='bottom', fontsize=10)

# Initialization function for the animation
def init():
    line.set_data([], [])
    time_text.set_text('')
    return line, time_text

# Animation update function
def update(n):
    x = data[:n+1, 0]
    y = data[:n+1, 1]
    line.set_data(x, y)
    # Format time to display it in days, rounded to two decimal places
    time_text.set_text(f'Time: {times[n]:.2f} days')
    return line, time_text

# Create the animation
ani = FuncAnimation(fig, update, frames=len(data), init_func=init, blit=True, repeat=True)

# Show the plot
plt.show()

