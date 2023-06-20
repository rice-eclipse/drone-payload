import time
import sys
import random
import os
from pathlib import Path

REPO_TOP = Path(__file__).resolve().parent.parent.parent
print(REPO_TOP)
sys.path.append(os.path.join(REPO_TOP, "src/lib"))

import signal_mgmt
import pix_logging
import capturing

if __name__ == "__main__":
    vehicle = signal_mgmt.init_vehicle()

    seed = random.randint(100_000_000, 999_999_999)
    print(f"Seed: {seed}")
    img_id = 100_000_000

    img_dir = Path(os.getcwd()) / f"pigeon_img_{seed}"
    data_dir = Path(os.getcwd()) / f"pigeon_data_{seed}"
    os.mkdir(img_dir)
    os.mkdir(data_dir)

    image_file = img_dir / f"{img_id}_capture.jpg"
    camera = capturing.Camera()
    camera.take_photo(image_file)
    datalog_file = data_dir / f"{img_id}_log.csv"
    log_data = []

    # Main drone software loop
    while True:
        
        signal_mgmt.switch_override(vehicle)
        log_data.append(pix_logging.get_vehicle_fields(vehicle))

        if not camera.proc_running:
            print(f"\n-------- Camera task {img_id} complete ----------\n")
            pix_logging.save_logs(datalog_file, log_data)
            img_id += 1
            image_file = img_dir / f"{img_id}_capture.jpg"
            print("Logs saved")
            metadata, utc_time = camera.get_job_results()
            print(f"UTC TIME OF CAPTURE: {utc_time}")
            print(f"METADATA: {metadata}")
            camera.take_photo(image_file)
            datalog_file = data_dir / f"{img_id}_log.csv"
            log_data = []

        time.sleep(0.5)