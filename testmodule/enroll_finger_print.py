import datetime
import time
import serial

import requests
import adafruit_fingerprint

from sqlite3db import FPAttendanceSystemDB

api_register_url = "http://192.168.1.25:8000/api/register/"
delete_finger_api = "http://192.168.1.25:8000/api/registerdeletedata/"
# import board
# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
# uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi and hardware UART:
uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)

# If using with Linux/Raspberry Pi 3 with pi3-disable-bt
# uart = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=1)

finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

fp_att = FPAttendanceSystemDB()


def enroll_finger(location):
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        print("finger image: ", i)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    p_name = input("Enter your name: ")
    print("i is: ", location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
        now = datetime.datetime.now()
        register_data = {"personName": p_name, "fpid": location, "joiningdatetime": now}

        response = requests.post(api_register_url, register_data)

        print(response.status_code)

        if response.status_code == 201:
            fp_att.insert_data(p_name, now, location)
            print("finger registered successfully in db")
        elif requests.exceptions.HTTPError:
            print(response)
        # fp_att.select_registered_fp(location)
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True


def get_num(max_number):
    """Use input() to get a valid number from 0 to the maximum size
    of the library. Retry till success!"""
    i = -1
    while (i > max_number - 1) or (i < 0):
        try:
            i = int(input("Enter ID # from 0-{}: ".format(max_number - 1)))

        except ValueError:
            pass
    return i


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

    print("e) enroll print")
    print("d) delete print")
    print("----------------")

    c = input("> ")

    if c == "e":
        enroll_finger(get_num(finger.library_size))
    elif c == "d":
        f_id = get_num(finger.library_size)
        response = requests.delete(delete_finger_api+str(f_id)+"/")
        print("response delete", response, f_id)
        if response.status_code == 200:
            print("response in 200")
            fp_att.delete_registered_person(f_id)
            if finger.delete_model(f_id) == adafruit_fingerprint.OK:
                print("Deleted!")
            else:
                print("Failed to delete")
