# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 12:02:48 2016

@author: Eric
"""

def loadList(directory, file_name):
    filePath = directory + "/" + file_name
    
    with open(filePath, 'r') as infile:
        data = infile.read()  # Read the contents of the file into memory.

    # Return a list of the lines, breaking at line boundaries.
    return data.splitlines()
    
def splitTab(dataList):
    
    stringList = []
    for line in dataList:
        if line.find("\t") > -1:
            tab = line.find("\t")
            try:
                if float(line[:tab]) != None:               
                    x = [float(line[:tab]), float(line[tab+1:])]
                    stringList.append(x)
            except:
                pass
    return stringList

class Data(object):
    def __init__(self, directory = 'C:/Users/Eric/Dropbox/J-V/test', file_name = 'opv_Friday_d1  151014-170349.txt' ):
        self.rawList = loadList(directory, file_name)
        self.numList = splitTab(self.rawList)
        self.parsedList = []
    


def parseFields(Data):
    from dateutil.parser import parse
    import string

    for line in Data.rawList:
        index = line.find(":")
        if line.find("\t") >= 0:
            pass
        elif line[:index] is 'Device Name:':
            Data.parsedList.append(['Device Name', line[index+2:]])
        elif line[:index] is 'Description':
            Data.parsedList.append(['Description', line[index+2:]])
        elif line[:index] is 'Area':
            Data.parsedList.append(['Area', line[index+2:]])
        elif line[:index] is 'Block':
            Data.parsedList.append(['Block', line[index+2:]])
        elif line[:index] is 'Carrier':
            Data.parsedList.append(['Carrier', line[index+2:]])
        elif line[:index] is 'Device':
            Data.parsedList.append(['Device', line[index+2:]])
        elif line[:index] is 'LB device':
            Data.parsedList.append(['LB device', line[index+2:]])
        elif line.find('Measured on') > -1:
            Data.parsedList.append(['Test Time', parse(line[14:])])
        elif line.find("### Sensor Readings") != -1:
            while index > -1:
                index = line.find(":")
                for x in string.uppercase:
                    try:
                        firstCap = line[:index].rFind(x)
                        break
                y = [firstCap, str()]
                line = line[index:]
                return y
                
        else:
            pass

#def splitString(string, index):
 #   try:
  #      return [float(string[:index]), float(string[index+1:])]
   # except:
    #    return

def plot(tupleList):
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.ticker import NullFormatter

    #x = np.arange(0, 5, 0.1);
    #y = np.sin(x)
    #plt.plot(x, y)   
    x_val = [x[0] for x in tupleList]
    y_val = [x[1] for x in tupleList]

    #print x_val
    #plt.plot(x_val,y_val)
    #plt.show()

    
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
