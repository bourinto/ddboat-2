import sys
import os
import time
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import imu9_driver_v2 as imu_driver
import arduino_driver_v2 as arduino_driver
from calibration import load_calibration
from get_heading import get_heading
from mini_roblib import sawtooth
import write_log

# Control parameters
Kp = 130
Kp_rot = 80
base_speed = 150

if __name__ == '__main__':
    # Initialize IMU and Arduino
    imu = imu_driver.Imu9IO()
    ard = arduino_driver.ArduinoIO()

    # Load calibration data
    bmag, Amag = load_calibration("calibration_data.npz")

    # Initialize logger and filter
    logger = write_log.Log(['heading', 'correction'])

    # Phase 1: Move NW for 30 seconds
    start_time = time.time()
    target_heading = np.radians(-45)
    while time.time() - start_time < 30:
        heading = get_heading(imu, bmag, Amag)
        correction = Kp * sawtooth(target_heading - heading)
        ard.send_arduino_cmd_motor(base_speed + correction, base_speed - correction)
        logger.write_log([np.degrees(heading), correction])

        time.sleep(0.1)

    # Phase 2: Hold position for 10 seconds while rotating
    start_time = time.time()
    target_heading = np.radians(135)
    while time.time() - start_time < 10:
        heading = get_heading(imu, bmag, Amag)
        correction = Kp_rot * sawtooth(target_heading - heading)
        ard.send_arduino_cmd_motor(correction, -correction)
        logger.write_log([np.degrees(heading), correction])

        time.sleep(0.1)

    # Phase 3: Move SE for 30 seconds
    start_time = time.time()
    target_heading = np.radians(135)
    while time.time() - start_time < 30:
        heading = get_heading(imu, bmag, Amag) + np.radians(-10)
        correction = Kp * sawtooth(target_heading - heading)
        ard.send_arduino_cmd_motor(base_speed + correction, base_speed - correction)
        logger.write_log([np.degrees(heading), correction])

        time.sleep(0.1)

    # Stop motors at the end
    ard.send_arduino_cmd_motor(0, 0)
