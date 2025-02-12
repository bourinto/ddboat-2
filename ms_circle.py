from ws3k2_drivers import *


class MSCircle:
    def __init__(self, radius, period, center, boat_id=10, boat_nb=11):
        self.radius = radius
        self.period = period
        self.center = center
        self.boat_id = boat_id
        self.boat_nb = boat_nb

    @property
    def phase(self):
        return 2 * np.pi / self.period * self.boat_id / self.boat_nb

    def circular_traj(self, t):
        return self.center + np.array([self.radius * np.cos(2 * np.pi * t / self.period + self.phase),
                                       self.radius * np.sin(2 * np.pi * t / self.period + self.phase)])


if __name__ == '__main__':
    # Initialization
    ws3k2 = WS3K2(['x', 'y', 'target_heading', 'heading', 'correction', 'distance'])

    # Phase 1: Join the circle
    print("\n===== Joining the circle =====")
    coords_buoy = np.array([48.200117, -3.01574933])
    ws3k2.navigate_to_waypoint(coords_buoy, base_speed=200, kp=130, dstop=20)

    # Phase 2 : Follow the circle
    print("\n===== Following the circle =====")
    # Convert buoy cordinates
    rho = 6400000
    lat_buoy = np.radians(coords_buoy[0])
    lon_buoy = np.radians(coords_buoy[1])
    x_buoy = rho * np.cos(np.radians(ws3k2.ref_point[0])) * (lon_buoy - np.radians(ws3k2.ref_point[1]))
    y_buoy = rho * (lat_buoy - np.radians(ws3k2.ref_point[0]))
    pos_buoy = np.array([x_buoy, y_buoy])

    circle = MSCircle(30, 200, pos_buoy)
    ws3k2.follow_virtual_point(virtual_traj=circle.circular_traj, journey_time=200)

    # Stop motors at the end
    ws3k2.motor(0, 0)
