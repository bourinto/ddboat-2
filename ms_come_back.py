from ws3k2_drivers import *

home = np.array([48.199024666666666, -3.0147976666666674])

if __name__ == '__main__':
    # Initialization
    ws3k2 = WS3K2(['X', 'Y', 'target_heading', 'heading', 'correction', 'distance'])

    # Control
    ws3k2.navigate_to_waypoint(home, base_speed=150, kp=130, dstop=10)

    # Stop motors at the end
    ws3k2.motor(0, 0)