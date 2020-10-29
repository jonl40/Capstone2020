import matplotlib.pyplot as plt

fig, ax = plt.subplots()
plt.title('Test Set up')

#X coordinates, Y coordinates
plt.plot([0,0,4], [0,3,3], 'r^', label = 'Reciever')

#X coordinates, Y coordinates
plt.plot([2,3,4], [2,1,0], 'bo-', label='Transmitter', linestyle='dashed')

#X min, X max, Y min, Y max
plt.axis([-1,5,-1,4])

#grid 
plt.grid()

#legend 
plt.legend() 

plt.show()