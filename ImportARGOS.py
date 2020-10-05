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

# Import modules
import sys, os, arcpy

# Set input variables (Hard-wired)
inputFile = 'D:/AdvGIS/ARGOSTracking/Data/ARGOSData/1997dg.txt'
outputFC = "D:/AdvGIS/ARGOSTracking/Scratch/ARGOStrack.shp"

