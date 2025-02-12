from ws3k2_drivers import *

if __name__ == '__main__':
    # Initialization
    ws3k2 = WS3K2(['X', 'Y', 'target_heading', 'heading', 'correction', 'distance'])

    # Control
    ws3k2.navigate_to_waypoint(ws3k2.ref_point, base_speed=200, kp=130, dstop=10)

    # Stop motors at the end
    ws3k2.motor(0, 0)