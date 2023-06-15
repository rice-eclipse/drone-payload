import config_vars
import csv
import os
import sys
from typing import List, Dict, Any

sys.path.append("../main")


def get_vehicle_fields(vehicle):
    '''
    Gets the relevant vehicle fields for logging
    '''
    data = {}
    data['Global Location'] = vehicle.location.global_frame
    data['Local Location'] = vehicle.location.local_frame
    data['Attitude'] = vehicle.attitude
    data['Velocity'] = vehicle.velocity
    data['GPS'] = vehicle.gps_0
    data['Heading'] = vehicle.heading
    return data


def save_logs(filepath: os.PathLike, log_data: List[Dict[str, Any]]):
    """
    Saves a list of dictionary fields to a csv file
    """
    file = open(filepath, "w")
    dw = csv.DictWriter(file, fieldnames=config_vars.LOGGING_FIELD_NAMES)
    dw.writeheader()
    [dw.writerow(data) for data in log_data]
    file.close()
