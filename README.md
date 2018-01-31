# README


## About

This is the repository of the development of the **MsC thesis: Automatic Habitat Mapping using Machine Learning**. This repository contains programs that use Computer Vision techniques to deal with image enhancement and image noise in photos and sidescan sonar images. It may also contain some programs that handle the images in a file system. In the future will have the implementation of the ML predictive model (first approach will be CNNs).   


## Requirements

To use this program you need to have installed the libopencv2.4-jni and their dev libraries:

    sudo apt-get install libopencv2.4-jni libopencv*-dev

Then use pip3 (or conda if you use anaconda) to install the modules numpy and opencv:

    sudo pip3 install --upgrade pip
    sudo pip3 install opencv-python numpy


## Running

Just run the program using python3 (as you would normally do) in the terminal:

	python3 csvImageExtractor.py [path to your CSV file]

This program will create a directory called FilteredPhotos in your mra folder with the Original photos. Also, this program retrieves the photos from a CSV file in which roll and pitch have values bellow 7.2º and the altitude limits are between 1.5 and 3 meters. These values can be changed within program's execution.


To apply the filters available use:
    
    python3 imageProcessing.py [path to the photos directory]


**WARNING:** Depending on the amount of photos on the directory, this process may take a while and it'll be using all the threads available on your CPU. If you do not want to use all your threads please edit all occurrences of this line in the **imageProcessing.py** file:

    processes = mp.cpu_count() 

and change the value __mp.cpu_count()__ for the number of your choice.

### Have fun!  
