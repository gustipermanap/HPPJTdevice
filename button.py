from gpiozero import Button
import time
help_button = Button(24)
while True:
	if help_button.is_pressed:
		print("Button is Pressed")
		time.sleep(1)
