# import os
# import time

#apt package from thor labs for python
import thorlabs_apt as apt
import ctypes 
HWTYPE_LTS300 = 42	# LTS300/LTS150 Long Travel Integrated Driver/Stages

STAGE_UNITS_MM = 1		# Stage units are in mm.
HOME_FWD = 1
"""Home in the forward direction"""
HOME_REV = 2
"""Home in the reverse direction"""

#motor configs gives device info in tuples
motor_configs = apt.list_available_devices()

#we grab the serial number from the first tuple
motor = apt.Motor(motor_configs[0][1])
print(motor.velocity_upper_limit)
motor.move_home_direction
#motor.move_home() #HOMES MOTOR
# motor.move_home(False)
# from clr_loader import get_coreclr
print("Backlash distance: " + str(motor.backlash_distance))
#motor.move_by(0)
print(motor.position)
motor.move_to(150)
print(motor.position)

print("Motor position: " + str(motor.position))