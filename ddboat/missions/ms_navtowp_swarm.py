import re
import socket
import numpy as np

from ddboat.core.ws3k2_drivers import WS3K2
from ddboat.utils.calibration import do_calibration

if __name__ == '__main__':
    hostname = socket.gethostname()
    match = re.search(r'ddboat(\d+)', hostname)

    if match:
        boat_nb = match.group(1)
    else:
        print("Error while parsing hostname")
        sys.exit(1)

    print("\n\n\n===== WELCOME ON DDBOAT {} =====".format(boat_nb))
    time.sleep(1)
    do_calibration(boat_nb)

    os.makedirs('logs', exist_ok=True)

    print("\n\n\n===== INITIALIZATION PROCEDURE =====\n")
    ws3k2 = WS3K2(['x', 'y', 'xt', 'yt', 'target_heading', 'heading', 'correction', 'distance'])

    print("\n\n\n===== NAVIGATION TO WAYPOINT =====\n")
    coords_buoy = np.array([48.200117, -3.01574933])
    ws3k2.navigate_to_waypoint(coords_buoy, base_speed=200, kp=130, dstop=10)
