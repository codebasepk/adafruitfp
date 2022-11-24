import time

from enroll_finger_print import uart
from mark_attendance import MarkAttendance

import adafruit_fingerprint

# import serial

# uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
mark_att = MarkAttendance()


def get_fingerprint():
    """Get a finger print image, template it, and see if it matches!"""
    print("Waiting for image...")
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    print("Templating...")
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    print("Searching...")
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


# initialize LED color
led_color = 1
led_mode = 3
while True:
    # Turn on LED
    finger.set_led(color=led_color, mode=led_mode)
    print("----------------")
    if finger.read_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Fingerprint templates: ", finger.templates)
    if finger.count_templates() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to read templates")
    print("Number of templates found: ", finger.template_count)
    if finger.read_sysparam() != adafruit_fingerprint.OK:
        raise RuntimeError("Failed to get system parameters")

    if get_fingerprint():
        print("Detected #", finger.finger_id, "with confidence", finger.confidence)
        mark_att.get_finger_id(finger.finger_id)
        time.sleep(2)
        # fp_att = FPAttendanceSystemDB()
        # fp_att.select_registered_fp(finger.finger_id)
    else:
        print("Finger not found")
