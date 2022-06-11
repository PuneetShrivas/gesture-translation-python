import os
from PIL import Image
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
        plt.axis([1,9,1,21])
        plt.grid(color='grey', linestyle='dotted', linewidth=0.5)
        plt.gca().invert_yaxis()
        plt.gca().set_aspect('equal')
        filename="{0}{1}.png".format('plot', i)
        filenames.append(filename)
        plt.savefig(filename, bbox_inches='tight')
    
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
    