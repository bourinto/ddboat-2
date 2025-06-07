# DDBOAT Control Project

This project controls an Unmanned Surface Vehicle (USV), the DDBOAT, using various sensors such as GPS, IMU (
magnetometer, accelerometer, gyroscope), and motor controllers. The boat is programmed to execute predefined missions
including heading control, waypoint navigation, and swarm behaviors. The
source code is organized as a Python package to simplify reuse and
deployment on the boats.

**Note:** This project is a more advanced and accomplished iteration of our previous work available
at [this link](https://gitlab.ensta-bretagne.fr/fleuryvi/ddboatws3k).

**For a demonstration and explanation, please view our [video here](https://www.youtube.com/watch?v=INGWGhuL-2k).**

## Table of Contents

- [Requirements](#requirements)
- [Connection Setup](#connection-setup)
- [Programs Overview](#programs-overview)
    - [Utilities](#utilities)
    - [Control Functions](#control-functions)
    - [Missions](#missions)
- [Authors](#authors)

## Requirements

To run this project, you need:

- A DDBOAT equipped with GPS, IMU (magnetometer, accelerometer, gyroscope), and motors controlled via Arduino.
- Access to the DARTAP WiFi network.
- SSH access to the DDBOAT.

## Connection Setup

Before running any program, follow these steps:

1. **Connect to DARTAP WiFi**:
    - Ensure your machine is connected to the DARTAP WiFi network.

2. **SSH into the DDBOAT**:
    - Open a terminal and use the following SSH command:
      ```bash
      ssh ue32@172.20.25.2XX
      ```
    - Replace `XX` with the correct DDBOAT number.

## Programs Overview

This project is organized as a Python package named **`ddboat`** with three main
subpackages: **utilities**, **core functions**, and **missions**. The utilities
and core functions provide essential support for the high-level mission scripts
located under `ddboat/missions`.

### Utilities

Located in `ddboat/utils`, these modules offer foundational support and
auxiliary functionalities:

- **client_server.py** – communication helpers for multi-boat setups
- **write_log.py** – simple CSV logging utility
- **mini_roblib.py** – mathematical helpers for navigation

### Core Functions

Located in `ddboat/core`, these modules handle the boat’s sensor data and
control computations:

- **calibration.py** – magnetometer calibration utilities
- **get_gps.py** – GPS parsing helpers
- **get_heading.py** – compute heading from IMU data
- **ws3k2_drivers.py** – main driver class for sensors and motors

### Missions

Mission scripts are found under `ddboat/missions` and build upon the core functions. They are organized in chronological order:

- **ddboat/missions/ms_round_trip.py**
  Created to test the heading calibration. The boat performs a round-trip maneuver, initially moving in one direction
  and then reversing after a calibration test.

- **ddboat/missions/ms_come_back.py**
  Commands the boat to navigate back to the pontoon using GPS data.

- **ddboat/missions/ms_fix_circle.py**
  Directs the boat to follow a circular trajectory around a static buoy. [Demonstration here.](Images/circle.mp4)
  <div align="center">
  <video width="500" controls>
    <source src="Images/circle.mp4" type="video/mp4">
  </video>
  </div>

- **ddboat/missions/ms_circle.py**
  Guides the boat along a circular path around a moving buoy (for example, another DDBOAT).

- **ddboat/missions/ms_follow_boat.py**
  Enables the boat to follow another DDBOAT. [Demonstration here.](Images/IMG_4793.MP4)
  <div align="center">
  <video width="500" controls>
    <source src="Images/IMG_4793.MP4" type="video/mp4">
  </video>
  </div>


- **ddboat/missions/ms_navtowp_swarm.py**
  A swarm test mission that launches every available DDBOAT toward the same GPS waypoint. [Demonstration here.](Images/IMG_4214.MP4)

  <div align="center">
  <video width="500" controls>
    <source src="Images/IMG_4214.MP4" type="video/mp4">
  </video>
  </div>

- **ddboat/missions/consensus.py**
  The most advanced mission where one boat is declared the leader to perform a specified mission, while the other
  DDBOATs follow its lead. [Demonstration here.](Images/consensus.MP4)

  <div align="center">
  <video width="500" controls>
    <source src="Images/consensus.mp4" type="video/mp4">
  </video>
  </div>

**Note:** You can find videos representing some of the missions directly on the README.md.

## Authors

This project was developed by:

- **BOURIN Toméo**
- **DUNOT Clément**
- **FLEURY Vianney**

From **ENSTA - Autonomous Robotic 2026**.