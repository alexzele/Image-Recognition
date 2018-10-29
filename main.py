import cv2
import numpy as np
import func
from matplotlib import pyplot as plt
from PIL import Image
import pandas as pd


img_rgb = cv2.imread('circle.png')
#cv2.imshow('color',img_rgb)
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)#convert original pic to gary scale
#cv2.imshow('gray',img_gray)
templatec = cv2.imread('single_circle.PNG')
#cv2.imshow('color_single',templatec)
template = cv2.cvtColor(templatec, cv2.COLOR_BGR2GRAY)#convert original pic to gary scale
#cv2.imshow('gray_single',template)

w, h = template.shape[::-1]#get size of template

img_gray=func.myExtendedPadding(img_gray,10)
cv2.imshow('padding',img_gray)


res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)#return the midlle point of circle found
cv2.imshow('what it is',res)
im=cv2.imread('circle.png')
width, height,col = im.shape

width+=10
height+=10
binaryM= np.zeros([width,height])#create binary matrix
threshold = 0.42
i = 0
loc = np.where( res >= threshold)#
cv2.imshow('what it is1',res)
list_xy = []
for pt in zip(*loc[::-1]):#
    cv2.rectangle(img_rgb, pt, (pt[0]+w , pt[1]+h ), (0,0,255),1 )
    list_xy.append(((pt[0] + w)-10,(pt[1] + h)-10))#create list of all images for syc with vector (loading func)
    binaryM[pt[1]:pt[1] + h,pt[0]:pt[0] + w] = 1
   # box = img_rgb[pt[1]:pt[1] + h, pt[0]:pt[0] + w]#save the cordination
    #cv2.imwrite(str(i) + '.png', box)#save lot of cut pic
    i=i+1
#cv2.imshow('ans5',np.uint8(binaryM*255))#cheack if the matrix have 1

cv2.imwrite('orig.png',img_gray)#convet to original size
img = Image.open('orig.png')
new_width  = 1124
new_height = 918
img = img.resize((new_width, new_height), Image.ANTIALIAS)
ans=binaryM * img# save in ans just the circle

cv2.imshow('ans',np.uint8(ans))#the mtrix with numbers
cv2.imwrite('res.png',img_rgb)


df = pd.read_excel('test.xlsx', shee_tname='Blad2')
pd.options.display.max_rows = 999
listSepalWidth = df['leak_equipment']
print(listSepalWidth[512])
print (df['leak_equipment'])





