import os
import shutil
import subprocess



def extractAndCompileCLAHEFiles(newDir):
    status = subprocess.call(["tar", "-xf", "filter1.tar.gz", "-C", newDir])
    os.chdir(newDir)
    subprocess.call(["make"], shell=True)
    if not status:
        print("Extracted filter1.tar.gz in", newDir, "successfully")
    else:
        print("Oops! Something went wrong while extracting")
        exit(1)
    
def executeCLAHEAlgorithm(newDir, wantedRows):
    normalizedDir = "/".join(newDir.split("/")[:-1]) + "/Normalized"
    if not os.path.exists(normalizedDir):
        os.makedirs(normalizedDir)
    os.chdir(newDir)
    print("Applying CLAHE algorithm...")
    for img in wantedRows:
        if os.path.exists(img + ".jpg"):
            if "retifi_"+img+".jpg" not in os.listdir(normalizedDir):
                if wantedRows.index(img) % 100 == 0 or wantedRows.index(img) == len(wantedRows):
                    print("Processed", img + ".jpg\t", wantedRows.index(img) + 1,"/", len(wantedRows))
                subprocess.call(["./filter1", img+".jpg"])
    print("Images successfully retified")
    return normalizedDir

def organizeDirectory(newDir, normalizedDir):
    listDir = os.listdir(newDir)
    movingList = [ a for a in listDir if "retifi" in a]
    for filename in movingList:
        if not os.path.exists(normalizedDir + "/" + filename):
            shutil.move(filename, normalizedDir)
    for filename in [a for a in os.listdir(newDir) if not a.split(".")[0].isdigit()]:
        os.remove(filename)
