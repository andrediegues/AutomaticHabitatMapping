from __future__ import division
import sys
import csv
import os
import libraries
    
def main():
    if len(sys.argv) < 2:
        print "Please provide a CSV file to filter\n\n  python filter.py [.csv file]"
        sys.exit(1)
    filepath = sys.argv[1]
    if not os.path.isabs(filepath):
        filepath = os.path.abspath(filepath)
    inputfile = open(filepath, "r")
    dataset = csv.reader(inputfile)
    rows = [row for row in dataset]
    desiredPitch = 7.2
    desiredRoll = 7.2
    bottomLimAltitude = 1.5
    upperLimAltitude = 3
    
    wantedRows = libraries.getWantedRowsFromCSVFile(rows, desiredPitch, desiredRoll, bottomLimAltitude, upperLimAltitude)
    
    newDir = libraries.copyWantedRowFilesToMRADir(wantedRows, filepath)
    print "File filtered with pitch = " + str(desiredPitch) + ", roll = " + str(desiredRoll) + " and altitude between " + str(bottomLimAltitude) + " and " + str(upperLimAltitude) + ", which resulted in " + str(len(wantedRows)) + " rows and " + str(round(len(wantedRows) / len(rows) * 100,2)) + " % of data from the original dataset"

    libraries.extractAndCompileCLAHEFiles(newDir)
    libraries.executeCLAHEAlgorithm(newDir, wantedRows)
    libraries.organizeDirectory(newDir)
    
    print "exiting..."
    sys.exit(0)
        
if __name__ == "__main__":
    main()
