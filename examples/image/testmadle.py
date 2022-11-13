#!/usr/bin/env python
# -*- coding: utf-8 -*-
# PRECISION NAVIGATION AND PAYLOAD DROP
# AEROKLE AEROTHON 2022
from __future__ import print_function
from email.mime import image
from geopy.distance import geodesic as GD
import time
from turtle import goto
from dronekit import connect, VehicleMode, LocationGlobalRelative,LocationGlobal,Command
from pymavlink import mavutil
import math
import numpy as np     
import argparse
from functions import geta,getb,getc
parser = argparse.ArgumentParser(description='Commands vehicle using vehicle.simple_goto.')
parser.add_argument('--connect',
                    help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()
connection_string = args.connect
sitl = None
if not connection_string:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
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
def condition_yaw(heading,is_relative=True):
    msg = vehicle.message_factory.command_long_encode(
            0,0,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW,
            0,
            heading,
            0,
            -1,
            is_relative,
            0,0,0)
    vehicle.send_mavlink(msg)
def send_body_ned_velocity1(velocity_x, velocity_y, velocity_z, duration=0):
    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,       # time_boot_ms (not used)
        0, 0,    # target system, target component
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame Needs to be MAV_FRAME_BODY_NED for forward/back left/right control.
        0b0000111111000111, # type_mask
        0, 0, 0, # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # m/s
        0, 0, 0, # x, y, z acceleration
        0, 0)
    for x in range(0,duration):
         b=getb()
         if b>230:
            break
         else:     
          vehicle.send_mavlink(msg)
          time.sleep(1)    
def mission():
    arm_and_takeoff(4)
    time.sleep(4)
    while 1:
     c=getc()
     if c==1:
        print("detected")
        print("yawing")
        a=geta()
        b=getb()
        d=math.sqrt((a-320)*(a-320)+(b-240)*(b-240)) 
        if a<320 and b<240:
               theta=math.degrees(math.asin((320-a)/d))
        elif a>320 and b<240:
               theta=360-math.degrees(math.asin((a-320)/d))
        elif a<320 and b>240:
               theta=90+math.degrees(math.asin((b-240)/d))
        elif a>320 and b>240:
               theta=180+math.degrees(math.asin((a-320)/d))
        condition_yaw(theta,True)    
        time.sleep(2)
        send_body_ned_velocity1(0.5,0,0,1500)
        print("reached destination")
mission()
