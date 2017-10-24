import math
import os
import shutil
import subprocess
import commands

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
                            print "Copying file\t", i, "/", len(wantedRows)
                        shutil.copy2(photosPath + "/" + photodir + "/" + f, newDir)
                    else:
                        print "The file", f, "already exists in the destiny directory", "\t",i, "/", len(wantedRows)
    return newDir

def extractAndCompileCLAHEFiles(newDir):
    status = subprocess.call(["tar", "-xf", "filter1.tar.gz", "-C", newDir])
    os.chdir(newDir)
    subprocess.call(["make"], shell=True)
    if not status:
        print "Extracted filter1.tar.gz in", newDir, "successfully"
    else:
        print "Oops! Something went wrong while extracting"
        exit(1)
    
def executeCLAHEAlgorithm(newDir, wantedRows):
    normalizedDir = "/".join(newDir.split("/")[:-1]) + "/Normalized"
    if not os.path.exists(normalizedDir):
        os.makedirs(normalizedDir)
    os.chdir(newDir)
    print "Applying CLAHE algorithm..."
    for img in wantedRows:
        if os.path.exists(img + ".jpg"):
            if "retifi_"+img+".jpg" not in os.listdir(normalizedDir):
                if wantedRows.index(img) % 100 == 0 or wantedRows.index(img) == len(wantedRows):
                    print "Processed", img + ".jpg\t", wantedRows.index(img) + 1,"/", len(wantedRows)
                subprocess.call(["./filter1", img+".jpg"])
    print "Images successfully retified"
    return normalizedDir

def organizeDirectory(newDir, normalizedDir):
    listDir = os.listdir(newDir)
    movingList = [ a for a in listDir if "retifi" in a]
    for filename in movingList:
        if not os.path.exists(normalizedDir + "/" + filename):
            shutil.move(filename, normalizedDir)
    for filename in [a for a in os.listdir(newDir) if not a.split(".")[0].isdigit()]:
        os.remove(filename)
