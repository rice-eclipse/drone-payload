import logging
import signal_mgmt
import time
import sys
import subprocess
import random
import os
from typing import List, Dict, Any

sys.append("../lib")


if __name__ == "__main__":
    vehicle = signal_mgmt.init_vehicle()

    seed = random.randint(100_000_000, 999_999_999)
    img_id = 100_000_000

    img_dir = os.getcwd() / f"pigeon_img_{seed}"
    data_dir = os.getcwd() / f"pigeon_data_{seed}"
    os.mkdir(img_dir)
    os.mkdir(data_dir)

    # TODO: Replace with camera command, imgdir
    camera_process = subprocess.Popen(["libcamera-still", "-o"])
    datalog_file = data_dir / f"{img_id}_log.csv"
    log_data = []

    while True:
        signal_mgmt.switch_override(vehicle)
        log_data.append(logging.get_vehicle_fields(vehicle))

        if camera_process.poll() is not None:
            logging.save_logs(datalog_file, log_data)
            img_id += 1
            camera_process = subprocess.Popen(["libcamera-still", "-o"])
            datalog_file = data_dir / f"{img_id}_log.csv"
            log_data = []

        time.sleep(1)
