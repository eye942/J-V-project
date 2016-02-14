# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:21:08 2016

@author: Eric
"""

# -*- coding: utf-8 -*-
import pdb

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
    '''Creates the Data class. Takes a text log and analyzes it.
    '''
    def __init__(self, directory = 'C:\\Users\\jye\\Desktop', file_name = 'opv_Friday_d1  151014-172247.txt' ):
        import re
        from dateutil import parser
        
        self.fileName = file_name
        self.directory = directory
        self.rawList = loadList(directory, file_name)
        self.numList = splitTab(self.rawList)
        self.parsedList = []
        matchObj = re.match("(?P<device>.+)  (?P<time>.+)\.txt", file_name)
        self.device = matchObj.group("device")
        time = parser.parse(matchObj.group("time"))
        self.date = time.date()
        self.time= time.time()        
        p = re.compile('\\\\')
        test_str = self.directory
        subst = "/"
        self.forwardDir = re.sub(p, subst, test_str)
        power = [-x[0]*x[1] for x in self.numList]
        self.maxPower = max(power)

    
    def plot(self, write = 'n'):
        import matplotlib.pyplot as plt
        import numpy as np
        
        x_val = [x[0] for x in self.numList]
        y_val = [x[1] for x in self.numList]
        
        # definitions for the axes
        left, width = 0.1, 0.65
        bottom, height = 0.1, 0.65
    
        rect_scatter = [left, bottom, width, height]
        
        # start with a rectangular Figure
        fig = plt.figure(1, figsize=(8, 8))
        
        axScatter = plt.axes(rect_scatter)
        
        # the scatter plot:
        axScatter.scatter(x_val, y_val)
        
        # now determine nice limits by hand:        
        axScatter.set_xlim(min(x_val) - min(np.absolute(x_val))  , max(x_val) + min(np.absolute(x_val)))
        axScatter.set_ylim(min(y_val) - min(np.absolute(y_val)) , max(y_val) + min(np.absolute(y_val)))

        # label of axes        
        fig.suptitle('J-V curve: ' + self.fileName, fontsize = 25)# + Data.parsedList[0])
        plt.xlabel("Voltage(V)", fontsize = 12)
        plt.ylabel("Current (mA)", fontsize = 12)
        
        # setting of axes
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        
        #saving
        if write == 'y':
            try:
                plt.savefig(self.directory + "/" + self.fileName[0:-4] +'.jpg')
            
            except:
                print "Can't save graph"
        
        
        plt.show()

        #Image.open('testplot.png').save('testplot.jpg','JPEG')

    def parseFields(self):
        import re
        #import pdb
        rawList = self.rawList
        for linestr in rawList:

            #Eliminate redundancy for the plot points
            if linestr.find("\t") >= 0:
                pass
            #Check for all colons in the line
            x = [m.start() for m in re.finditer(': ', linestr)]
            
            #Separates the line into two if there is only one colon
            if len(x) == 1:
                self.parsedList.append(re.split(": ", linestr))

            """elif linestr[:index] == 'Description':
                self.parsedList.append(['Description', linestr[index+2:]])
            elif linestr[:index] == 'Area':
                self.parsedList.append(['Area', linestr[index+2:]])
            elif linestr[:index] == 'Block':
                self.parsedList.append(['Block', linestr[index+2:]])
            elif linestr[:index] == 'Carrier':
                self.parsedList.append(['Carrier', linestr[index+2:]])
            elif linestr[:index] == 'Device':
                self.parsedList.append(['Device', linestr[index+2:]])
            elif linestr[:index] == 'LB device':
                self.parsedList.append(['LB device', linestr[index+2:]])"""
            
            #Take out the abnormal time string: added into parsed list
            if linestr.find('Measured on') > -1:
                self.parsedList.append(['Test Time', linestr[13:]])
            
            #Need to be replaced with more robust code @made a little better
            match = re.search(" ?SPA system IV test:  IV test type: basic ?", linestr)
            if match:
                x = re.compile("SPA system IV test:  IV test type: (?P<test_type>.+)  Recipe:  (?P<Recipe>.+)")
                y = re.match(x, linestr)
                test = ["IV test type", y.group("test_type")]
                recipe = ["Recipe", y.group("Recipe")]
                self.parsedList.append(["SPA system IV test", [test, recipe]])
           
            #Takes in sensor properties: appends the dictionary form as a list
            match = re.search("Sensor:", linestr)
            if match:
                sensorProp = re.match("Sensor: (?P<Sensor>.+) Value: (?P<Value>.+) Units: (?P<Units>.+) Channel: (?P<Channel>.+) Area: (?P<Area>.+) Block: (?P<Block>.+) ",linestr)
                dictList = []
                sensorDict = sensorProp.groupdict()
                sensorName = sensorProp.groupdict().pop("Sensor")
                for key, value in sensorDict.iteritems():
                    temp = [key,value]
                    dictList.append(temp)                
                
                self.parsedList.append([sensorName, dictList])
            
            #Need to be replaced with more robust code
            match = re.search("Recipe Settings: Source mode", linestr)
            if match:
                x = re.match(".+Source mode:(?P<Source_mode>.+)", linestr)
                y= x.group("Source_mode")
                self.parsedList.append(["Source Mode", y])
            
            #Puts Limit Level into the parsed list
            match = re.search("Limit Level", linestr)
            if match:
                p = re.match(".+Limit Level(?P<LimLev>.+)", linestr)
                if p:        
                    self.parsedList.append(["Limit Level", p.group("LimLev")])
                else:
                    print "Could not incorporate Limit Level into the list"                     
           
            #Puts Delay in Seconds into the parsed list          
            match = re.search("Delay in Sec", linestr)
            if match:
                p = re.compile('.+Delay in Sec (?P<DiS>.+)')
                x = re.match(p, linestr)
                
                self.parsedList.append(["Delay in Sec", x.group("DiS")])

            #Puts Measurement into the parsed list
            match = re.search("Mesurement Speed (PLC)", linestr);
            if match:
                p = re.compile(' Mesurement Speed.+ (.+)') 
                mesSpeed = re.search(p, linestr)
                
                self.parsedList.append(["Mesurement Speed (PLC)", mesSpeed])
             
            match = re.search("Sweep Points", linestr)
            if match:
                sweepPnt = re.match(" Sweep Points:  Start (?P<Start>.+) Stop (?P<Stop>.+) Number of Points  (?P<NumPoints>.+)", linestr)
                sweepDict = sweepPnt.groupdict()
                dictList = []
                for key, value in sweepDict.iteritems():
                    temp = [key,value]
                    dictList.append(temp)
                self.parsedList.append(["Sweep Points", dictList] )
        
        
        
    def createHDF5(self, saveLoc = 'C:/Users/Eric/Desktop/J-V/Test/Hdf5', overwrite = "y"): 
        #Author: Yash Pershad
        #Date: 1/12/2016
        #Makes an hdf5 file with the same name as the txt file from which data is organized
        #need to input file location and save location
        import re    
        import os    
        import h5py
        import numpy as np
        
        if not os.path.exists(saveLoc):
            os.makedirs(saveLoc)
                
        if os.name == "nt":
            slash = "\\"
        elif os.name == "posix":
            slash = "/"
        
        fileName = self.fileName        
                
        saveName = re.findall('[^.]*',fileName)[0]+'.hdf5'
        
            
        try:
            saveData=h5py.File(saveLoc + "/" +saveName,'w-')
            willsave='y'
            print('Creating file '+ saveName)
        except:
            print(saveLoc + slash + saveName + ' already exists')
            if overwrite=='y':
                os.remove(saveLoc + "/" + saveName)
                saveData=h5py.File(saveLoc + "/" + saveName,'w-')
                willsave='y'
                print('Overwriting')
            else:
                willsave='n'
                print('Leaving old data')
        f = saveData.create_group('Data')
        g = saveData.create_group('/Data/Attrbs')
        #dSetV = f.create_dataset("Voltage", np.array(self.voltage))
        #dSetC = f.create_dataset("Current", np.array(self.current))
        arr = np.array(self.numList)
        dSetPlot = f.create_dataset("Plot Points", data = arr)        
        for x in self.parsedList:
            #try:
            if len(x) == 2:
                if isinstance(x[1], list):
                    h = g.create_group(x[0])
                    for e in x[1]:
                        h[e[0]] = e[1]        
                else:
                    saveData["Data"].attrs[x[0]] = np.string_(x[1])                        
                #xcept:
                
                #print

        return saveData
    
#def splitString(string, index):
 #   try:
  #      return [float(string[:index]), float(string[index+1:])]
   # except:
    #    return
    


def closeHdf5():
    import h5py    
    import gc
    print "Closing objects"
    for obj in gc.get_objects():   # Browse through ALL objects
        if isinstance(obj, h5py.File):   # Just HDF5 files
            try:
                obj.close()
            except:
                pass # Was already closed
                
def unifyHdf5(directory, saveLoc, overwrite = 'y'):
       
    import os    
    import h5py
    import numpy as np
    #Check whether the saveLocation exists.
    if not os.path.exists(saveLoc):
        os.makedirs(saveLoc)
            
    listDir = os.listdir(directory)
    nameDict = {} 
    
    #Stores each text file ass a Data object in a dictionary keyed by device name
    for txtFile in listDir:
        if txtFile[-4:] == ".txt":
            name = Data(directory, txtFile)
            name.parseFields()
            dName = name.device
            if dName in nameDict:
                #pdb.set_trace()
                #nameDict[dName] = 
                nameDict[dName].append(name)
                #pass
            else:
                #pdb.set_trace()
                nameDict[dName] = [name]      

    print("Finished writing data to memory")
    #Create a file for each device. Has a hierarchy of Date, time, Attribute
    for key in nameDict:
        #Creates a         
        try:
            saveData=h5py.File(saveLoc + "/" + key,'w-')
            willsave='y'
            print('Creating file '+ key)
        except:
                print(saveLoc + "/" + key + ' already exists')
                if overwrite=='y':
                    os.remove(saveLoc + "/" + key)
                    saveData=h5py.File(saveLoc + "/" + key,'w-')
                    willsave='y'
                    print('Overwriting')
                else:
                    willsave='n'
                    print('Leaving old data')

        f = saveData.create_group(key)
        for point in nameDict[key]:
            g = f.create_group(str('/'+ str(point.date) + '/' + str(point.time)))
            try:
                arr = np.array(point.numList)
                dSetPlot = g.create_dataset("Plot Points", data = arr)
            except:
                pass
            attribs = g.create_group("Attributes")
            for x in point.parsedList:
                #try:
                if len(x) == 2:
                    if isinstance(x[1], list):
                        h = attribs.create_group(x[0])
                        for e in x[1]:
                            h[e[0]] = e[1]        
                    else:
                        g.attrs[x[0]] = np.string_(x[1])                        
            g.attrs["Misc"] = attribs.ref
            print point
        print("The device, " + key + ", is finished.")
        saveData.close()
    
        
def appendHDF5(root, addFile):
    import h5py
    import np    
    
    x = addFile.rfind("/")
    newData = Data(addFile[:x], addFile[x+1:])
    
    dataSet = h5py.File(root, 'w')
    key = newData.device
    
    f = newData.create_group(key)
    g = f.create_group(str('/'+ str(newData.date) + '/' + str(newData.time)))
    try:
        arr = np.array(newData.numList)
        dSetPlot = g.create_dataset("Plot Points", data = arr)
    except:
        pass
    attribs = g.create_group("Attributes")
    for x in newData.parsedList:
        #try:
        if len(x) == 2:
            if isinstance(x[1], list):
                h = attribs.create_group(x[0])
                for e in x[1]:
                    h[e[0]] = e[1]        
            else:
                g.attrs[x[0]] = np.string_(x[1])                        
    g.attrs["Misc"] = attribs.ref
    print("The device, " + key + ", is finished.")
    dataSet.close()    

def openFiles(directory = 'C:\Users\Eric\Desktop', saveLoc = "C:\Users\Eric\Desktop\J-V\test\hdf5"):
    import os
    
    if not os.path.exists(saveLoc):
        os.makedirs(saveLoc)
    
    listDir = os.listdir(directory)
    if os.name == "nt":
        slash = "\\"
    elif os.name == "posix":
        slash = "/"
    """:
        print "Weird OS alert!"
        directory = input("Where are your files? Include any slashes")"""
    for fileName in listDir:
        
        #Is it a hdf5?
        if fileName[-4:]== ".txt":
            data = Data(directory, fileName)
            data.parseFields()
            if slash == "\\":
                data.createHDF5(directory)
            elif slash == "/":
                data.createHDF5(data.directory + "/hdf5/" + fileName[-4:] +".hdf5")
                
def plotDevice( directory = "C:\Users\jye\Desktop", deviceName = "opv_Friday_d1", write = 'n'):
    import os
    import h5py
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np
    import matplotlib.colors as color
    from itertools import cycle
     
    listDir = os.listdir(directory)

    #Account for file system
    if os.name == "nt":
        slash = "\\"
    elif os.name == "posix":
        slash = "/"
    
    plotPoints = []    
    count = 0
    length = len(listDir)
    '''#coloring the plot'''
    x = np.arange(length)
    colors = iter(cm.rainbow(np.linspace(0, 1, length)))
    rainbow = ["r", "orange","Yellow", "B",  "Violet"]    
    colorWow = cycle(rainbow)
    
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65

    rect_scatter = [left, bottom, width, height]
    
    # start with a rectangular Figure
    fig = plt.figure(1, figsize=(8, 8))
    
    axScatter = plt.axes(rect_scatter)
    
    for fileName in listDir:        
        #Is it a hdf5?
        if fileName[-5:]== ".hdf5":

            if slash == "/":
                temp = h5py.File(directory + slash + fileName,"r")
            elif slash == "\\":
                temp = h5py.File(directory + slash + fileName, "r")
            else:
                print "Congrats on having a different computer. Please try again on a Unix-based or Windows OS"

            if temp["Data"].attrs.get("Device Name") == deviceName:
                try:
                    voltage = [y[0] for y in temp["Data"]["Plot Points"][:]]
                    current = [y[1] for y in temp["Data"]["Plot Points"][:]]
                    # the scatter plot:
                    axScatter.scatter(voltage, current, color = next(colors))
                    count+=1

                except:
                    pdb.set_trace()
    
    print(count)
    
    # label of axes        
    fig.suptitle('Aggregate J-V curve: ' + deviceName, fontsize = 25)
    plt.xlabel("Voltage(V)", fontsize = 12)
    plt.ylabel("Current (mA)", fontsize = 12)

    
    # setting of axes
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

        
    #saving
    if write == 'y':
        try:
            plt.savefig(directory + slash + "figs" + slash + deviceName +'.jpg')
        
        except:
            print "Can't save graph"
    plt.show()
'''def plotFigure(fileLoc):
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
    from mpl_toolkits.axes_grid1.inset_locator import mark_inset
    import h5py
    
    data = h5py.File(fileLoc, 'r')
    
    x_val = [x[0] for x in data['Data']["Plot Points"][:]]
    y_val = [-x[1] for x in data['Data']["Plot Points"][:]]
    
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65

    rect_scatter = [left, bottom, width, height]
    
    rectTotal = [left+width + width,bottom, left+width+width+width, bottom + height]
    
    # start with a rectangular Figure
    fig = plt.figure(1, figsize=(8, 8))
    
    axScatter = plt.subplot(111)
    plt.xlabel("Voltage(V)", fontsize = 12)
    plt.ylabel("Current (mA)", fontsize = 12)
    
    

    
    # the scatter plot:
    axScatter.scatter(x_val, y_val)
    
    # now determine limits by hand:        

    axins = zoomed_inset_axes(axScatter, 6, loc=1)
    x1, x2, y1, y2 = -1.5, -0.9, -2.5, -1.9
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)

    axins1 = zoomed_inset_axes(axScatter, 8, loc=2) # zoom = 6
    axins1.scatter(x_val, y_val)

    
    x = fileLoc.rfind("/")
    # label of axes        
    fig.suptitle('J-V curve: ' + fileLoc[x+1:], fontsize = 25)# + Data.parsedList[0])
    
    
    # setting of axes
    axScatter.axhline(0, color='black')
    axScatter.axvline(0, color='black')
    
    #saving
    if write == 'y':
        try:
            plt.savefig(self.directory + "/" + self.fileName[0:-4] +'.jpg')
        
        except:
            print "Can't save graph"
    

    maxPower = data['Data'].attrs['Max Power']
    isc = data['Data'].attrs['Isc']
    voc = data['Data'].attrs['Voc']
    textstr = '$\mathrm{Max Power}$=%.3e\n$I_{sc}$=%.2f\n$V_{oc}$=%.2f'%(maxPower, isc, voc)

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    axScatter.text( 3, 3, textstr, transform= axScatter.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

    
    plt.show()'''

def plotFigure(fileLoc):
    import numpy as np
    import matplotlib.pyplot as plt
    import h5py
    
    data = h5py.File(fileLoc, 'r')
    
    x_val = [x[0] for x in data['Data']["Plot Points"][:]]
    y_val = [-x[1] for x in data['Data']["Plot Points"][:]]
    maxPower = data['Data'].attrs['Max Power']
    isc = data['Data'].attrs['Isc']
    voc = data['Data'].attrs['Voc']
    fillFactor = data['Data'].attrs['Fill Factor']
    textstr = '$\mathrm{Power_{Max}}$=%.3e\n$I_{sc}$=%.3e\n$V_{oc}$=%.3e\n$\mathrm{FF}$=%.3f'%(maxPower, isc, voc, fillFactor)

    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)


    # start with a rectangular Figure
    fig = plt.figure(1, figsize=(8, 8))
    
    axScatter = plt.subplot(221)
    plt.xlabel("Voltage(V)", fontsize = 12)
    plt.ylabel("Current (mA)", fontsize = 12)
    ax2 = plt.subplot(212)
    # place a text box in upper left in axes coords
    plt.figtext(.7, .7, textstr, horizontalalignment='center', verticalalignment='center', transform=axScatter.transAxes,
                bbox=props, visible=True)

    
    # the scatter plot:
    axScatter.scatter(x_val, y_val)
    ax2.scatter(x_val, y_val)    
    
    # now determine limits by hand:        
    ax2.set_xlim(0  , max(x_val) + min(np.absolute(x_val)))
    ax2.set_ylim(0 , max(y_val) + min(np.absolute(y_val)))
    
    

    
    x = fileLoc.rfind("/")
    # label of axes        
    fig.suptitle('J-V curve: ' + fileLoc[x+1:], fontsize = 25)# + Data.parsedList[0])
    
    
    # setting of axes
    axScatter.axhline(0, color='black')
    axScatter.axvline(0, color='black')
    
    #saving
    #if write == 'y':
     #   try:
      #      plt.savefig(self.directory + "/" + self.fileName[0:-4] +'.jpg')
       # 
        #except:
          #  print "Can't save graph"
    



    zoom_effect02(ax2, axScatter)

    data.close()
    plt.show()

    
def plotDeviceHdf5(fileDir, write = 'n'):
    import h5py
    import os
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np


    #Account for file system
    if os.name == "nt":
        slash = "\\"
    elif os.name == "posix":
        slash = "/"
    try:
        device = h5py.File(fileDir, "r")
    except:
        x = input("Try another file directory. Include file extenstion if applicable.")
        plotDeviceHdf5(x, write)
        return
    
    
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    rect_scatter = [left, bottom, width, height]
    fig = plt.figure(1, figsize=(8, 8))
    axScatter = plt.axes(rect_scatter)
    
    count = 0
    for day in device.keys():
        try:        
            for time in device[day]:                
                count+=1
        except:
            pass

    colors = iter(cm.rainbow(np.linspace(0, 1, count)))
    

           
    #Iterate through file to plot scatter points
    for day in device.keys():
        try:        
            for time in device[day]:
                try:
                    voltage = [y[0] for y in device[day][time][:]]
                    current = [y[1] for y in device[day][time][:]]
                    # the scatter plot:
                    axScatter.scatter(voltage, current, color = next(colors))
                except:
                    pdb.set_trace()
        except:
            pass
    
    #Labeling axes            
    fig.suptitle('Aggregate J-V curve: ' + device.keys()[-1], fontsize = 15)
    plt.xlabel("Voltage(V)", fontsize = 12)
    plt.ylabel("Current (mA)", fontsize = 12)

    
    # setting of axes
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

        
    #saving
    if write == 'y':
        try:
            plt.savefig(saveLoc+ slash + deviceName +'.jpg')
        
        except:
            print "Can't save graph"
    
    #Print plot
    plt.show()

def plotDevice( directory = "C:\Users\jye\Desktop", deviceName = "opv_Friday_d1", write = 'n'):
    import os
    import h5py
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm
    import numpy as np
    import matplotlib.colors as color
    from itertools import cycle
     
    listDir = os.listdir(directory)

    #Account for file system
    if os.name == "nt":
        slash = "\\"
    elif os.name == "posix":
        slash = "/"
    
    plotPoints = []    
    count = 0
    length = len(listDir)
    '''#coloring the plot'''
    x = np.arange(length)
    colors = iter(cm.rainbow(np.linspace(0, 1, length)))
    rainbow = ["r", "orange","Yellow", "B",  "Violet"]    
    colorWow = cycle(rainbow)
    
    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65

    rect_scatter = [left, bottom, width, height]
    
    # start with a rectangular Figure
    fig = plt.figure(1, figsize=(8, 8))
    
    axScatter = plt.axes(rect_scatter)
    
    for fileName in listDir:        
        #Is it a hdf5?
        if fileName[-5:]== ".hdf5":

            if slash == "/":
                temp = h5py.File(directory + slash + fileName,"r")
            elif slash == "\\":
                temp = h5py.File(directory + slash + fileName, "r")
            else:
                print "Congrats on having a different computer. Please try again on a Unix-based or Windows OS"

            if temp["Data"].attrs.get("Device Name") == deviceName:
                try:
                    voltage = [y[0] for y in temp["Data"]["Plot Points"][:]]
                    current = [y[1] for y in temp["Data"]["Plot Points"][:]]
                    # the scatter plot:
                    axScatter.scatter(voltage, current, color = next(colors))
                    count+=1

                except:
                    pdb.set_trace()
    
    print(count)
    
    # label of axes        
    fig.suptitle('Aggregate J-V curve: ' + deviceName, fontsize = 25)
    plt.xlabel("Voltage(V)", fontsize = 12)
    plt.ylabel("Current (mA)", fontsize = 12)

    
    # setting of axes
    plt.axhline(0, color='black')
    plt.axvline(0, color='black')

        
    #saving
    if write == 'y':
        try:
            plt.savefig(directory + slash + "figs" + slash + deviceName +'.jpg')
        
        except:
            print "Can't save graph"
    plt.show()
    


def getISC(fileLoc):
    import numpy as np
    import h5py
    
    hdf5 = h5py.File(fileLoc, "r+")
    points = hdf5["Data"]["Plot Points"][:]
    index = np.array([[np.abs(y[0])] for y in points]).argmin()
    isc = points[index][1]    
    hdf5["Data"].attrs['Isc'] = abs(isc)
    print abs(isc)
    hdf5.close()
 
def getVOC(fileLoc):
    import numpy as np
    import h5py
    
    hdf5 = h5py.File(fileLoc, "r+")
    points = [[y[0], -y[1]]for y in hdf5["Data"]["Plot Points"][:]]
    posList = []
    negList = []   
    for y in points:
        if y[1] > 0:
            posList.append(y)
        else:
            negList.append(y)
            
    posList = [[y[1],y[0]] for y in posList]
    negList = [[y[1],y[0]] for y in negList]

    indX = np.array([[np.abs(y[0])] for y in posList]).argmin()
    closePos = posList[indX]
    indY = np.array([[np.abs(y[0])] for y in negList]).argmin()
    closeNeg = negList[indY]    
    slope = (closePos[1] - closeNeg[1])/(closePos[0] - closeNeg[0])
    b = closePos[1] - (slope * closePos[0])
    hdf5["Data"].attrs['Voc'] = b    
    print b
    hdf5.close()

def getFillFactor(fileLoc):
    import numpy as np
    import h5py

    hdf5 = h5py.File(fileLoc, "r+")
    power = hdf5["Data"].attrs['Max Power']
    isc = hdf5["Data"].attrs['Isc']
    voc = hdf5["Data"].attrs['Voc']
    bigPower = isc*voc
    fillFactor = power/bigPower
    hdf5["Data"].attrs['Fill Factor'] = fillFactor
    print abs(fillFactor)
    hdf5.close()
    
def findMaxPower(fileloc):
    import numpy as np
    import h5py
    hdf5 = h5py.File(fileloc, 'r+')
    power = [-y[0]*y[1] for y in hdf5['Data']['Plot Points'][:]]
    maxPower = np.amax(power)
    hdf5["Data"].attrs['Max Power'] = maxPower
    print(maxPower) 
    hdf5.close()

#Functions for convenient testing
def main(close = 'y'):
    dataTest = Data()
    #dataTest = Data()
    #import pandas
    
    dataTest.parseFields()
    print dataTest.parsedList
    #try:    
    saveData = dataTest.createHDF5(dataTest.forwardDir)
    #except:
     #   print "Could not generate HDF5 file
    print saveData.items()

    dataTest.plot('y')
        # except:
    if close == 'y':
        closeHdf5()
        
# imported Libraries from matplotlib
from matplotlib.transforms import Bbox, TransformedBbox, \
    blended_transform_factory

from mpl_toolkits.axes_grid1.inset_locator import BboxPatch, BboxConnector,\
    BboxConnectorPatch


def connect_bbox(bbox1, bbox2,
                 loc1a, loc2a, loc1b, loc2b,
                 prop_lines, prop_patches=None):
    if prop_patches is None:
        prop_patches = prop_lines.copy()
        prop_patches["alpha"] = prop_patches.get("alpha", 1)*0.2

    c1 = BboxConnector(bbox1, bbox2, loc1=loc1a, loc2=loc2a, **prop_lines)
    c1.set_clip_on(False)
    c2 = BboxConnector(bbox1, bbox2, loc1=loc1b, loc2=loc2b, **prop_lines)
    c2.set_clip_on(False)

    bbox_patch1 = BboxPatch(bbox1, **prop_patches)
    bbox_patch2 = BboxPatch(bbox2, **prop_patches)

    p = BboxConnectorPatch(bbox1, bbox2,
                           # loc1a=3, loc2a=2, loc1b=4, loc2b=1,
                           loc1a=loc1a, loc2a=loc2a, loc1b=loc1b, loc2b=loc2b,
                           **prop_patches)
    p.set_clip_on(False)

    return c1, c2, bbox_patch1, bbox_patch2, p

def zoom_effect02(ax1, ax2, **kwargs):
    """
    ax1 : the main axes
    ax1 : the zoomed axes

    Similar to zoom_effect01.  The xmin & xmax will be taken from the
    ax1.viewLim.
    """

    tt = ax1.transScale + (ax1.transLimits + ax2.transAxes)
    trans = blended_transform_factory(ax2.transData, tt)

    mybbox1 = ax1.bbox
    mybbox2 = TransformedBbox(ax1.viewLim, trans)

    prop_patches = kwargs.copy()
    prop_patches["ec"] = "none"
    prop_patches["alpha"] = 0.2

    c1, c2, bbox_patch1, bbox_patch2, p = \
        connect_bbox(mybbox1, mybbox2,
                     loc1a=3, loc2a=2, loc1b=4, loc2b=1,
                     prop_lines=kwargs, prop_patches=prop_patches)

    ax1.add_patch(bbox_patch1)
    ax2.add_patch(bbox_patch2)
    ax2.add_patch(c1)
    ax2.add_patch(c2)
    ax2.add_patch(p)

    return c1, c2, bbox_patch1, bbox_patch2, p

