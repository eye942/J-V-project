# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

def load():
    with open('C:/Users/Eric/Dropbox/J-V/test/opv_Friday_d1  151014-171247.txt', 'r') as infile:

        data = infile.read()  # Read the contents of the file into memory.

    # Return a list of the lines, breaking at line boundaries.
    return data.splitlines()
    
    
def splitTab(dataList):
    
    stringList = []
    for line in dataList:
        if line.find("\t") > -1:
            tab = line.find("\t")
            try:
                x = [float(line[:tab]), float(line[tab+1:])]
                stringList.append(x)
            except:
                pass
            
        else:
            pass
    return stringList

#def splitString(string, index):
 #   try:
  #      return [float(string[:index]), float(string[index+1:])]
   # except:
    #    return

def plot(tupleList):
    import numpy as np
    import matplotlib.pyplot as plt


    #x = np.arange(0, 5, 0.1);
    #y = np.sin(x)
    #plt.plot(x, y)   
    x_val = [x[0] for x in tupleList]
    y_val = [x[1] for x in tupleList]

    #print x_val
    #plt.plot(x_val,y_val)
    #plt.show()
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter
    
    # the random data
   
    nullfmt = NullFormatter()         # no labels
    
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02
    
    rect_scatter = [left, bottom, width, height]
    #rect_histx = [left, bottom_h, width, 0.2]
    #rect_histy = [left_h, bottom, 0.2, height]
    
    # start with a rectangular Figure
    plt.figure(1, figsize=(8, 8))
    
    axScatter = plt.axes(rect_scatter)
    #axHistx = plt.axes(rect_histx)
    #axHisty = plt.axes(rect_histy)
    
    # no labels
    #axHistx.xaxis.set_major_formatter(nullfmt)
    #axHisty.yaxis.set_major_formatter(nullfmt)
    
    # the scatter plot:
    axScatter.scatter(x_val, y_val)
    
    # now determine nice limits by hand:
    binwidth = 0.25
    xymax = np.max([np.max(np.fabs(x_val)), np.max(np.fabs(y_val))])
    lim = (int(xymax/binwidth) + 1) * binwidth
    
    axScatter.set_xlim((-lim, lim))
    axScatter.set_ylim((-lim, lim))
    
    bins = np.arange(-lim, lim + binwidth, binwidth)
   # axHistx.hist(x, bins=bins)
    #axHisty.hist(y, bins=bins, orientation='horizontal')
    
   # axHistx.set_xlim(axScatter.get_xlim())
    #axHisty.set_ylim(axScatter.get_ylim())
    
    plt.show()
