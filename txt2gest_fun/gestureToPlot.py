import os
import matplotlib.pyplot as plt
def gestureToPlot(gesture):
    X=gesture['X_positions']
    Y=gesture['Y_positions']
    plt.clf()
    plt.axis([1,9,1,21])
    plt.gca().invert_yaxis()
    plt.gca().set_aspect('equal')
    
    plt.plot(X,Y)
    # os.remove('plot.png')
    plt.savefig('plot.png', bbox_inches='tight')

   
    pass