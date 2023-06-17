
import time
import sys
import os
from picamera2 import Picamera2
import libcamera
from pathlib import Path

REPO_TOP = Path(__file__).resolve().parent.parent.parent
sys.path.append(os.path.join(REPO_TOP, "src/lib"))

seed = int(sys.argv[1])
print(f"seed = {seed}")
picam2 = Picamera2()
picam2.start()
picam2.set_controls({'AfMode': libcamera.controls.AfModeEnum.Manual, 'LensPosition': 1.5})

photo_dir = REPO_TOP / f"pigeon_img_{seed}"
time_dir = REPO_TOP / f"time_{seed}"
os.mkdir(photo_dir)
os.mkdir(time_dir)

img_id = 100_000_000
while True:
    time.sleep(3)
    cycle_result = picam2.autofocus_cycle()
    metadata = picam2.capture_file(photo_dir / ("img_" + str(img_id) + ".png"), format="png")
    state = metadata['AfState']
    print("Photo captured")
    print(f"Cycle success: {cycle_result}")
    if state == libcamera.controls.AfStateEnum.Focused:
        print("capture focused!")
    elif state == libcamera.controls.AfStateEnum.Failed:
        print("capture failed")
    else:
        print(f"wack capture state: {state}")

    if "SensorTimestamp" in metadata.keys():
        capture_ns = metadata["SensorTimestamp"]
        print(f"Capture: {capture_ns}")
    else:
        print("Could not find SensorTimestamp in metadata keys")
        capture_ns = -1
    file = open(time_dir / f"time_{img_id}.txt", 'w')
    file.write(str(capture_ns))
    file.write(f"\n{'Autofocus success' if cycle_result else 'Autofocus failure'}")
    print(f"CAPTURE ---- {capture_ns}")
    file.close()
    img_id += 1
