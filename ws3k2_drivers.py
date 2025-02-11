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


class WS3K2():
    def __init__(self, headers):
        self.logger = Log(headers)

        # Initialize IMU, Arduino and GPS
        self.imu = imu_driver.Imu9IO()
        self.ard = arduino_driver.ArduinoIO()
        self.gps_device = gpsdrv.GpsIO()
        self.gps_device.set_filter_speed('0')

        # Load calibration data
        self.bmag, self.Amag = load_calibration("calibration_data.npz")

        # Reference variables
        self.ref_point = (48.19900500000001, -3.0148363333333332)

    def motor(self, spd_left, spd_right):
        self.ard.send_arduino_cmd_motor(spd_left, spd_right)

    def heading(self):
        return get_heading(self.imu, self.bmag, self.Amag)

    def loc(self,rho=6400000):
        # Read GPS
        gps = get_gps(self.gps_device)
        lat_gps = np.radians(gps[0])
        lon_gps = np.radians(gps[1])

        # Convert GPS reading
        x_gps = rho * np.cos(self.ref_point[0]) * (lon_gps - self.ref_point[1])
        y_gps = rho * (lat_gps - self.ref_point[0])
        pos = np.array([x_gps, y_gps])
        return pos

    def follow_heading(self, target_heading, base_speed, kp, duration=30, Hz=10):
        start_time = time.time()
        while time.time() - start_time < duration:
            heading = self.heading()

            error = target_heading - heading
            correction = kp * sawtooth(error)
            self.motor(base_speed + correction, base_speed - correction)

            self.logger.write_log([np.degrees(heading), correction])

            time.sleep(1. / Hz)

    def navigate_to_waypoint(self, aimed_point, base_speed , kp, dstop=5, Hz=10):
        rho = 6400000  # approximate Earth radius in meters

        # Convert points (lat, lon in degrees) to radians
        lat_ref = np.radians(self.ref_point[0])
        lon_ref = np.radians(self.ref_point[1])

        lat_aimed = np.radians(aimed_point[0])
        lon_aimed = np.radians(aimed_point[1])

        # Compute target coordinates:
        x_target = rho * np.cos(lat_ref) * (lon_aimed - lon_ref)
        y_target = rho * (lat_aimed - lat_ref)
        target = np.array([x_target, y_target])

        # Initialize the error distance
        distance = np.inf

        while distance > dstop:
            pos = self.loc()
            # Compute control
            error = target - pos
            target_heading = np.arctan2(error[1], error[0])
            heading = self.heading()
            correction = kp * sawtooth(target_heading - heading)

            self.motor(base_speed + correction, base_speed - correction)

            # Log the current state
            distance = np.linalg.norm(error)
            self.logger.write_log([pos[0], pos[1], target_heading, heading, correction, distance])

            time.sleep(1. / Hz)


    def follow_virtual_point(self, virtual_traj, journey_time):
        t0 = time.time()
        t = 0

        heading_kP = 130
        speed_kP = 15

        while t < journey_time:
            t = time.time()-t0
            target = virtual_traj(t)

            error = target - self.loc
            target_heading = np.arctan2(error[1], error[0])
            heading = self.heading()
            heading_error = sawtooth(target_heading - heading)
            heading_correction = heading_kP * heading_error

            distance_error = np.linalg.norm(error)
            if distance_error < 10:
                base_speed = speed_kP * distance_error
            else:
                base_speed = 150

            self.motor(base_speed + heading_correction, base_speed - heading_correction)

            self.logger.write_log([np.degrees(heading), heading_correction])

            time.sleep(0.1)