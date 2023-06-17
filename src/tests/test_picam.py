
import time
import libcamera
from picamera2 import Picamera2

running = False
def test_sig(future):
    global running
    print(f"----SIGNAL START---- {running}")
    running = False
    print(f"----SIGNAL END, RUNNING = {running}----")

picam2 = Picamera2()
picam2.set_controls({"AfMode": libcamera.controls.AfModeEnum.Continuous, "AfTrigger":1})
picam2.start()

print("job 1")
time.sleep(2)
running = True
job = picam2.capture_file("test.jpg", wait=False, signal_function=test_sig)
while running:
    print("running!")
    time.sleep(0.01)
print("job1:", job.get_result())

print("job 2")
time.sleep(2)
running = True
job = picam2.capture_file("test2.jpg", wait=False, signal_function=test_sig)
while running:
    print("running!")
    time.sleep(0.01)
print("job 2 finished capture")
print(job.get_result())
picam2.close()