import socket
import re
from ws3k2_drivers import *

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
