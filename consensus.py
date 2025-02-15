import sys

sys.path.append('/home/ue32/grp09')

from ws3k2_drivers import *
import subprocess
import socket
import re

if __name__ == '__main__':

    hostname = socket.gethostname()
    match = re.search(r'ddboat(\d+)', hostname)

    if match:
        boat_nb = match.group(1)
        os.makedirs('logs', exist_ok=True)
    else:
        print("Error while parsing hostname")
        sys.exit(1)

    print("\n\n\n===== WELCOME ON DDBOAT {} =====".format(boat_nb))
    time.sleep(1)
    do_calibration(boat_nb)

    try:
        with open("config.txt", "r") as file:
            ids = [line.strip() for line in file.readlines()]
        time.sleep(1)
    except:
        print("\nError while parsing config.txt")
        sys.exit(1)

    print("\n===== INITIALIZATION PROCEDURE =====\n")
    leader_id = min(ids)

    if boat_nb == leader_id:
        print("----- You are the Leader -----\n")
        subprocess.run("/usr/bin/python3 /home/ue32/grp09/ms_fix_circle.py", shell=True, executable="/bin/bash")

    else:
        print("----- You are a Sidekick -----\n")
        subprocess.run("/usr/bin/python3 /home/ue32/grp09/ms_follow_boat.py -id " + leader_id, shell=True,
                       executable="/bin/bash")
