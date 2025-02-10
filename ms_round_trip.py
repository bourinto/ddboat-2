from ws3k2_drivers import *

if __name__ == '__main__':
    # Initializations
    ws3k2 = WS3K2(['heading', 'correction'])

    # Phase 1: Move NW for 30 seconds
    ws3k2.keep_heading(np.radians(-45), base_speed=150, kp=130, kd=0)

    # Phase 2: Hold position for 10 seconds while rotating
    ws3k2.keep_heading(np.radians(135), base_speed=0, kp=130, kd=0, duration=10)

    # Phase 3: Move SE for 30 seconds
    ws3k2.keep_heading(np.radians(135), base_speed=0, kp=130, kd=0)

    # Stop motors at the end
    ws3k2.motor(0, 0)
