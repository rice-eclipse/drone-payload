import os
import cv2
import numpy as np
import random
import math
from typing import List
from pathlib import Path

REPO_TOP = Path(__file__).resolve().parent.parent.parent

import config_vars

class ChessboardImage:
    def __init__(self, filename: os.PathLike):
        filename = str(filename)
        self.image = cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2GRAY)
        found, self.corners = cv2.findChessboardCorners(
            self.image, config_vars.CHESSBOARD_DIMS, None
        )
        self.objp = config_vars.UNITLESS_CHESSBOARD_COORDS
        if not found:
            print("Failed to find points")

class Camera:
    def __init__(self):
        self.camera = picamera2.Picamera2()
        self.camera.set_controls({"AfMode": libcamera.controls.AfModeEnum.Continuous})
        self.camera.start()
        self.proc_running = False

    def take_photo(self, path: os.PathLike):
        '''
        Retrieves a metadata dictionary from photo taking
        '''
        self.proc_running = True
        self._job = self.camera.capture_file(path, wait=False, signal_function=lambda job: self._photo_complete(job))
    
    def get_job_results(self):
        if not self.proc_running:
            print("Getting result")
            metadata = self._job.get_result()
            if "SensorTimestamp" in metadata.keys():
                capture_ns = metadata["SensorTimestamp"]
            else:
                print("Could not find SensorTimestamp in metadata keys")
                capture_ns = -1
            return metadata, capture_ns
        else:
            raise Exception("Job still running")
    
    def close(self):
        self.camera.close()
    
    def _photo_complete(self, job):
        self.proc_running = False

# def chessboard_images(n_samples: int) -> List[ChessboardImage]:
#     result = []
#     picam2 = Picamera2()
#     picam2.start()
#     picam2.set_controls({'AfMode': libcamera.controls.AfModeEnum.Manual, 'LensPosition': 1.5})
#     for img_idx in range(n_samples):
#         input(f"({img_idx + 1}) Press enter to capture calibration image")
#         filename = str(Path(os.getcwd()) / f"calibration_img_{img_idx + 1}.png")
#         cycle_result = picam2.autofocus_cycle()
#         if cycle_result: print("Error: autofocus failure")
#         metadata = picam2.capture_file(filename, format="png")
#         result.append(ChessboardImage(filename))
#         print(
#             f"Img Dims:\n{result[-1].image.shape}\nPoints:\n{result[-1].corners}\nObjPoints (cm):\n{result[-1].objp}"
#         )
#     return result

def calibrate_perspective(chess_image: ChessboardImage) -> List[np.ndarray]:
    print("Calibrating perspective...")
    print(f"Corners (x{len(chess_image.corners)}):\n {chess_image.corners}")

    print(chess_image.objp)
    chess_image.objp[:, 0] -= max(chess_image.objp[:, 0])/2
    chess_image.objp[:, 1] -= max(chess_image.objp[:, 1])/2
    chess_image.objp[:, :2] *= config_vars.CHESSBOARD_SQUARE_LENGTH_CM
    chess_image.objp[:, 2] = config_vars.CALIB_CAMERA_DISTANCE_CM
    print(f"Relative corner coordinates:\n{chess_image.objp}")
    assert len(chess_image.corners) == len(chess_image.objp)

    # We are assuming that each corner index corresponds in objp and corners
    cm_per_px_ests = []
    random.seed = config_vars.PX_DISTANCE_EST_SEED
    for _ in range(config_vars.PX_DISTANCE_EST_TRIALS):
        from_idx = random.randint(0, len(chess_image.corners) - 1)
        from_obj, from_px = chess_image.objp[from_idx], chess_image.corners[from_idx]
        to_idx = random.randint(0, len(chess_image.corners) - 1)
        if to_idx == from_idx:
            to_idx = (to_idx + 1) % len(chess_image.corners)
        to_obj, to_px = chess_image.objp[to_idx], chess_image.corners[to_idx]
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

    x_vals = np.linspace(-1 * chess_image.image.size[0] / 2 * cm_per_px, chess_image.image.size[0] / 2 * cm_per_px, chess_image.image.size[0])
    x_vals = np.repeat(x_vals, chess_image.image.size[1], axis=1)
    y_vals = np.linspace(-1 * chess_image.image.size[1] / 2 * cm_per_px, chess_image.image.size[1] / 2 * cm_per_px, chess_image.image.size[1])
    y_vals = np.repeat(y_vals, chess_image.image.size[0], axis=1)
    y_vals = y_vals.transpose()
    z_vals = np.ones(chess_image.image.size) * config_vars.CALIB_CAMERA_DISTANCE_CM
    print(f"x-vals: {x_vals}")
    print(f"y-vals: {y_vals}")
    print(f"z-vals: {z_vals}")

    # Lol I think this trig is right
    thetas = np.arctan2(y_vals, x_vals)
    phis = np.arctan2(np.sqrt(x_vals ** 2 + y_vals ** 2), z_vals)
    print(f"Thetas:\n{thetas}")
    print(f"Phis:\n{phis}")
    return thetas, phis

