from dronekit import connect
import subprocess
import os
import csv

vehicle = connect('/dev/ttyS0', wait_ready=True, baud=57600)

print("Vehicle connected!")
print("Autopilot Firmware version: %s" % vehicle.version)
print("Autopilot capabilities (supports ftp): %s" % vehicle.capabilities.ftp)
print("Global Location: %s" % vehicle.location.global_frame)
print ("Global Location (relative altitude): %s" % vehicle.location.global_relative_frame)
print ("Local Location: %s" % vehicle.location.local_frame)    #NED
print ("Attitude: %s" % vehicle.attitude)
print ("Velocity: %s" % vehicle.velocity)
print ("GPS: %s" % vehicle.gps_0)
print ("Groundspeed: %s" % vehicle.groundspeed)
print ("Airspeed: %s" % vehicle.airspeed)
print ("Gimbal status: %s" % vehicle.gimbal)
print ("Battery: %s" % vehicle.battery)
print ("EKF OK?: %s" % vehicle.ekf_ok)
print ("Last Heartbeat: %s" % vehicle.last_heartbeat)
print ("Rangefinder: %s" % vehicle.rangefinder)
print ("Rangefinder distance: %s" % vehicle.rangefinder.distance)
print ("Rangefinder voltage: %s" % vehicle.rangefinder.voltage)
print ("Heading: %s" % vehicle.heading)
print ("Is Armable?: %s" % vehicle.is_armable)
print ("System status: %s" % vehicle.system_status.state)
print ("Mode: %s" % vehicle.mode.name)    # settable
print ("Armed: %s" % vehicle.armed)    # settable

datafile = open("../data.csv", "w")
fieldnames = ['Global Location', 'Local Location', 'Attitude', 'Velocity', 'GPS', 'Heading']
dw = csv.DictWriter(datafile, fieldnames=fieldnames)
dw.writeheader()
full_data = []

for i in range(20):
    print("Taking photo")
    result = subprocess.run(['libcamera-still', '--autofocus', '-o', '../photos/test{i}.png'])
    print("Subprocess Complete")
    data = {}
    data['Global Location'] = vehicle.location.global_frame
    data['Local Location'] = vehicle.location.local_frame
    data['Attitude'] = vehicle.attitude
    data['Velocity'] = vehicle.velocity
    data['GPS'] = vehicle.gps_0
    data['Heading'] = vehicle.heading
    dw.writerow(data)
    print('Row written')
        
datafile.close()