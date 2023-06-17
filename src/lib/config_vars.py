import math
import numpy as np


# Vehicle's address
ADDRESS = '/dev/ttyAMA0'

# On and off signal frequencies
SIGNAL_ON = 1200
SIGNAL_OFF = 1600

# Pins connected to switches
INPUT_PIN1 = 25
INPUT_PIN2 = 21

CHANNEL_NUM = 8

CAPTURE_TIMEOUT_MS = 5000
CAMERA_NS_OFFSET = -2.16 * 1e13 # -6 hours

PHOTO_CMD = ["/usr/bin/libcamera-still", "--nopreview", f"--timeout={CAPTURE_TIMEOUT_MS}", "--autofocus-on-capture", "--flush", "-o"]
# Logging field names
LOGGING_FIELD_NAMES = ['Time', 'Global Location', 'Local Location',
                       'Attitude', 'Velocity', 'GPS', 'Heading']

# 0 is very relaxed, retaining black pixels from distortion. 
# 1 will occlude all unwanted pixels, auto-cropping ROI
ROI_SCALING = 1

CHESSBOARD_DIMS = (7, 7) # Internal corners
CALIB_CAMERA_DISTANCE_CM = 59 # Distance from the camera to the chessboard (cm)
CHESSBOARD_SQUARE_LENGTH_CM = 2.5875 # Length of each chessboard square

PX_DISTANCE_EST_SEED = 42
PX_DISTANCE_EST_TRIALS = 50

ANGLE_WARP_PHI_CUTOFF = math.pi / 4 # The max angle of elevation view before image is cut off

UNITLESS_CHESSBOARD_COORDS = np.zeros((CHESSBOARD_DIMS[0] * CHESSBOARD_DIMS[1], 3), np.float32)
UNITLESS_CHESSBOARD_COORDS[:, :2] = np.mgrid[
        :CHESSBOARD_DIMS[0],
        :CHESSBOARD_DIMS[1]
    ].transpose().reshape(-1, 2)