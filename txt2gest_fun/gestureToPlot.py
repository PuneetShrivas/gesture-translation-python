import os
from turtle import color
from PIL import Image
import numpy as np
from matplotlib import patheffects
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

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
    

def gestureToGif(gestures,overlay,frame,speed):
    if speed==None: speed=5
    if frame!=None: gesture=gestures[frame-1]
    else: gesture=gestures[0]
    X_values=gesture['X_positions']
    Y_values=gesture['Y_positions']
    pressure_values=gesture['pressure_variation']
    pressures=[]
    X=[]
    Y=[]
    fig = plt.figure()
    ims=[]
    for i in range(len(X_values)):
        X.append(X_values[i])
        Y.append(Y_values[i])
        pressures.append(pressure_values[i])
        plt.axis([1,9,1,21])
        plt.grid(color='grey', linestyle='dotted', linewidth=0.5)
        plt.gca().invert_yaxis()
        plt.xticks(np.arange(1, 9, 1.0),fontsize=7)
        plt.yticks(np.arange(1, 21, 1.0),fontsize=7)   
        plt.gca().set_aspect('equal') 
        fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        plt.tight_layout()            
        sizes_factors=[0, 1, 2, 3, 6, 10]
        if overlay:
            plt.plot(X,Y,color='grey',linewidth=0.5)
        if i>4:
                sizes=[a*b for a,b in zip(sizes_factors,pressures[i-5:i+1])]
                im = plt.scatter(X[i-5:i+1],Y[i-5:i+1],s=sizes,color='blue')
        else:
                sizes=[a*b for a,b in zip(sizes_factors[0:i+1],pressures[0:i+1])]
                im = plt.scatter(X[0:i+1],Y[0:i+1],s=sizes,color='blue')
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat_delay=500)
    writer = PillowWriter(fps=speed)
    ani.save("plot.gif", writer=writer)
    