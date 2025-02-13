# DDBOAT Control Project

This project controls a drone boat (DDBOAT) using various sensors such as GPS, IMU (magnetometer, accelerometer, gyroscope), and motor controllers. The boat is programmed to follow predefined missions involving heading control, waypoint navigation, and circular trajectory following.

**Demonstration and explanatory video available by** [**clicking here.**](https://www.youtube.com/watch?v=n9koBU_pk7A)

## Table of Contents
- [Requirements](#requirements)
- [Connection Setup](#connection-setup)
- [Project Structure](#project-structure)
- [How to Run the Missions](#how-to-run-the-missions)
- [Authors](#authors)

## Requirements
To run this project, you need:
- A DDBOAT equipped with GPS, IMU (magnetometer, accelerometer, gyroscope), and motors controlled via Arduino.
- Access to the DARTAP WiFi network.
- SSH access to the DDBOAT.

## Connection Setup

Before running any mission, follow these steps:

1. **Connect to DARTAP WiFi**:
   - Ensure your machine is connected to the DARTAP WiFi network.

2. **SSH into the DDBOAT**:
   - Open a terminal and use the following SSH command:
     ```bash
     ssh ue32@172.20.25.2XX
     ```
   - Replace `XX` with the correct DDBOAT number.

## Project Structure

This project includes several key Python scripts and modules:

- **ws3k2_drivers.py**: Contains the `WS3K2` class for controlling the boat's motors, GPS navigation, and heading adjustments.
- **calibration_data.npz**: Contains the calibration offset (`bmag`) and matrix (`Amag`) for the IMU's magnetometer, used to correct raw magnetometer data for accurate heading calculations.
- **write_log.py**: A logging utility for recording the boat's data, such as position, heading, and correction values, into CSV files.
- **ms_round_trip.py**: A mission where the boat moves northwest for 30 seconds, stops and rotates, then moves southeast for 30 seconds.
- **ms_come_back.py**: A mission where the boat navigates back to a predefined home location.
- **ms_circle.py**: A mission where the boat follows a circular trajectory around a buoy.
- **mini_roblib.py**: Contains helper functions like `sawtooth` (for error correction) and rotation matrix calculations.
- **get_heading.py**: Interfaces with the IMU to compute the boat's heading.
- **get_gps.py**: Interfaces with the GPS device to fetch and convert GPS coordinates.

## How to Run the Missions

Once connected to the DDBOAT via SSH, you can execute any of the missions by following these steps:

1. **Run a mission**:
   - Each mission script corresponds to a different task. For instance, to run the **round_trip** mission:
     ```bash
     python3 ms_round_trip.py
     ```

2. **Mission Descriptions (by chronological order)**:
   - **ms_round_trip.py**: The boat moves northwest for 30 seconds, then rotates to face southeast, and moves southeast for another 30 seconds.(Day 1)
   - **ms_come_back.py**: The boat navigates back to a specified home location.(Often useful)
   - **ms_circle.py**: The boat follows a circular trajectory around a buoy. The trajectory is dynamically calculated over time.(Day 2)

3. **Logging**:
   - Each mission logs critical data such as GPS coordinates, heading, correction values, and distance to a CSV file (`logs/{timestamp}.csv`). This log can be reviewed after the mission for analysis.

## Authors

This project was developed by:
- **BOURIN Toméo**, **DUNOT Clément**, **FLEURY Vianney** 

From **ENSTA Bretagne ROB 26**.
