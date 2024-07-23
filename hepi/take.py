import gpiozero  # We are using GPIO pins
 
button = gpiozero.Button(26) # GPIO17 connects to button 
 
while True:
  if button.is_pressed:
	#print (os.popen("ls -l").read())
    	print ("raspistill -o ~/Pictures/new_image.jpg -w 1280 -h 720 -vf -t 2000")
    #subprocess.call(["raspistill -o ~/new_image.jpg -w 1280 -h 720 -vf -t 2000"])
    #print("sukses")
  else:
    print("")
