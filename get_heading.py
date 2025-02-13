import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import imu9_driver_v2 as imudrv
import time
import numpy as np
from calibration import load_calibration


def get_heading(imu, bmag, Amag):
    xmag, ymag, zmag = imu.read_mag_raw()

    y1 = Amag @ (np.array([[xmag], [ymag], [zmag]]) + bmag)
    y1 /= np.linalg.norm(y1)

    return np.arctan2(y1[1], y1[0])[0]


if __name__ == '__main__':
    imu = imudrv.Imu9IO()
    bmag, Amag = load_calibration("calibration_data.npz")

    while True:
        print((np.degrees(get_heading(imu, bmag, Amag)) + 360) % 360)
        time.sleep(1)