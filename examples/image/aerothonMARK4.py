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
from functions import geta,getb,getc
import numpy as np     
import argparse
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
# FOR PRECISION HOVERING
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
         if b>110:
            break;
         else:     
          vehicle.send_mavlink(msg)
          time.sleep(1)
def send_body_ned_velocity2(velocity_x, velocity_y, velocity_z, duration=0):
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
         print(vehicle._location.global_relative_frame.alt)
         if vehicle.location.global_relative_frame.alt<22:
            break;
         else:     
          vehicle.send_mavlink(msg)
          time.sleep(1)     
def send_body_ned_velocity3(velocity_x, velocity_y, velocity_z, duration=0):
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
         if c==1:
            print("detection")
            break;
         else:     
          vehicle.send_mavlink(msg)
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
def cur_loc():
        f=vehicle.location.global_relative_frame.lat
        r=vehicle.location.global_relative_frame.lon
        return (f,r)
def dis(a,b):
    d=math.sqrt((a-120)*(a-120)+(b-120)*(b-120))
    return d        
#FOR PRECISION HOVERING AND PAYLOAD DROP
# FLIGHT COMMANDS
arm_and_takeoff(30)
#################################################################################################
#################################################################################################
point1 = LocationGlobalRelative(28.3677924,77.3163593, 30)
point2 = LocationGlobalRelative(28.3678502,77.3164827, 30)
point3 = LocationGlobalRelative(28.3692556,77.3159194, 30)



#################################################################################################
#################################################################################################
vehicle.simple_goto(point1,groundspeed=5)
print("going to first waypoint")
pointa=(28.3677924,77.3163593)
pointb=cur_loc()
while (GD(pointa,pointb))*1000>1:
    c=getc()
    if c==0:
        pointb=cur_loc()
        continue
    else:
        d=vehicle.location.global_relative_frame.lat
        e=vehicle.location.global_relative_frame.lon
        print("detection")
        print("hold attitude")
        current=LocationGlobalRelative(d,e,30)
        vehicle.simple_goto(current,groundspeed=1)
        time.sleep(15)
        print("aligning")
        condition_yaw(180,True)
        time.sleep(15)
        b=getb()
        a=geta()
        d=dis(a,b)
        if a<120 and b<120:
               theta=math.degrees(math.asin((120-a)/d))
        elif a>120 and b<120:
               theta=360-math.degrees(math.asin((a-120)/d))
        elif a<120 and b>120:
               theta=90+math.degrees(math.asin((b-120)/d))
        elif a>120 and b>120:
               theta=180+math.degrees(math.asin((a-120)/d))              
        condition_yaw(theta,True)  
        print("docking") 
        time.sleep(10)
        c=getc()
        if(c==1):
          send_body_ned_velocity1(0.5,0,0,15)
          time.sleep(10)
          send_body_ned_velocity2(0,0,0.5,100)
          time.sleep(10)
          drop_parcel()
          time.sleep(10)
          print("returning to launch site")
          vehicle.mode=VehicleMode("RTL")
          exit()
        else:
            print("encountered corner detection problem")
            print("moving forward")
            send_body_ned_velocity3(0.2,0,0,100)
            time.sleep(4)
            send_body_ned_velocity1(0.5,0,0,100)
            time.sleep(10)
            send_body_ned_velocity2(0,0,0.5,100)
            time.sleep(10)
            drop_parcel()
            time.sleep(10)
            print("returning to launch site")
            vehicle.mode=VehicleMode("RTL")
            exit()
#########################################################################################################
#########################################################################################################            
print("going to second waypoint")        
vehicle.simple_goto(point2,groundspeed=50)
pointa=(28.3678502,77.3164827)
pointb=cur_loc()
while (GD(pointa,pointb))*1000>1:
    c=getc()
    if c==0:
        pointb=cur_loc()
        continue
    else:
        d=vehicle.location.global_relative_frame.lat
        e=vehicle.location.global_relative_frame.lon
        print("detection")
        print("hold attitude")
        current=LocationGlobalRelative(d,e,5)
        vehicle.simple_goto(current,groundspeed=1)
        time.sleep(15)
        condition_yaw(180,True)
        time.sleep(15)
        a=geta()
        b=getb()
        d=dis(a,b)
        if a<120 and b<120:
               theta=math.degrees(math.asin((120-a)/d))
        elif a>120 and b<120:
               theta=360-math.degrees(math.asin((a-120)/d))
        elif a<120 and b>120:
               theta=90+math.degrees(math.asin((b-120)/d))
        elif a>120 and b>120:
               theta=180+math.degrees(math.asin((a-120)/d))           
        condition_yaw(theta,True)  
        print("docking") 
        time.sleep(10)
        c=getc()
        if(c==1):
          send_body_ned_velocity1(0.5,0,0,100)
          time.sleep(10)
          send_body_ned_velocity2(0,0,0.5,100)
          time.sleep(10)
          drop_parcel()
          time.sleep(10)
          print("returning to launch site")
          vehicle.mode=VehicleMode("RTL")
          exit()
        else:
            print("encountered corner detection problem")
            print("moving forward")
            send_body_ned_velocity3(0.2,0,0,100)
            time.sleep(4)
            send_body_ned_velocity1(0.5,0,0,100)
            time.sleep(10)
            send_body_ned_velocity2(0,0,0.5,100)
            time.sleep(10)
            drop_parcel()
            time.sleep(10)
            print("returning to launch site")
            vehicle.mode=VehicleMode("RTL")
            exit()
############################################################################################################
############################################################################################################
print("going to third waypoint")        
vehicle.simple_goto(point3,groundspeed=50)
pointa=(28.3692556,77.3159194)
pointb=cur_loc()
while (GD(pointa,pointb))*1000>1:
    c=getc()
    if c==0:
        pointb=cur_loc()
        continue
    else:
        d=vehicle.location.global_relative_frame.lat
        e=vehicle.location.global_relative_frame.lon
        print("detection")
        print("hold attitude")
        current=LocationGlobalRelative(d,e,5)
        vehicle.simple_goto(current,groundspeed=1)
        time.sleep(15)
        condition_yaw(180,True)
        time.sleep(15)
        a=geta()
        b=getb()
        d=dis(a,b)
        if a<120 and b<120:
               theta=math.degrees(math.asin((120-a)/d))
        elif a>120 and b<120:
               theta=360-math.degrees(math.asin((a-120)/d))
        elif a<120 and b>120:
               theta=90+math.degrees(math.asin((b-120)/d))
        elif a>120 and b>120:
               theta=180+math.degrees(math.asin((a-120)/d))            
        condition_yaw(theta,True)  
        print("docking") 
        time.sleep(10)
        c=getc()
        if(c==1):
          send_body_ned_velocity1(0.5,0,0,100)
          time.sleep(10)
          send_body_ned_velocity2(0,0,0.5,100)
          time.sleep(10)
          drop_parcel()
          time.sleep(10)
          print("returning to launch site")
          vehicle.mode=VehicleMode("RTL")
          exit()
        else:
            print("encountered corner detection problem")
            print("moving forward")
            send_body_ned_velocity3(0.2,0,0,100)
            time.sleep(4)
            send_body_ned_velocity1(0.5,0,0,100)
            time.sleep(10)
            send_body_ned_velocity2(0,0,0.5,100)
            time.sleep(10)
            drop_parcel()
            time.sleep(10)
            print("returning to launch site")
            vehicle.mode=VehicleMode("RTL")
            exit()
########################################################################################################
########################################################################################################            
time.sleep(5)
print("returning to launch site")
print("MISSION COMPLETED")
vehicle.mode=VehicleMode("RTL")
exit()        
