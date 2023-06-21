
import time
import libcamera
import sys
import os
from picamera2 import Picamera2
from pathlib import Path
import datetime
import psutil

boot_utc_micros = int(datetime.datetime.utcfromtimestamp(psutil.boot_time()).timestamp() * 1e6)

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
    metadata = picam2.capture_file(photo_dir / f"img_{img_id}.jpg")
    if "SensorTimestamp" in metadata.keys():
        capture_utc_micros = metadata["SensorTimestamp"] / 1000 + boot_utc_micros
    else:
        print("Could not find SensorTimestamp in metadata keys")
        capture_utc_micros = -1
    file = open(time_dir / f"time_{img_id}.txt", 'w')
    file.write(str(capture_utc_micros))
    file.close()
    img_id += 1
    time.sleep(0.5)
