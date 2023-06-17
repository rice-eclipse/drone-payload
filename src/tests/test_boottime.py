import psutil
import datetime
import time

boot_time = psutil.boot_time()
boot_time_utc = datetime.datetime.utcfromtimestamp(boot_time)

# Get the current time in microseconds
current_time_micros = int(time.time() * 1e6)

# Calculate the boot time in microseconds
boot_time_micros = int(boot_time_utc.timestamp() * 1e6)

# Calculate the time since boot in microseconds
time_since_boot_micros = current_time_micros - boot_time_micros

print("System boot time (UTC):", boot_time_utc)
print("Time since boot (microseconds):", time_since_boot_micros)