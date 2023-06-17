import os
import subprocess
import cv2
import numpy as np

import config_vars


def chessboard_images(n_samples: int):
    points, objpoints, imgs = [], [], []
    for img_idx in range(n_samples):
        input(f"({img_idx + 1}) Press enter to capture calibration image")
        filename = (os.getcwd() / f"calibration_img_{img_idx + 1}.jpg")
        camera_process = subprocess.Popen(["libcamera-still", "-o", filename])
        camera_process.wait()
        img = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(
            img, config_vars.CHESSBOARD_DIMS, None)
        if not found:
            img_idx -= 1
            continue
        else:
            points.append(corners)
            imgs.append(img)

            # Setting up chessboard cm coordinates relative to camera (board at z=0)
            objp = np.zeros(
                (config_vars.CHESSBOARD_DIMS[0] *
                 config_vars.CHESSBOARD_DIMS[1], 3), np.float32
            )
            objp[:, :2] = np.mgrid[
                :config_vars.CHESSBOARD_DIMS[0],
                :config_vars.CHESSBOARD_DIMS[1]
            ].transpose().reshape(-1, 2)
            objp *= config_vars.CHESSBOARD_SQUARE_LENGTH_CM
            objp[:, 0] -= max(objp[:, 0])/2
            objp[:, 1] -= max(objp[:, 1])/2
            objpoints.append(objp)

            print(
                f"Img Dims:\n{img.shape}\nPoints:\n{points}\nObjPoints (cm):\n{objpoints}")
    return points, objpoints, imgs
