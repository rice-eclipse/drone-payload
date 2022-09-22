import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

img = cv.imread("distortion_test_soccer_field_image.png")
print(img.shape)

# Field Size 60' x 90'
h = 900
w = 1200


# 4 Points on Original Image
pt1 = np.float32([[511.54881, 184.64497],
 [758.16124, 141.19525],
 [1159.37185, 191.21864],
 [1153.4168, 276.2696]])

# 4 Corresponding Points of Desired Bird Eye View Image
pt2 = np.float32([
    [ 508.38733,  180.3246 ],
    [ 762.08234,  133.98148],
    [1271.5339 ,  154.91203],
    [1250.6611 ,  260.52057]])


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