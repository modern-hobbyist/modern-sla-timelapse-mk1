from subprocess import call
import time
import RPi.GPIO as GPIO

# Pin definitions
input_pin = 4

# Suppress warnings
GPIO.setwarnings(False)

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set LED pin as output
GPIO.setup(input_pin, GPIO.IN)

rc = call("./initialize-camera-save-to-sd.sh")

triggered = False

try:
  while True:
    value = GPIO.input(input_pin)
    if not value and not triggered:
      rc = call("./trigger-snapshot.sh")
      triggered = True
    elif triggered and value:
      triggered = False

finally:
  GPIO.cleanup()
  print("Thanks for running me!")
