import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.legend_handler import HandlerLine2D

fig, ax = plt.subplots()
plt.title('Test Set up')

#X coordinates, Y coordinates
plt.plot([0,0,5], [0,5,5], 'r^', label = 'Reciever')

#X coordinates, Y coordinates
plt.plot([2.5, 3, 3.5, 4, 4.5, 5], [2.5, 2, 1.5, 1, 0.5, 0], 'bo-', label='Transmitter', linestyle='dashed')

#plt.plot([2.5, 3, 3.5, 4, 4.5, 5], [3.5, 3, 2.5, 2, 1.5, 1], 'gs-', label='Measured')

#X min, X max, Y min, Y max
plt.axis([-1,6,-1,6])

#grid 
plt.grid()

#legend 
plt.legend() 

plt.show()