import os
from PIL import Image
import numpy as np
from matplotlib import patheffects
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
def gestureToPlot(gestures):
    filenames=[]
    for i,gesture in enumerate(gestures):
        X=gesture['X_positions']
        Y=gesture['Y_positions']
        coords = list(zip(X,Y))
        width=gesture['pressure_variation']
        lines = [(start, end) for start, end in zip(coords[:-1], coords[1:])]
        lines = LineCollection(lines, linewidths=width, path_effects=[patheffects.Stroke(capstyle="round")])
        plt.clf()
        fig, ax = plt.subplots()
        ax.add_collection(lines)
        # plt.plot(5, 10, marker="o", markersize=20, markeredgecolor="red", markerfacecolor="green")
        plt.axis([1,9,1,21])
        plt.grid(color='grey', linestyle='dotted', linewidth=0.5)
        plt.gca().invert_yaxis()
        plt.xticks(np.arange(1, 9, 1.0),fontsize=7)
        plt.yticks(np.arange(1, 21, 1.0),fontsize=7)
        plt.gca().set_aspect('equal')
        filename="{0}{1}.png".format('plot', i)
        filenames.append(filename)
        plt.savefig(filename, bbox_inches='tight')
        plt.close(fig)
    
    images = [Image.open(x) for x in filenames]
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('plot.png')
    