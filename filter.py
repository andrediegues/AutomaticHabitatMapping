from __future__ import division
import sys
import csv
import libraries
    
def main():
    if len(sys.argv) < 2:
        print "Please provide a CSV file to filter\n\n  python filter.py [.csv file]"
        sys.exit(1)

    inputfile = open(sys.argv[1], "r")
    dataset = csv.reader(inputfile)
    rows = [row for row in dataset]
    desiredPitch = 7.2
    desiredRoll = 7.2
    bottomLimAltitude = 1.5
    upperLimAltitude = 3
    
    wantedRows = libraries.getWantedRowsFromCSVFile(rows, desiredPitch, desiredRoll, bottomLimAltitude, upperLimAltitude)
    
    newDir = libraries.copyWantedRowFilesToMRADir(wantedRows, sys.argv[1])
    
    print "File filtered with pitch = " + str(desiredPitch) + ", roll = " + str(desiredRoll) + " and altitude between " + str(bottomLimAltitude) + " and " + str(upperLimAltitude) + ", which resulted in " + str(len(wantedRows)) + " rows and " + str(round(len(wantedRows) / len(rows) * 100,2)) + " % of data from the original dataset"

    answer = raw_input("Do you want to equalize this pictures with the CLAHE algorithm? [Y/n]")
    if "n" not in answer:
        libraries.extractAndCompileCLAHEFiles(newDir)
        libraries.executeCLAHEAlgorithm(newDir, wantedRows)
        libraries.removeNormalFiles(newDir, wantedRows)
    else:
        print "exiting..."
        
    sys.exit(0)
        
if __name__ == "__main__":
    main()
