import os
import subprocess
import cv2

import config_vars

def chessboard_images(n_samples: int):
    points, imgs = [], []
    for img_idx in range(n_samples):
        input(f"({img_idx + 1}) Press enter to capture calibration image")
        filename = (os.getcwd() / f"calibration_img_{img_idx + 1}.jpg")
        camera_process = subprocess.Popen(["libcamera-still", "-o", filename])
        camera_process.wait()
        img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(img, config_vars.CHESSBOARD_DIMS, None)
        if not found:
            img_idx -= 1
            continue
        else:
            points.append(corners)
            imgs.append(img)
            print(f"Img Dims:\n{img.shape}\nPoints:\n{points}")