
import time
import libcamera
import sys
import os
from picamera2 import Picamera2
from pathlib import Path
import datetime
import psutil

REPO_TOP = Path(__file__).resolve().parent.parent.parent
sys.path.append(os.path.join(REPO_TOP, "src/lib"))

import config_vars

boot_utc_micros = int(datetime.datetime.utcfromtimestamp(psutil.boot_time()).timestamp() * 1e6) + config_vars.UTC_MICROS_OFFSET
for _ in range(10):
    print(f"BOOT UTC {boot_utc_micros}")

REPO_TOP = Path(__file__).resolve().parent.parent.parent
sys.path.append(os.path.join(REPO_TOP, "src/lib"))

seed = int(sys.argv[1])
print(f"seed = {seed}")
picam2 = Picamera2()
picam2.set_controls({"AfMode": libcamera.controls.AfModeEnum.Continuous})
picam2.start()

photo_dir = REPO_TOP / f"pigeon_img_{seed}"
time_dir = REPO_TOP / f"time_{seed}"
os.mkdir(photo_dir)
os.mkdir(time_dir)

img_id = 100_000_000
while True:
    time.sleep(3)
    metadata = picam2.capture_file(photo_dir / ("img_" + str(img_id) + ".png"), format="png")
    print("Photo captured")
    if "SensorTimestamp" in metadata.keys():
        capture_ns = metadata["SensorTimestamp"]
        print(f"Capture: {capture_ns}")
    else:
        print("Could not find SensorTimestamp in metadata keys")
        capture_ns = -1
    file = open(time_dir / f"time_{img_id}.txt", 'w')
    file.write(str(capture_ns))
    print(f"CAPTURE ---- {capture_ns}")
    file.close()
    img_id += 1
