import numpy as np
import cv2 

# read the image file 
img = cv2.imread("./green_lande.jpg")

# print the shape of the image
# print(img.shape)

# show the image
cv2.imshow("Green Land", img)
cv2.waitKey()
cv2.destroyAllWindows()