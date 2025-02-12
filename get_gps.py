import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'drivers-ddboat-v2'))
import gps_driver_v2 as gpsdrv


def convert_gps_coordinate(raw_value):
    """Converts GPS coordinate format from DDMM.MMMM to decimal degrees."""
    degrees = raw_value // 100
    minutes = raw_value % 100
    return degrees + (minutes / 60)


def get_gps(gps_device):
    """Fetches latitude and longitude from the GPS device."""
    while True:
        success, gps_data = gps_device.read_gll_non_blocking()
        if success:
            latitude = convert_gps_coordinate(gps_data[0]) * (1 if gps_data[1] == 'N' else -1)
            longitude = convert_gps_coordinate(gps_data[2]) * (1 if gps_data[3] == 'E' else -1)
            return latitude, longitude


def get_gps_wt(gps_device):
    """Fetches GPS coordinates along with the timestamp."""
    while True:
        success, gps_data = gps_device.read_gll_non_blocking()
        if success:
            latitude = convert_gps_coordinate(gps_data[0]) * (1 if gps_data[1] == 'N' else -1)
            longitude = convert_gps_coordinate(gps_data[2]) * (1 if gps_data[3] == 'E' else -1)
            timestamp = gps_data[-1]
            return (latitude, longitude), timestamp


def average_gps_coordinates(gps_device, samples=10):
    """Calculates an averaged GPS coordinate over a given number of samples."""
    total_lat, total_long = 0, 0
    for _ in range(samples):
        lat, long = get_gps(gps_device)
        total_lat += lat
        total_long += long
        time.sleep(0.1)
    return total_lat / samples, total_long / samples


if __name__ == '__main__':
    # Initialize GPS module
    gps_device = gpsdrv.GpsIO()
    gps_device.set_filter_speed('0')

    print("Processing GPS data...")
    avg_lat, avg_long = average_gps_coordinates(gps_device)
    print("Averaged Coordinates: Latitude: {avg_lat}, Longitude: {avg_long}".format(avg_lat=avg_lat, avg_long=avg_long))

# Bridge = Latitude: 48.19900500000001, Longitude: -3.0148363333333332
