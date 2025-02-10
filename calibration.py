import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import imu9_driver_v2 as imudrv
import numpy as np


def get_magnetometer_data():
    """
    Creates an instance of the IMU sensor and reads raw magnetometer data.
    Returns the data as a 3x1 numpy array.
    """
    imu = imudrv.Imu9IO()
    # Read raw magnetic data (x, y, z)
    x, y, z = imu.read_mag_raw()
    print("Raw magnetometer data:", x, y, z)
    return np.array([[x], [y], [z]])


def save_calibration(filename, bmag, Amag):
    """
    Saves the calibration offset and matrix to a file using NumPy's savez format.
    """
    np.savez(filename, bmag=bmag, Amag=Amag)
    print(f"Calibration data saved to {filename}")


def load_calibration(filename):
    """
    Loads calibration data from the given file and returns the bmag and Amag matrices.
    """
    data = np.load(filename)
    bmag = data['bmag']
    Amag = data['Amag']
    return bmag, Amag


if __name__ == "__main__":
    print("=== Magnetometer Calibration Process ===")
    print("You will be prompted to position the boat in 4 orientations and press Enter.")

    # Fixed calibration parameters:
    B = 46  # micro Tesla
    I = 64 / 180 * np.pi  # Angle of incidence in radians

    # For each orientation, wait for user confirmation then capture raw data.
    input("Place the boat in the NORTH orientation and press Enter...")
    xN = get_magnetometer_data()
    print("Data: ", xN)

    input("Place the boat in the SOUTH orientation and press Enter...")
    xS = get_magnetometer_data()
    print("Data: ", xS)

    input("Place the boat in the WEST orientation and press Enter...")
    xW = get_magnetometer_data()
    print("Data: ", xW)

    input("Place the boat in the UP orientation and press Enter...")
    xU = get_magnetometer_data()
    print("Data: ", xU)

    # Define expected magnetic field vectors for each orientation:
    yN = np.array([[B * np.cos(I)], [0], [-B * np.sin(I)]])
    yS = np.array([[-B * np.cos(I)], [0], [B * np.sin(I)]])
    yW = np.array([[0], [-B * np.cos(I)], [-B * np.sin(I)]])
    yU = np.array([[-B * np.sin(I)], [0], [B * np.cos(I)]])

    # Compute offset (bmag) using the North and South measurements:
    bmag = -(xN + xS) / 2

    # Build the Y and X matrices for the calibration:
    Y = np.hstack((yN, yW, yU))
    X = np.hstack((xN + bmag, xW + bmag, xU + bmag))

    # Compute the calibration matrix Amag
    Amag = X @ np.linalg.inv(Y)
    Amag_inv = np.linalg.inv(Amag)

    # Print the calibration results:
    print("\n--- Calibration Results ---")
    print("Calibration offset (bmag):\n", bmag)
    print("Calibration matrix (Amag):\n", Amag_inv)

    # Save the calibration data for later use:
    calibration_filename = "calibration_data.npz"
    save_calibration(calibration_filename, bmag, Amag_inv)

    # bmag, Amag = load_calibration("calibration_data.npz")
