import numpy as np
import cv2
def myZeroPadding(myImage, padSize=1):#__author__ = 'Dmitry Patashov'

    if myImage.__class__ == np.ndarray:

        Dim = myImage.shape
        if len(Dim) == 2:

            m, n = Dim[0], Dim[1]
            NewImg = np.zeros([m + 2 * padSize, n + 2 * padSize])
            NewImg[padSize:m + padSize, padSize:n + padSize] = myImage

            return np.uint8(NewImg)

        elif len(Dim) == 3:

            b, g, r = cv2.split(myImage)
            Pb = myZeroPadding(b, padSize)
            Pg = myZeroPadding(g, padSize)
            Pr = myZeroPadding(r, padSize)

            return cv2.merge((Pb, Pg, Pr))
        else:
            return None
    else:
        return None

def myExtendedPadding(myImage, padSize=1): #__author__ = 'Dmitry Patashov'
    if myImage.__class__ == np.ndarray:

        Dim = myImage.shape
        if len(Dim) == 2:

            newImg = myZeroPadding(myImage, padSize)
            def extendTopDown(newImg, padSize, dim):

                newImg[:padSize, :] = newImg[padSize, :]
                newImg[dim + padSize:, :] = newImg[dim + padSize - 1, :]

                return newImg

            newImg = extendTopDown(newImg, padSize, Dim[0])
            newImg = extendTopDown(newImg.transpose(), padSize, Dim[1]).transpose()

            return np.uint8(newImg)

        elif len(Dim) == 3:

            b, g, r = cv2.split(myImage)
            Pb = myExtendedPadding(b, padSize)
            Pg = myExtendedPadding(g, padSize)
            Pr = myExtendedPadding(r, padSize)

            return cv2.merge((Pb, Pg, Pr))
        else:
            return None
    else:
        return None