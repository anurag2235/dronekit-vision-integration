#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
© Copyright 2015-2016, 3D Robotics.
simple_goto.py: GUIDED mode "simple goto" example (Copter Only)

Demonstrates how to arm and takeoff in Copter and how to navigate to points using Vehicle.simple_goto.

Full documentation is provided at http://python.dronekit.io/examples/simple_goto.html
"""

from __future__ import print_function
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil


# Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None


# Start SITL if no connection string specified
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()


# Connect to the Vehicle
print('Connecting to vehicle on: %s' % connection_string)
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

def drop_parcel():
    msg = vehicle.message_factory.command_long_encode(
        0, 0,  # target_system, target_component
        mavutil.mavlink.MAV_CMD_DO_SET_SERVO,  # command
        0,  # confirmation
        9,  # servo number
        1000,  # servo position between 1000 and 2000
        0, 0, 0, 0, 0)  # param 3 ~ 7 not used
    print("dropping parcel...")
    # send command to vehicle
    vehicle.send_mavlink(msg)
    print("parcel dropped...")

arm_and_takeoff(5)

print("Set default/target airspeed to 50")
vehicle.airspeed = 50

print("Going towards first point for 30 seconds ...")
point1 = LocationGlobalRelative(28.3677924,77.3163593, 50)
vehicle.simple_goto(point1,groundspeed=50)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards second point for 30 seconds (groundspeed set to 50 m/s) ...")
point2 = LocationGlobalRelative(28.3681594,77.3162198, 50)
vehicle.simple_goto(point2, groundspeed=50)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards third point for 30 seconds (groundspeed set to 50 m/s) ...")
point3 = LocationGlobalRelative(28.3681700,77.3163794 , 50)
vehicle.simple_goto(point3, groundspeed=50)

# sleep so we can see the change in map
time.sleep(30)

print("Going towards fourth point for 30 seconds (groundspeed set to 50m/s) ...")
point4 = LocationGlobalRelative(28.3681629,77.3166396, 50)
vehicle.simple_goto(point4, groundspeed=50)

# sleep so we can see the change in map
time.sleep(30)
print("dropping parcel")
drop_parcel()

print("Returning to Launch")
vehicle.mode = VehicleMode("RTL")
time.sleep(100)
