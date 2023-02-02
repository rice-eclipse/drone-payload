import time

from picamera2 import Picamera2, Preview


class Camera:
    def __init__(self) -> None:
        picam2 = Picamera2()

        # Create an image capture object that contains necessary parameters parameters -> main is the actual image quality
        self.capture_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")

        # Configures the preview of the camera
        self.preview_config = picam2.create_preview_configuration()
        self.picam2.configure(self.preview_config)

        #track run status of camera
        self.started = False

        self.image_postfix = 0

    def configure(self):
        pass

    def start(self):
        # Not sure what happens if you start while its already started so added check for now
        if not self.started:
            self.picam2.start()
            time.sleep(2)
            self.started = True

    def capture(self):
        if self.started:
            print("Taking Picture")

            r = self.picam2.switch_mode_capture_request_and_stop(self.capture_config)
            r.save("main", f"../photos/image{self.image_postfix}.jpg")
            self.image_postfix += 1

            print("Image Captured")

        else:
            print("Camera not running")