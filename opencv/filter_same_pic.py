# pip install opencv-python
# pip install opencv-contrib-python

import os
import cv2
import numpy

def CheckIdenticalImages(img1, img2):
    image1=cv2.imread(img1)
    image2=cv2.imread(img2)
    if  image1.shape!=image2.shape:
        return 0
    else:
        check=cv2.subtract(image1, image2)
        out=numpy.any(check)
        if out==False:
            return 1
        else:
            return 0

if __name__ == '__main__':

    main()
    print('Complete!!!!!!!!!!')
