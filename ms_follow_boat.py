import argparse

from ws3k2_drivers import *


class MSFollow:
    def __init__(self, ip, get_gps_server_xy):
        self.ip = ip
        self.get_gps_server_xy = get_gps_server_xy

    def trajectory(self, t):
        return self.get_gps_server_xy(server_ip=self.ip)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-id", help="ddboat number")
    args = parser.parse_args()

    # Initialization
    ws3k2 = WS3K2(['x', 'y', 'xt', 'yt', 'target_heading', 'heading', 'correction', 'distance'])
    target = MSFollow("172.20.25.2" + args.id, ws3k2.get_gps_server_xy)

    print("\n===== FOLLOWING DDBOAT {} =====\n".format(args.id))
    try:
        ws3k2.follow_virtual_point(virtual_traj=target.trajectory, journey_time=np.inf)
    except:
        print("\n===== END OF COMMUNICATION =====")
        print("-> Motor stopped")
        ws3k2.motor(0, 0)
