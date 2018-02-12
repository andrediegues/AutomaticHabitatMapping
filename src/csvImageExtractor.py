import sys
import csv
import os
import math
import shutil

def getWantedRowsFromCSVFile(rows, desiredPitch, desiredRoll, bottomLimAltitude, upperLimAltitude):
    wantedRows = []
    for row in rows[1:]:
        pitch = float(row[7])
        roll = float(row[6])
        altitude = float(row[4])
        if math.fabs(pitch) <= desiredPitch and math.fabs(roll) <= desiredRoll and math.fabs(altitude) >= bottomLimAltitude and math.fabs(altitude) <= upperLimAltitude:
            wantedRows.append(row[0])
    return wantedRows

def copyWantedRowFilesToMRADir(wantedRows, path):
    photosFolderLS = path.split("/")
    newDir = "/".join(photosFolderLS[:-2]) + "/FilteredPhotos/Original"
    if not os.path.exists(newDir):  
        os.makedirs(newDir)
        
    photosPath = "/".join(photosFolderLS[:-3]) + "/Photos"
    listOfPhotoDirs = os.listdir(photosPath)
   
    i = 0
    for filename in sorted(wantedRows):
        for photodir in sorted(listOfPhotoDirs):
            listOfFiles = os.listdir(photosPath + "/" + photodir + "/")
            for f in sorted(listOfFiles):
                if filename in f:
                    i += 1
                    if not os.path.exists(newDir + "/" + f):
                        if i % 100 == 0 or i == len(wantedRows): 
                            print("Copying file\t", i, "/", len(wantedRows))
                        shutil.copy2(photosPath + "/" + photodir + "/" + f, newDir)
                    else:
                        print("The file", f, "already exists in the destiny directory", "\t",i, "/", len(wantedRows))
    return newDir
    
def main():
    if len(sys.argv) < 2:
        print("Please provide a CSV file to filter\n\n  python csvImageExtractor.py [.csv file]")
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
    
    newParameters = input("Provide the pitch (7.2), roll (7.2) and altitude (3.0) values in this order separated by a space.\nIf not provided this values will take their default value:\n")
    if newParameters and len(newParameters.split()) == 3:
        parameters = newParameters.split()
        desiredPitch = float(parameters[0])
        desiredRoll = float(parameters[1])
        upperLimAltitude = float(parameters[2])
    
    wantedRows = getWantedRowsFromCSVFile(rows, desiredPitch, desiredRoll, bottomLimAltitude, upperLimAltitude)
    
    newDir = copyWantedRowFilesToMRADir(wantedRows, filepath)
    print("File filtering resulted in " + str(len(wantedRows)) + " rows and " + str(round(len(wantedRows) / len(rows) * 100,2)) + " % of data from the original dataset and were saved in the", newDir, "directory.")    
    print("exiting...")
    sys.exit(0)
        
if __name__ == "__main__":
    main()
