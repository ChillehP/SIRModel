#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Basic-Instructions" data-toc-modified-id="Basic-Instructions-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Basic Instructions</a></span></li><li><span><a href="#Code" data-toc-modified-id="Code-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Code</a></span></li></ul></div>

# # Basic Instructions
#
# 1 Initialise basic grid
#
# 2 initialise 'next' grid as a copy of basic grid
#
# 3 Get list of all Infected squares
#
# 4 For each Infected squares:
#
# 4.1 Get list of valid suspectible tiles around it
#
# 4.2 randomly change S to I in the 'next' grid based on Infection rate
#
# 5 For all Infected squares, randomly 'recover' squares in the 'next' grid
#
# 6 current grid is changed to next grid
#
# 7 increase timestep
#

# # Code

# In[9]:


def main():

    # Libraries
    import random
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time
    import pandas as pd
    #get_ipython().run_line_magic('matplotlib', 'notebook')

    def SIRModel(size=50, Irate=0.92, Rrate=0.8, Ttime=100, inc=10):
        ''' arguments:
        size determines the rows/columns in the infection grid
        Irate is the chance that a Susceptible cell does not get infected when near an infected cell
        Rrate is the chance that an Infected cell does not recover when past incubation period
        Ttime is the number of time steps to run model for
        inc is the incubation period after infection where recovery cannot occur'''

        # Setting up initial condition grid
        arr = np.zeros([size, size])
        mid = int(np.floor((size+1) / 2)-1)

        # Setting up incubation grid
        arrI = np.zeros([size, size])

        # first infected tile in the centre
        arr[mid, mid] = 1

        # Set up DataFrame and populate first row
        data = pd.DataFrame(columns=['Time', 'S', 'I', 'R'])
        S = np.count_nonzero(arr == 0)
        I = np.count_nonzero(arr == 1)
        R = np.count_nonzero(arr == 2)
        newrow = {'Time': 0,
                  'S': S,
                  'I': I,
                  'R': R,
                  }
        data = data.append(newrow, ignore_index=True)

        # Setting up initial plots
        plt.ion()
        fig, (ax1, ax2) = plt.subplots(2, 1,
                                       gridspec_kw={'height_ratios': [3, 2]},
                                       figsize=(8, 11))
        fig.suptitle('Infection grid')
        infec = ax1.imshow(arr, vmin=0, vmax=2, cmap='rainbow')
        SChart, = ax2.plot(data.Time, data.S, label='S')
        IChart, = ax2.plot(data.Time, data.I, label='I')
        RChart, = ax2.plot(data.Time, data.R, label='R')
        ax2.legend(loc=7)
        ax1.set_axis_off()
        ax2.set_xlim([0, Ttime])
        ax2.set_ylim([0, (size**2)*1.1])
        fig.canvas.draw()

        # Grid loop
        for t in range(1, Ttime):
            # Copy of current n-grid on which to write n+1 conditions
            arrn = np.copy(arr)

            # row loop i
            for i in range(size):

                # column loop j
                for j in range(size):

                    # If infected, random infection in n+1 grid for 8 squares surrounding
                    if arr[i, j] == 1:
                        for k in range(-1, 2):
                            for l in range(-1, 2):

                                # Checks if surrounding squares are within the grid
                                if i+k > -1 and j+l > -1 and i+k < size and j+l < size:

                                    # If suspectible
                                    if arr[i+k, j+l] == 0:
                                        if random.random() > Irate:
                                            arrn[i+k, j+l] = 1

            # if incubation period longer than inc value, random recovery
            for i in range(size):
                for j in range(size):
                    if arrI[i, j] > inc:
                        if random.random() > Rrate:
                            arrn[i, j] = 2

            # Increase infected incubation period by 1
            for i in range(size):
                for j in range(size):
                    if arr[i, j] == 1:
                        arrI[i, j] += 1

            # n+1 grid becomes the new grid for next time step
            arr = arrn

            # Count values of each subset and update Dataframe
            S = np.count_nonzero(arr == 0)
            I = np.count_nonzero(arr == 1)
            R = np.count_nonzero(arr == 2)
            newrow = {'Time': t,
                      'S': S,
                      'I': I,
                      'R': R,
                      }
            data = data.append(newrow, ignore_index=True)

            # update plot graphics and refresh
            infec.set_data(arr)
            SChart.set_ydata(data.S)
            SChart.set_xdata(data.Time)
            IChart.set_ydata(data.I)
            IChart.set_xdata(data.Time)
            RChart.set_ydata(data.R)
            RChart.set_xdata(data.Time)
            ax1.set_title(t)
            fig.canvas.draw()
            fig.canvas.flush_events()

    # Run the model
    SIRModel()

if __name__ in "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:
