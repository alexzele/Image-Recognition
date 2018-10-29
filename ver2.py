import cv2
import numpy as np
from PIL import Image
import unicodedata
import pandas as pd

# Choose "Additional Data" in Tesseract installation for better OCR recognition
import pytesseract

# Improve recognition chances for marginal patterns
import func as f

# Activation of Tesseract OCR Library
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"

#---------------------------------------------------------------------------------------------------#

img_rgb = cv2.imread('OriginalFiles/Origin.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

# Manually cropped circle for matchTemplate
template = cv2.imread('OriginalFiles/single_circle.PNG', 0)

# Extract Height and Width of template
w, h = template.shape[::-1]

# Add padding to insure  identification of margin objects
img_gray = f.myExtendedPadding(img_gray, 10)
img_rgb = f.myExtendedPadding(img_rgb, 10)

# Calculate all matches of template in image
res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)

# Variables
threshold = 0.4
i = 0
OCR_FailureFlag = 1
exel_file_path = 'OriginalFiles/test.xlsx'

# list of strings, each represents a match
ocr_Results = []

# X,Y values of matches
# For future development, Sync press on screen with click on app
coordinates_template = []

# Only matches above certain value
loc = np.where(res >= threshold)

for pt in zip(*loc[::-1]):
    #cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    pt_cord = pt, (pt[0] + w, pt[1] + h)
    coordinates_template.append(pt_cord)
    box_Grey = img_gray[pt[1]:pt[1] + h, pt[0]:pt[0] + w]
    cv2.imwrite('WorkingDirectory/' + str(i) + '.png', box_Grey)

    # ------ Image optimization for OCR ------ #

    # Image optimization for OCR - B&W (Best threshold = 215)
    box_BW= cv2.threshold(box_Grey, 215, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite('WorkingDirectory/' + str(i) + '_BW.png', box_BW)

    # Image optimization for OCR - Resize
    size_enhancment = 540, 530
    box_BW_improv = Image.open('WorkingDirectory/' + str(i) + '_BW.png')
    box_BW_improv = box_BW_improv.resize(size_enhancment, Image.ANTIALIAS)
    box_BW_improv.save('WorkingDirectory/' + str(i) + '_BW_resized.png', "PNG")

    # Image optimization for OCR - Crop
    # Crop will leave only numbers

    box_BW_improv = cv2.imread('WorkingDirectory/' + str(i) + '_BW_resized.png')

    # From Center [Top:Bottom, Left:Right]
    BW_crop_img = box_BW_improv[170:340, 50:490]
    cv2.imwrite('WorkingDirectory/' + str(i) + '_BW_cropped.png', BW_crop_img)

    # Actual OCR attempt (casting to make result a string)
    result_String = pytesseract.image_to_string(Image.open('WorkingDirectory/' + str(i) + '_BW_cropped.png'))
    unicodedata.normalize('NFKD', result_String).encode('ascii', 'ignore')

    # Validate All digits identified
    for char in result_String:
        if(not char.isdigit()) :
             print("in file " + str(i))
             OCR_FailureFlag = 1

    # Un/Successful identification to results array + saves successes with file name
    if (not OCR_FailureFlag):
        ocr_Results.append(result_String)
        cv2.imwrite('WorkingDirectory/' + str(i) + "_" + str(result_String) + '.png', box_Grey)
    else:
        ocr_Results.append('fail')

    OCR_FailureFlag = 0

    i=i+1


number_found = 1
data = input("enter a number of leak equipment: ")
data4Exel = data
data = str(data).decode("utf-8")

if data in ocr_Results:
    print("Yes, " + data + " found in the leak equipment List")
else:
    print("Sorry, We didnt find the number")
    number_found = 0

df = pd.read_excel(exel_file_path, sheet_name='Blad2')
leakEquipmentFromExel = df['leak_equipment']

# For demonstration use 101987
for x in leakEquipmentFromExel:
    if x == data4Exel:
        print("The leak_equipment was found, Next version will print your data here")
        if (number_found):
            IDindex = ocr_Results.index(data)
            cv2.rectangle(img_rgb, coordinates_template[IDindex][0], (coordinates_template[IDindex][0][0] + w, coordinates_template[IDindex][0][1] + h), (255,0,0), 2)
            cv2.imshow('Your leak equipment', img_rgb)
            cv2.waitKey()
        break