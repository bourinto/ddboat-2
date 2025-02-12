from ws3k2_drivers import *


class MSCircle:
    def __init__(self, radius, period, center_functiun, boat_id=10, boat_nb=11):
        self.radius = radius
        self.period = period
        self.center = center_functiun
        self.boat_id = boat_id
        self.boat_nb = boat_nb

    @property
    def phase(self):
        return 2 * np.pi / self.period * self.boat_id / self.boat_nb

    def trajectory(self, t):
        return self.center() + np.array([self.radius * np.cos(2 * np.pi * t / self.period + self.phase),
                                         self.radius * np.sin(2 * np.pi * t / self.period + self.phase)])


if __name__ == '__main__':
    # Initialization
    ws3k2 = WS3K2(['x', 'y', 'xt', 'yt', 'target_heading', 'heading', 'correction', 'distance'])

    # Convert buoy cordinates
    coords_buoy = np.array([48.200117, -3.01574933])
    pos_buoy = ws3k2.gps_to_xy(coords_buoy)


    def static_buoy(): return pos_buoy


    print("\n===== Following the circle =====\n")

    circle = MSCircle(30, 200, static_buoy)
    ws3k2.follow_virtual_point(virtual_traj=circle.trajectory, journey_time=450)

    # Come back at end
    ws3k2.navigate_to_waypoint(ws3k2.ref_point, base_speed=200, kp=130, dstop=9)
    ws3k2.motor(0, 0)
