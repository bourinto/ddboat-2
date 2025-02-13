import numpy as np
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import arduino_driver_v2 as arduino_driver
import imu9_driver_v2 as imu_driver
import gps_driver_v2 as gpsdrv

from calibration import load_calibration, do_calibration
from get_heading import get_heading
from get_gps import get_gps_wt, convert_gps_coordinate
from mini_roblib import *
from client_server import robot2_client_onetime

from write_log import Log


class WS3K2:
    def __init__(self, headers=['x', 'y', 'target_heading', 'heading', 'correction', 'distance']):
        self.logger = Log(headers)

        # Initialize IMU, Arduino and GPS
        self.imu = imu_driver.Imu9IO()
        self.ard = arduino_driver.ArduinoIO()
        self.gps_device = gpsdrv.GpsIO()
        self.gps_device.set_filter_speed('0')
        self.gps_data_server = None

        # Load calibration data
        self.bmag, self.Amag = load_calibration("calibration_data.npz")

        # Reference variables
        self.ref_point = np.array([48.19900500000001, -3.0148363333333332])
        self.rho = 6400000

    def motor(self, spd_left, spd_right):
        self.ard.send_arduino_cmd_motor(spd_left, spd_right)

    def heading(self):
        return get_heading(self.imu, self.bmag, self.Amag)

    def gps_to_xy(self, gps):
        lat_gps = np.radians(gps[0])
        lon_gps = np.radians(gps[1])

        # Convert GPS reading
        x_gps = self.rho * np.cos(np.radians(self.ref_point[0])) * (lon_gps - np.radians(self.ref_point[1]))
        y_gps = self.rho * (lat_gps - np.radians(self.ref_point[0]))
        return np.array([x_gps, y_gps])

    def loc(self, with_time=False, rho=6400000):
        # Read GPS
        gps, timestamp = get_gps_wt(self.gps_device)
        # Conversion
        pos = self.gps_to_xy(gps)
        return (pos, timestamp) if with_time else pos

    def get_gps_server(self, server_ip="172.20.25.217"):
        measured_gps_data_server = robot2_client_onetime(server_ip)
        if len(measured_gps_data_server) != 0:
            self.gps_data_server = measured_gps_data_server
        lat, ns, lon, ew = self.gps_data_server.split(';')[:4]
        lat, lon = float(lat), float(lon)
        lat, lon = convert_gps_coordinate(lat), convert_gps_coordinate(lon)
        if ns[0] == 'S':
            lat = -lat
        if ew[0] == 'W':
            lon = -lon
        return np.array([lat, lon])

    def get_gps_server_xy(self, server_ip="172.20.25.217"):
        gps = self.get_gps_server(server_ip)
        pos = self.gps_to_xy(gps)
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

    def navigate_to_waypoint(self, aimed_point, base_speed, kp, dstop=5, Hz=10):
        # Compute target coords
        target = self.gps_to_xy(aimed_point)

        # Initialize the error distance
        distance = np.inf

        while distance > dstop:
            pos = self.loc()
            # Compute control
            error = target - pos
            target_heading = np.arctan2(error[0], error[1])
            heading = self.heading()
            correction = kp * sawtooth(target_heading - heading)

            self.motor(base_speed + correction, base_speed - correction)

            # Log the current state
            distance = np.linalg.norm(error)
            self.logger.write_log([pos[0], pos[1], target[0], target[1], target_heading, heading, correction, distance])

            time.sleep(1. / Hz)

    def follow_virtual_point(self, virtual_traj, journey_time):
        t0 = time.time()

        heading_kP = 130
        speed_kP = 25

        while time.time() - t0 < journey_time:
            pos, timestamp = self.loc(with_time=True)
            target = virtual_traj(time.time())
            error = target - pos

            target_heading = np.arctan2(error[0], error[1])
            heading = self.heading()
            heading_error = sawtooth(target_heading - heading)
            heading_correction = heading_kP * heading_error

            distance_error = np.linalg.norm(error)
            if distance_error < 2:
                base_speed = 0
            elif distance_error < 10:
                base_speed = speed_kP * distance_error
            else:
                base_speed = 250

            self.motor(base_speed + heading_correction, base_speed - heading_correction)

            self.logger.write_log(
                [pos[0], pos[1], target[0], target[1], np.degrees(target_heading), np.degrees(heading),
                 heading_correction, distance_error])

            time.sleep(0.1)