#!/bin/sh
# Camera Initialization Script
# Sets the capture target to the SD card
# Written by: Formerlurker@pm.me

# Put the arguments sent by Octolapse into variables for easy use
CAMERA_NAME=$1
# Set camera to save images to flash memory
# IMPORTANT:  The capturetarget setting may vary.  Run 'gphoto2 --auto-detect --get-config capturetarget' to determine the appropriate setting
gphoto2 --auto-detect --set-config capturetarget=1
