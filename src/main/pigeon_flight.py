import signal_mgmt
import logging
import time
import sys
import subprocess
import random
import os

sys.append("../lib")

import config_vars

if __name__ == "__main__":
    vehicle = signal_mgmt.init_vehicle()

    seed = random.randint(100_000_000, 999_999_999)
    print(f"Seed: {seed}")
    img_id = 100_000_000

    img_dir = os.getcwd() / f"pigeon_img_{seed}"
    data_dir = os.getcwd() / f"pigeon_data_{seed}"
    os.mkdir(img_dir)
    os.mkdir(data_dir)

    image_file = img_dir / f"{img_id}_capture.jpg"
    camera_process = subprocess.Popen([*config_vars.PHOTO_CMD, str(image_file)])
    datalog_file = data_dir / f"{img_id}_log.csv"
    log_data = []

    while True:

        signal_mgmt.switch_override(vehicle)
        log_data.append(logging.get_vehicle_fields(vehicle))

        if camera_process.poll() is not None:
            logging.save_logs(datalog_file, log_data)
            img_id += 1
            camera_process = subprocess.Popen([*config_vars.PHOTO_CMD, str(image_file)])
            datalog_file = data_dir / f"{img_id}_log.csv"
            log_data = []

        time.sleep(0.5)