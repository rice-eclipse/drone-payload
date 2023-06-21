import time
import sys
import random
import os
import subprocess
from pathlib import Path

REPO_TOP = Path(__file__).resolve().parent.parent.parent
sys.path.append(os.path.join(REPO_TOP, "src/lib"))

import signal_mgmt
import pix_logging

if __name__ == "__main__":
    vehicle = signal_mgmt.init_vehicle()

    seed = random.randint(100_000_000, 999_999_999)
    print(f"Seed: {seed}")
    data_id = 100_000_000
    photo_started = False

    data_dir = Path(REPO_TOP / f"pigeon_data_{seed}")
    os.mkdir(data_dir)
    log_data = []

    # Main drone software loop
    ticks = 0
    while True:
        datalog_file = data_dir / f"{data_id}_log.csv"
        if signal_mgmt.switch_override(vehicle) and not photo_started:
            photo_started = True
            proc = subprocess.Popen(["python3", str(Path(REPO_TOP, "src/main/photo_script.py")), str(seed)])
        data = pix_logging.get_vehicle_fields(vehicle)
        log_data.append(data)
        ticks += 1
        if ticks >= 100:
            print(f"LOGGING --- {data['Time']}")
            pix_logging.save_logs(datalog_file, log_data)
            data_id += 1
            ticks = 0
            log_data = []
        time.sleep(0.1)