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

ROI_SCALING = 0.5 # 0 is very relaxed, retaining all pixels. 1 will occlude all unwanted pixels
CHESSBOARD_DIMS = (7, 7)