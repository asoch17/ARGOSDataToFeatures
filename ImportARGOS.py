##---------------------------------------------------------------------
## ImportARGOS.py
##
## Description: Read in ARGOS formatted tracking data and create a line
##    feature class from the [filtered] tracking points
##
## Usage: ImportArgos <ARGOS folder> <Output feature class> 
##
## Created: Fall 2020
## Author: as986@duke.edu (for ENV859)
##---------------------------------------------------------------------
#%%
# Import modules
import sys, os, arcpy

arcpy.env.overwriteOutput = True

# Set input variables (user input)
inputFolder = arcpy.GetParameterAsText(0)
inputFiles = os.listdir(inputFolder)
outputFC = arcpy.GetParameterAsText(1)
outputSR = arcpy.GetParameterAsText(2)

## Prepare a new feature class to which we'll add tracking points
# Create an empty feature class; requires the path and name as separate parameters
outPath,outName = os.path.split(outputFC)
arcpy.CreateFeatureclass_management(outPath, outName, "POINT", "","","", outputSR)

# Add TagID, LC, IQ, and Date fields to the output feature class
arcpy.AddField_management(outputFC,"TagID","LONG")
arcpy.AddField_management(outputFC,"LC","TEXT")
arcpy.AddField_management(outputFC,"Date","DATE")

# Create the insert cursor
cur = arcpy.da.InsertCursor(outputFC,['Shape@','TagID','LC','Date'])

#iterate through each ARGOS file
inputFiles = os.listdir(inputFolder)
for inputFile in inputFiles:
    #don't process README.txt file
    if inputFile == "README.txt":
        continue

    #add full path to input file name
    inputFile_full = os.path.join(inputFolder, inputFile)

    #Construct a while loop to iterate through all lines in the datafile
    # Open the ARGOS data file for reading
    inputFileObj = open(inputFile_full,'r')
    
    # Get the first line of data, so we can use a while loop
    lineString = inputFileObj.readline()
    
    # Start the while loop
    while lineString:
        
        # Set code to run only if the line contains the string "Date: "
        if ("Date :" in lineString):
            
            # Parse the line into a list
            lineData = lineString.split()
            
            # Extract attributes from the datum header line
            tagID = lineData[0]
            obsDate = lineData[3]
            obsTime = lineData[4]
            obsLC = lineData[7]
            
            # Extract location info from the next line
            line2String = inputFileObj.readline()
            
            # Parse the line into a list
            line2Data = line2String.split()
            
            # Extract the date we need to variables
            obsLat = line2Data[2]
            obsLon= line2Data[5]
            
             # Print results to see how we're doing
           # print (tagID,"Lat:"+str(obsLat),"Long:"+str(obsLon),"Date:"+obsDate,"Time:"+obsTime,"LC:"+obsLC)
            
            #try to convert the coordinate numbers
            try:
            
                 # Convert raw coordinate strings to numbers
                if obsLat[-1] == 'N':
                    obsLat = float(obsLat[:-1])
                else:
                    obsLat = float(obsLat[:-1]) * -1
                if obsLon[-1] == 'E':
                    obsLon = float(obsLon[:-1])
                else:
                    obsLon = float(obsLon[:-1]) * -1
                    
                # Construct a point object from the feature class
                obsPoint = arcpy.Point()
                obsPoint.X = obsLon
                obsPoint.Y = obsLat
                
                # Convert the point to a point geometry object with spatial reference
                inputSR = arcpy.SpatialReference(4326)
                obsPointGeom = arcpy.PointGeometry(obsPoint,inputSR)
                
                 #add a feature using our insert cursor
                feature = cur.insertRow((obsPointGeom,tagID,obsLC,obsDate.replace(".","/") + " " + obsTime))
    
            #handle the error
            except Exception as e:
                arcpy.AddWarning(f"Error adding record {tagID} to the output")
            
        # Move to the next line so the while loop progresses
        lineString = inputFileObj.readline()
        
    #Close the file object
    inputFileObj.close()

#Delete the cursor object
del cur