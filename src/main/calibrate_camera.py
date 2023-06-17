'''
Camera calibration script: modified for PIGEON purposes.
References:
https://docs.opencv.org/3.3.0/dc/dbb/tutorial_py_calibration.html

Authors: Ian Rundle, Yumn Teshome
'''

import sys
import os
from typing import List
import argparse
import cv2
import config_vars
import numpy as np

sys.path.append("../lib")

import capturing

__description__ = "Calibrates the camera, saves camera mx and distortions to npz."

def _parse_args(args: List[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--samples", "-s", type=int, required=True)
    return parser.parse_args(args)

def main(cmd_args: List[str]) -> None:
    args = _parse_args(cmd_args)

    # Taking the specified number of photos
    imgs, points = capturing.chessboard_images(args.samples)

    # Generate calibration matrices
    input("Press enter to begin calibration with data :)")
    _, mtx, dist, _, _ = cv2.calibrateCamera(points, imgs, imgs[0].shape[::-1], None, None)
    h, w = imgs[0].shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), config_vars.ROI_SCALING, (w,h))
    print(f"Camera matrix:\n{mtx}\nNew Camera Matrix:\n{newcameramtx}")

    # Undistorts the first image (imgs[0]), saves the result
    result_path = os.getcwd() / 'calibresult.png'
    undistort_img(mtx, dist, newcameramtx, imgs[0], roi)
    print(f"Undistorted Image saved as {result_path}")

    # Saves the calibration result for future 3D referencing
    save_path = os.getcwd() / "camera_matrices.npz"
    np.savez(save_path, camera_matrix=mtx, new_camera_matrix=newcameramtx, distortion=dist, roi=roi)
    print(f"Camera calibrated specs: camera_matrix, new_camera_matrix, distortion, roi at {save_path}")

    
def undistort_img(mtx, dist, newcameramtx, img, roi, result_path):
    # undistort (the 5 at the end is for good vibes)
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite(result_path, dst)
    return dst
        


if __name__ == "__main__":
    main(sys.argv[1:])