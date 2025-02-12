from ws3k2_drivers import *

if __name__ == '__main__':
    # Initialization
    ws3k2 = WS3K2(['x','y','target_heading','heading', 'correction','distance'])
    

    # Phase 1: Join the circle
    print("Joining the circle")
    coords_buoy = np.array([48.200117,-3.01574933])
    ws3k2.navigate_to_waypoint(coords_buoy, base_speed=200, kp=130, dstop=20)

    # Phase 2 : Follow the circle
    print("Following the circle")

        # Convert buoy corodinates
    rho = 6400000
    lat_buoy = np.radians(coords_buoy[0])
    lon_buoy = np.radians(coords_buoy[1])
    x_buoy = rho * np.cos(np.radians(ws3k2.ref_point[0])) * (lon_buoy - np.radians(ws3k2.ref_point[1]))
    y_buoy = rho * (lat_buoy - np.radians(ws3k2.ref_point[0]))
    pos_buoy = np.array([x_buoy, y_buoy])


    def circular_traj(t):
        r = 20
        T = 100

        boat_nr = 10
        nb_boats = 18

        phi = 0

        return pos_buoy + np.array([r*np.cos(2*np.pi*t/T + phi),
                                       r*np.sin(2*np.pi*t/T + phi)])

    ws3k2.follow_virtual_point(virtual_traj=circular_traj, journey_time=200)

    # Stop motors at the end
    ws3k2.motor(0, 0)