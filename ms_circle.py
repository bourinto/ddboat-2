from ws3k2_drivers import *

if __name__ == '__main__':
    # Initialization
    ws3k2 = WS3K2(['x','y','target_heading','heading', 'correction','distance'])
    

    # Phase 1: Join the circle
    coords_buoy = np.array([48.20010, -3.01573])
    ws3k2.navigate_to_waypoint(coords_buoy, base_speed=150, kp=130, dstop=10)

    # Phase 2 : Follow the circle
    def circular_traj(t, boat = ws3k2):
        r = 40
        T = 450

        boat_nr = 10
        nb_boats = 18

        # Convert buoy corodinates
        rho = 6400000
        lat_buoy = coords_buoy[0]
        lon_buoy = coords_buoy[1]
        x_buoy = rho * np.cos(boat.ref_point[0]) * (lon_buoy - boat.ref_point[1])
        y_buoy = rho * (lat_buoy - boat.ref_point[0])
        pos_buoy = np.array([x_buoy, y_buoy])

        return pos_buoy + np.array([r*np.cos(2*np.pi*t/T),
                                       r*np.sin(2*np.pi*t/T)])

    ws3k2.follow_virtual_point(virtual_traj=circular_traj, journey_time=200)

    # Stop motors at the end
    ws3k2.motor(0, 0)