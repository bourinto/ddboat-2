import numpy as np
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import arduino_driver_v2 as arduino_driver
import imu9_driver_v2 as imu_driver
import gps_driver_v2 as gpsdrv

from calibration import load_calibration
from get_heading import get_heading
from get_gps import get_gps
from mini_roblib import *

from write_log import Log


class WS3K2(Log):
    def __init__(self, headers):
        Log.__init__(self, headers)

        # Initialize IMU, Arduino and GPS
        self.imu = imu_driver.Imu9IO()
        self.ard = arduino_driver.ArduinoIO()
        self.gps_device = gpsdrv.GpsIO()
        self.gps_device.set_filter_speed('0')

        # Load calibration data
        self.bmag, self.Amag = load_calibration("calibration_data.npz")

    def motor(self, spd_left, spd_right):
        self.ard.send_arduino_cmd_motor(spd_left, spd_right)

    def heading(self):
        return get_heading(self.imu, self.bmag, self.Amag)

    def loc(self):
        return get_gps(self.gps_device)

    def keep_heading(self, target_heading, base_speed, kp, kd, duration=30, Hz=10):
        start_time = time.time()
        prev_error = 0
        while time.time() - start_time < duration:
            heading = self.heading()

            error = target_heading - heading
            derror = prev_error - error

            correction = kp * sawtooth(error) + kd * derror
            self.motor(base_speed + correction, base_speed - correction)

            self.write_log([np.degrees(heading), correction])
            prev_error = error

            time.sleep(1. / Hz)
