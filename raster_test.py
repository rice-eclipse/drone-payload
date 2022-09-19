import cv2 as cv
import numpy as np

im = cv.imread("distortion_test_soccer_field_image.png")
(height, width) = im.shape[:2]
assert (width, height) == (1280, 720), "or whatever else"

K = np.eye(3)
K[0,0] = K[1,1] = 1000 # 500-5000 is common
K[0:2, 2] = (width-1)/2, (height-1)/2
# array([[1000. ,    0. ,  639.5],
#        [   0. , 1000. ,  359.5],
#        [   0. ,    0. ,    1. ]])

print(K)

dc = np.float32([-0.54,  0.28,  0.  ,  0.  ,  0.  ]) # k1, k2, p1, p2, k3

modelpts = np.float32([
    [45.,  0.],
    [90.,  0.],
    [90., 60.],
    [45., 60.]]) * 15 # 15 pixels per foot

impts = [
 [511.54881, 184.64497],
 [758.16124, 141.19525],
 [1159.37185, 191.21864],
 [1153.4168, 276.2696]
]

impts_undist = np.float32([
    [ 508.38733,  180.3246 ],
    [ 762.08234,  133.98148],
    [1271.5339 ,  154.91203],
    [1250.6611 ,  260.52057]]).reshape((-1, 1, 2))

print(cv.undistortImagePoints(impts, K, dc))

H = cv.getPerspectiveTransform(impts_undist, modelpts)

# add some in the X and Y dimension
Tscale = np.array([
    [  1.,   0.,  75.], # arbitrary values
    [  0.,   1.,  25.],
    [  0.,   0.,   1.]])

topdown = cv.warpPerspective(impts_undist, H, dsize=(90*15, 60*15))

