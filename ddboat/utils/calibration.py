import os
import sys

sys.path.append(
    os.path.join(os.path.dirname(__file__), '..', 'drivers-ddboat-v2')
)
import imu9_driver_v2 as imudrv
import numpy as np

# Fixed calibration parameters:
B = 46  # micro Tesla
I = 64 / 180 * np.pi  # Angle of incidence in radians


def get_magnetometer_data():
    """
    Creates an instance of the IMU sensor and reads raw magnetometer data.
    Returns the data as a 3x1 numpy array.
    """
    # Read raw magnetic data (x, y, z)
    x, y, z = imu.read_mag_raw()
    print("Raw magnetometer data: {} {} {}\n".format(x, y, z))
    return np.array([[x], [y], [z]])


def compute_calibration(xN, xS, xW, xU):
    """
    Compute calibration matrices using magnetometer raw data.
    """
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
    return bmag, np.linalg.inv(Amag)


def save_calibration(filename, bmag, Amag):
    """
    Saves the calibration offset and matrix to a file using NumPy's savez format.
    """
    np.savez(filename, bmag=bmag, Amag=Amag)
    print("\nCalibration data saved to {}".format(filename))


def load_calibration(filename):
    """
    Loads calibration data from the given file and returns the bmag and Amag matrices.
    """
    data = np.load(filename)
    bmag = data['bmag']
    Amag = data['Amag']
    return bmag, Amag


def do_calibration(boat_nb):
    """
    Execute the calibration procedure using calib_12.txt file and save the calibration data.
    """
    filename = "calib_" + boat_nb + ".txt"

    try:
        # Read the file and extract values
        with open(filename, "r") as file:
            lines = file.readlines()
            values = [float(line.strip()) for line in lines]  # Convert each line to float

        # Ensure the file contains exactly 12 values
        if len(values) != 12:
            print("Error: calib_12.txt must contain exactly 12 lines (3 values for each orientation).")
            return

        # Assign values to respective orientation variables
        xN = np.array([[values[0]], [values[1]], [values[2]]])
        xS = np.array([[values[3]], [values[4]], [values[5]]])
        xW = np.array([[values[6]], [values[7]], [values[8]]])
        xU = np.array([[values[9]], [values[10]], [values[11]]])

        # Compute calibration data
        bmag, Amag = compute_calibration(xN, xS, xW, xU)
        print("\n--- Calibration Results ---\n")
        print("Calibration offset (bmag):\n{}".format(bmag))
        print("Calibration matrix (Amag):\n{}".format(Amag))

        # Save the calibration data
        calibration_filename = "calibration_data.npz"
        save_calibration(calibration_filename, bmag, Amag)

    except FileNotFoundError:
        print("Error: {} file not found.".format(filename))
    except ValueError:
        print("Error: {} contains invalid data. Ensure all values are numeric.".format(filename))


if __name__ == "__main__":
    imu = imudrv.Imu9IO()
    print("\n\n\n=== Magnetometer Calibration Process ===")
    print("You will be prompted to position the boat in 4 orientations and press Enter.\n")

    # For each orientation, wait for user confirmation then capture raw data.
    input("Place the boat in the NORTH orientation and press Enter...")
    xN = get_magnetometer_data()

    input("Place the boat in the SOUTH orientation and press Enter...")
    xS = get_magnetometer_data()

    input("Place the boat in the WEST orientation and press Enter...")
    xW = get_magnetometer_data()

    input("Place the boat in the UP orientation and press Enter...")
    xU = get_magnetometer_data()

    bmag, Amag = compute_calibration(xN, xS, xW, xU)

    # Print the calibration results:
    print("\n--- Calibration Results ---")
    print("Calibration offset (bmag):\n{}".format(bmag))
    print("Calibration matrix (Amag):\n{}".format(Amag))

    # Save the calibration data for later use:
    calibration_filename = "calibration_data.npz"
    save_calibration(calibration_filename, bmag, Amag)

    # Example usage of the load_calibration function:
    # bmag, Amag = load_calibration("calibration_data.npz")
