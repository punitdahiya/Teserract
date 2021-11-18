import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd=r'C:/Users/HP/AppData/Local/Tesseract-OCR/tesseract.exe'
from pytesseract import Output

image = cv2.imread('text.jpg', cv2.IMREAD_GRAYSCALE)
threshold_img = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY )[1]
print(threshold_img)
"""for i in range(232,232+37+1):
    for j in range(604,604+22+1):
        if threshold_img[i][j]==0:
            print(threshold_img[i][j],end=" ")
    print()
"""
custom_config = r'--oem 3 --psm 6'
details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')
print(details.keys())
bold={}
total_boxes = len(details['text'])
for sequence_number in range(total_boxes):
    if int(float(details['conf'][sequence_number])) >10:
        (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
        threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        """sum_b,sum_w=0,0
        for i in range(x,x+w):
            for j in range(y,y+h):
                #print(sum_b,sum_w)
                if threshold_img[i][j]>0:
                    sum_b+=1
                else:
                    sum_w+=1
        print(details['text'][sequence_number],sum_w,sum_b, "x",x, " w",w, " y",y," h",h)"""

cv2.imwrite("boxed.jpg",threshold_img)
print("HI",threshold_img)
