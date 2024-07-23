#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import gpiozero  # We are using GPIO pins

channel = 24
#obutton = 26
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)
button = gpiozero.Button(26) # GPIO17 connects to button 

def callback(channel):
        if GPIO.input(channel):
                print ("Helm Terjatuh!")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, callback)

while True:
  if button.is_pressed:
    	print ("tolong!")
  else:
    	print ("")

while True:
        time.sleep(1000)
