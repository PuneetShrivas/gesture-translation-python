import os
from matplotlib import patheffects
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
def gestureToPlot(gesture):
    X=gesture['X_positions']
    Y=gesture['Y_positions']
    coords = list(zip(X,Y))
    width=gesture['pressure_variation']
    lines = [(start, end) for start, end in zip(coords[:-1], coords[1:])]
    lines = LineCollection(lines, linewidths=width, path_effects=[patheffects.Stroke(capstyle="round")])
    plt.clf()
    fig, ax = plt.subplots()
    ax.add_collection(lines)
    plt.axis([1,9,1,21])
    plt.grid(color='grey', linestyle='dotted', linewidth=0.5)
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal')
    plt.savefig('plot.png', bbox_inches='tight')
  