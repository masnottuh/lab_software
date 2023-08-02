# import os
# import time

#apt package from thor labs for python
import thorlabs_apt as apt
import ctypes 
HWTYPE_LTS300 = 42	# LTS300/LTS150 Long Travel Integrated Driver/Stages

STAGE_UNITS_MM = 1		# Stage units are in mm.

#motor configs gives device info in tuples
motor_configs = apt.list_available_devices()

#we grab the serial number from the first tuple
motor = apt.Motor(motor_configs[0][1])

#now we can move the motor
# motor.move_home(False)
# from clr_loader import get_coreclr
print("Backlash distance: " + str(motor.backlash_distance))
motor.move_by(0.2)
print("Motor position: " + str(motor.position))