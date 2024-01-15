import cv2
import pytesseract
import imutils
pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR/tesseract.exe"
image = cv2.imread("img/c3.jpeg")
image = imutils.resize(image, width=500)
gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
gray = cv2.bilateralFilter(gray,11,17,17)
edge = cv2.Canny(gray, 170,200)
cnts, new = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
image1 = image.copy()
cv2.drawContours(image1, cnts, -1,(0,255,0),3)
cnts = sorted(cnts, key= cv2.contourArea, reverse= True) [: 30]
NumberPlateCount = None
image2 = image1.copy()
cv2.drawContours(image2,cnts,-1,(0,255,0),3)
count = 0
name = 1
for i in cnts:
    perimeter = cv2.arcLength(i, True)
    approx = cv2.approxPolyDP(i, 0.02* perimeter, True)
    if(len(approx) == 4):
        NumberPlateCount = approx
        x,y,w,h = cv2.boundingRect(i)
        crp_img = image[y:y+h, x:x+w]
        cv2.imwrite(str(name) + '.png', crp_img)
        name +=1
        break
cv2.drawContours(image,[NumberPlateCount], -1,(0,255,0),3)
crpImg = '1.png'
cv2.imshow("Cropped image", cv2.imread(crpImg))
text = pytesseract.image_to_string(crpImg, lang= 'eng')
print("Car number is : ", text)

cv2.imshow("Original image", image)
# cv2.imshow("Gray image", gray)
# cv2.imshow("Smooth image", gray)
# cv2.imshow("Canny image", edge)
# cv2.imshow("Canny after contours", image1)
# cv2.imshow("Cropped image", image2)
cv2.imshow("Final image", image)
cv2.waitKey(0)