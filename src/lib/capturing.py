import os
import subprocess
import cv2
import numpy as np
import random
import math
from typing import List, Tuple

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

            # Setting up chessboard evenly spaced coords (no units)
            objp = np.zeros(
                (config_vars.CHESSBOARD_DIMS[0] *
                 config_vars.CHESSBOARD_DIMS[1], 3), np.float32
            )
            objp[:, :2] = np.mgrid[
                :config_vars.CHESSBOARD_DIMS[0],
                :config_vars.CHESSBOARD_DIMS[1]
            ].transpose().reshape(-1, 2)
            objpoints.append(objp)

            print(
                f"Img Dims:\n{img.shape}\nPoints:\n{points}\nObjPoints (cm):\n{objpoints}"
                )
    return points, objpoints, imgs

def calibrate_perspective(corners: List[Tuple[float, float]], img_size: Tuple[int, int]) -> List[np.ndarray]:
    print("Calibrating perspective...")
    print(f"Corners (x{len(corners)}):\n {corners}")
    objp = np.zeros(
        (config_vars.CHESSBOARD_DIMS[0] *
            config_vars.CHESSBOARD_DIMS[1], 3), np.float32
    )
    objp[:, :2] = np.mgrid[
        :config_vars.CHESSBOARD_DIMS[0],
        :config_vars.CHESSBOARD_DIMS[1]
    ].transpose().reshape(-1, 2)
    objp[:, 0] -= max(objp[:, 1])/2
    objp[:, 1] -= max(objp[:, 2])/2
    objp[:, :2] *= config_vars.CHESSBOARD_SQUARE_LENGTH_CM
    objp[:, 2] = config_vars.CALIB_CAMERA_DISTANCE_CM
    print(f"Relative corner coordinates:\n{objp}")
    assert len(corners) == len(objp)

    # We are assuming that each corner index corresponds in objp and corners
    cm_per_px_ests = []
    random.seed = config_vars.PX_DISTANCE_EST_SEED
    for _ in range(config_vars.PX_DISTANCE_EST_TRIALS):
        from_idx = random.randint(0, len(corners) - 1)
        from_obj, from_px = objp[from_idx], corners[from_idx]
        to_idx = random.randint(0, len(corners) - 1)
        if to_idx == from_idx:
            to_idx = (to_idx + 1) % len(corners)
        to_obj, to_px = objp[to_idx], corners[to_idx]
        obj_dist = math.sqrt((to_obj[0] - from_obj[0])**2 + (to_obj[1] - from_obj[1])**2)
        px_dist = math.sqrt((to_px[0] - from_px[0])**2 + (to_px[1] - from_px[1])**2)
        estimate = obj_dist / px_dist
        print(f"Estimate: {estimate} cm/px")
        cm_per_px_ests.append(estimate)
    cm_per_px_ests = np.array(cm_per_px_ests)
    cm_per_px = np.mean(cm_per_px_ests)
    print(f"MSE of Estimates: {(cm_per_px_ests - cm_per_px)**2 / len(cm_per_px_ests)}")
    print(f"Mean of Estimates: {cm_per_px} cm/px")
    print(f"Configured orthogonal distance from camera: {config_vars.CALIB_CAMERA_DISTANCE_CM}")

    x_vals = np.linspace(-1 * img_size[0] / 2 * cm_per_px, img_size[0] / 2 * cm_per_px, img_size[0])
    x_vals = np.repeat(x_vals, img_size[1], axis=1)
    y_vals = np.linspace(-1 * img_size[1] / 2 * cm_per_px, img_size[1] / 2 * cm_per_px, img_size[1])
    y_vals = np.repeat(y_vals, img_size[0], axis=1)
    y_vals = y_vals.transpose()
    z_vals = np.ones(img_size) * config_vars.CALIB_CAMERA_DISTANCE_CM

    # Lol I think this trig is right
    thetas = np.arctan2(y_vals, x_vals)
    phis = np.arctan2(np.sqrt(x_vals ** 2 + y_vals ** 2), z_vals)
    print(f"Thetas:\n{thetas}")
    print(f"Phis:\n{phis}")
    return thetas, phis


