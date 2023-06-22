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
import numpy as np
from pathlib import Path

REPO_TOP = Path(__file__).resolve().parent.parent.parent
DATA_DIR = REPO_TOP / "src/data"
sys.path.append("../lib")

import capturing
import config_vars


__description__ = "Calibrates the camera, saves camera mx and distortions to npz."


def _parse_args(args: List[str]) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--samples", "-s", type=int, required=True)
    return parser.parse_args(args)


def main(cmd_args: List[str]) -> None:
    args = _parse_args(cmd_args)

    # Taking the specified number of photos
    cbimg = capturing.ChessboardImage(str(DATA_DIR / "chessboard.png"))
    objpoints = cbimg.objp
    points = cbimg.corners
    img = cbimg.image
    print(objpoints, points, img)

    # Generate calibration matrices
    input("Press enter to begin calibration with data :)")
    # Returns camera matrix, distortion coeffs, rotation and translation vectors to 3D space
    _, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        [objpoints], [points], img.shape[::-1], None, None)
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
        mtx, dist, (w, h), config_vars.ROI_SCALING, (w, h))
    print(f"Camera matrix:\n{mtx}\nNew Camera Matrix:\n{newcameramtx}")

    # Undistorts the images, saves results
    result_path = DATA_DIR / 'calib_result.png'
    undistort_img(mtx, dist, newcameramtx, img, roi, str(result_path))
    print(f"Undistorted Image saved as {result_path}")

    # Finds the corners of the chessboard in each undistorted image
    found, corners = cv2.findChessboardCorners(img, config_vars.CHESSBOARD_DIMS, None)
    if not found:
        raise Exception(f"Not found:\n{corners}")
    print(f"Undistorted corners:\n{corners}")

    # Saves the calibration result for future 3D referencing
    save_path = Path(os.getcwd()) / "camera_matrices.npz"
    np.savez(save_path, camera_matrix=mtx,
             new_camera_matrix=newcameramtx, distortion=dist, roi=roi)
    print(
        f"Camera calibrated specs: camera_matrix, new_camera_matrix, distortion, roi at {save_path}")
    
    # Displaying Accuracy
    print(rvecs)
    imgpoints2, _ = cv2.projectPoints(objpoints, rvecs[0], tvecs[0], mtx, dist)
    error = cv2.norm(points, imgpoints2, cv2.NORM_L2)
    print(f"Mean projection estimate error (cm): {error}")
    
    _confirm_perspective()
    # Perspective Calibration
    thetas, phis = capturing.calibrate_perspective(capturing.ChessboardImage(result_path))
    print(thetas)
    save_path = Path(os.getcwd()) / "perspective_matrices.npz"
    np.savez(save_path, thetas=thetas, phis=phis)


def undistort_img(mtx, dist, newcameramtx, img, roi, result_path):
    # undistort (the 5 at the end is for good vibes)
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite(result_path, dst)
    return dst

def _confirm_perspective():
    confirm = ""
    while confirm not in ("yes", "y", "no", "n"):
        confirm = input("Calbirate perspective now? (y/n)")
    if confirm in ("no", "n"):
        exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
