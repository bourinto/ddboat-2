from ws3k2_drivers import *
from ms_fix_circle import MSCircle

if __name__ == '__main__':
    # Initialization
    ws3k2 = WS3K2(['x', 'y', 'xt', 'yt', 'target_heading', 'heading', 'correction', 'distance'])

    print("\n===== Following the circle =====\n")

    circle = MSCircle(30, 200, ws3k2.get_gps_server_xy)
    ws3k2.follow_virtual_point(virtual_traj=circle.trajectory, journey_time=450)

    # Come back at end
    ws3k2.navigate_to_waypoint(ws3k2.ref_point, base_speed=200, kp=130, dstop=9)