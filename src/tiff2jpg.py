import os
from PIL import Image
from skimage.measure import shannon_entropy
import gdal
from skimage.io import imread

out = open("info.csv", "w")
out.write("filename, longitude, latitude, entropy\n")
current_path = os.getcwd()
for root, dirs, files in os.walk(current_path, topdown=False):
    for name in files:
        print( os.path.join(root, name))
        #if os.path.splitext(os.path.join(root, name))[1].lower() == ".tiff":
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
            if os.path.isfile(os.path.splitext(os.path.join(root, name))[0] + ".jpg"):
                print( "A jpeg file already exists for %s" % name)
            # If a jpeg with the name does *NOT* exist, covert one from the tif.
            else:
                outputfile = os.path.splitext(os.path.join(root, name))[0] + ".jpg"
                im = Image.open(os.path.join(root, name))
                print( "Converting jpeg for %s" % name)
                im.thumbnail(im.size)
                im.save(outputfile, "JPEG", quality=100)
                geo = gdal.Open(os.path.join(root, name))
                pos = geo.GetGeoTransform()
                lon = pos[0]
                lat = pos[3]
                entropy = shannon_entropy(imread(outputfile, True))
                out.write(outputfile.split('/')[-1] + ", " + str(lon) + ", " + str(lat) + ", " + str(entropy) + "\n")
out.close()