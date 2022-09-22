import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread("distortion_test_soccer_field_image.png")
print(img.shape)

# Field Size 60' x 90'
h = 900
w = 1200


# 4 Points on Original Image
pt1 = np.float32([[1,356],[1273,235],[769,212], [81,799]])

# 4 Corresponding Points of Desired Bird Eye View Image
pt2 = np.float32([[0,0],[0,h],[w,h],[w,0]])


matrix = cv.getPerspectiveTransform(pt1, pt2)
print(matrix)
output = cv.warpPerspective(img,matrix,(w,h))

for i in range(0,4):
    cv.circle(img,(int(pt1[i][0]),int(pt1[i][1])),5,(0,0,255),cv.FILLED)

# window1 = cv.namedWindow("w1")
# cv.imshow(window1,img)
# cv.waitKey(0)
# cv.destroyWindow(window1)


# window2 = cv.namedWindow("w2")
# cv.imshow(window2,output)
# cv.waitKey(0)
# cv.destroyWindow(window2)

plt.subplot(121),plt.imshow(img),plt.title('Input')
plt.subplot(122),plt.imshow(output),plt.title('Output')
plt.show()