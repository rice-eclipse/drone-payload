# Vehicle's address
ADDRESS = '/dev/ttyS0'

# On and off signal frequencies
SIGNAL_ON = 1200
SIGNAL_OFF = 1700

# Pins connected to switches
INPUT_PIN1 = 26
INPUT_PIN2 = 21

# Logging field names
LOGGING_FIELD_NAMES = ['Global Location', 'Local Location',
                       'Attitude', 'Velocity', 'GPS', 'Heading']

# 0 is very relaxed, retaining black pixels from distortion. 
# 1 will occlude all unwanted pixels, auto-cropping ROI
ROI_SCALING = 1

CHESSBOARD_DIMS = (7, 7) # Internal corners
CALIB_CAMERA_DISTANCE_CM = 20 # Distance from the camera to the chessboard (cm)
CHESSBOARD_SQUARE_LENGTH_CM = 2 # Length of each chessboard square

PX_DISTANCE_EST_SEED = 42
PX_DISTANCE_EST_TRIALS = 50