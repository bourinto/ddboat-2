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

    def follow_heading(self, target_heading, base_speed, kp, duration=30, Hz=10):
        start_time = time.time()
        while time.time() - start_time < duration:
            heading = self.heading()

            error = target_heading - heading
            correction = kp * sawtooth(error)
            self.motor(base_speed + correction, base_speed - correction)

            self.write_log([np.degrees(heading), correction])

            time.sleep(1. / Hz)

    def navigate_to_waypoint(self, ref_point, aimed_point, base_speed, kp, dstop=5, Hz=10):
        rho = 6400000  # approximate Earth radius in meters

        # Convert points (lat, lon in degrees) to radians
        lat_ref = np.radians(ref_point[0])
        lon_ref = np.radians(ref_point[1])

        lat_aimed = np.radians(aimed_point[0])
        lon_aimed = np.radians(aimed_point[1])

        # Compute target coordinates:
        x_target = rho * np.cos(lat_ref) * (lon_aimed - lon_ref)
        y_target = rho * (lat_aimed - lat_ref)
        target = np.array([x_target, y_target])

        # Initialize the error distance
        distance = np.inf

        while distance > dstop:
            # Read GPS
            gps = self.loc()
            lat_gps = np.radians(gps[0])
            lon_gps = np.radians(gps[1])

            # Convert GPS reading
            x_gps = rho * np.cos(lat_ref) * (lon_gps - lon_ref)
            y_gps = rho * (lat_gps - lat_ref)
            pos = np.array([x_gps, y_gps])

            # Compute control
            error = target - pos
            target_heading = np.arctan2(error[1], error[0])
            heading = self.heading()
            correction = kp * sawtooth(target_heading - heading)

            self.motor(base_speed + correction, base_speed - correction)

            # Log the current state
            distance = np.linalg.norm(error)
            self.write_log([x_gps, y_gps, target_heading, heading, correction, distance])

            time.sleep(1. / Hz)
