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
        
        self.fileName = file_name
        self.directory = directory
        self.rawList = loadList(directory, file_name)
        self.numList = splitTab(self.rawList)
        self.parsedList = []
        self.voltage = [[x[0], 0] for x in self.numList]
        self.current = [[x[1], 1] for x in self.numList]
        p = re.compile('\\\\')
        test_str = self.directory
        subst = "/"
        self.forwardDir = re.sub(p, subst, test_str)

    
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
        
        
        
    def createHDF5(self, saveLoc = 'C:/Users/Eric/Desktop', overwrite = "y"): 
        #Author: Yash Pershad
        #Date: 1/12/2016
        #Makes an hdf5 file with the same name as the txt file from which data is organized
        #need to input file location and save location
        import re    
        import os    
        import h5py
        fileName = self.fileName
        space = re.compile(" ")
        fileName = space.sub("_", fileName)
        
                
        saveName = re.findall('[^.]*',fileName)[0]+'.hdf5'
            
        try:
            saveData=h5py.File(saveLoc + '/' + saveName,'w-')
            willsave='y'
            print('Creating file '+saveName)
        except:
            print(saveLoc+' already exists')
            if overwrite=='y':
                os.remove(saveLoc+ "/" + saveName)
                saveData=h5py.File(saveName,'w-')
                willsave='y'
                print('Overwriting')
            else:
                willsave='n'
                print('Leaving old data')
        saveData.create_group('Data')
        for x in self.parsedList:
            try:
                if len(x) == 2:
                    if isinstance(x[1], list):
                        saveData.create_group(str(x[0]))
                        for e in x[1]:
                            saveData[str(x[0])][str(e[0])] = str(e[1])
                    else:
                        saveData[str(x[0])] = str(x[1])                        
            except:
                pass
            
        saveData["Voltage"] = self.voltage
        saveData["Current"] = self.current
        saveData["Plot Points"] = self.numList
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
    

def openFiles(directory = 'C:\Users\jye\Desktop'):
    import os
    
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
                data.createHDF5(data.directory)
            elif slash == "/":
                data.createHDF5(data.directory + "/" + "hdf5" + fileName[-4:] +".hdf5")

def plotDevice( directory = "C:\Users\jye\Desktop", deviceName = "opv_Friday_d1", write = 'n'):
    import os
    import h5py
    import matplotlib.pyplot as plt
    import numpy as np
    
    listDir = os.listdir(directory)

    #Account for file system
    if os.name == "nt":
        slash = "\\"
    elif os.name == "posix":
        slash = "/"
    
    plotPoints = []    
    count = 0    
    
    for fileName in listDir:        
        #Is it a hdf5?
        if fileName[-5:]== ".hdf5":

            if slash == "/":
                temp = h5py.File(directory + slash + fileName,"r")
            elif slash == "\\":
                temp = h5py.File(directory + slash + fileName, "r")
            

            
            else:
                print "Congrats on having a different computer. Please try again on a Unix-based or Windows OS"

            if temp["Device Name"].value == deviceName:
                try:                
                    plotPoints = plotPoints + temp["Plot Points"].value.tolist()  
                    count += 1
                except:
                    pdb.set_trace()
                    
