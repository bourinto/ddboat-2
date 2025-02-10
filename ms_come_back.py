import sys
import os
import time
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import imu9_driver_v2 as imu_driver
import arduino_driver_v2 as arduino_driver
from mini_roblib import sawtooth
from calibration import load_calibration
from get_heading import get_heading
from get_gps import get_gps


def go_straight_gps(ref_point, aimed_point, straight_speed, kp, eps=5, Hz=5):
        rho = 6400000

        lxm = np.radians(ref_point[0])
        lym = np.radians(ref_point[1])

        aimed_point = np.radians(aimed_point)  # Bouée
        axtilde, aytilde = rho * np.cos(aimed_point[1]) * (aimed_point[0] - lxm), rho * (aimed_point[1] - lym)

        a = np.array([axtilde, aytilde])
        d = np.inf

        while np.linalg.norm(d) > eps:
            gps = get_gps()
            lx, ly = np.radians(gps[0]), np.radians(gps[1])
            xtilde, ytilde = rho * np.cos(ly) * (lx - lxm), rho * (ly - lym)

            p = np.array([xtilde, ytilde])
            d = a - p

            goal = np.arctan2(d[1], d[0])
            psi = get_heading(imu, bmag, Amag)
            corr = kp * sawtooth(goal - psi)

            ard.send_arduino_cmd_motor(straight_speed + corr, straight_speed - corr)
            print(np.linalg.norm(d))
            print(np.degrees(psi))
            print(np.degrees(goal))
            print("")
            time.sleep(1 / Hz)


bridge = np.array([48.199024666666666, -3.0147976666666674])

if __name__ == '__main__':
    # Initialize IMU and Arduino
    imu = imu_driver.Imu9IO()
    ard = arduino_driver.ArduinoIO()

    # Load calibration data
    bmag, Amag = load_calibration("calibration_data.npz")

    go_straight_gps(bridge, bridge, 150, 400, eps=3, Hz=5)
