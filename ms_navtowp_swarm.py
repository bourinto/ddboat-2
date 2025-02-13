from ws3k2_drivers import *

if __name__ == '__main__':
    ws3k2 = WS3K2(['x', 'y', 'xt', 'yt', 'target_heading', 'heading', 'correction', 'distance'])
    coords_buoy = np.array([48.200117, -3.01574933])
    pos_buoy = ws3k2.gps_to_xy(coords_buoy)
    ws3k2.navigate_to_waypoint(coords_buoy, base_speed=200, kp=130, dstop=10)
