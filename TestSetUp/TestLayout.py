import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.legend_handler import HandlerLine2D

plt.title('Test Set up')

#X coordinate, Y coordinate
plt.plot([0,0,5], [0,5,5], 'r^', label = 'Reciever')

#X coordinate, Y coordinate
plt.plot([2.5, 3, 3.5, 4, 4.5, 5], [2.5, 2, 1.5, 1, 0.5, 0], 'bo-', label='Transmitter', linestyle='dashed')

#X min, X max, Y min, Y max
plt.axis([-1,6,-1,6])

#legend 
plt.legend() 

plt.show()