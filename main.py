from picamera import PiCamera
import sys
import os
import time
#Default configs#
#lenghtOfShots = 20
#This is the port that we are going to be using for the pause switch 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
#This is the input and output switches that we are using
SWITCH  = 18 
IS_RUNNING = 27
NOT_PAUSED = 17
TAKING_IMAGE_LED = 24

#configures switch 
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(IS_RUNNING,GPIO.OUT)
GPIO.setup(NOT_PAUSED,GPIO.OUT)
GPIO.setup(TAKING_IMAGE_LED,GPIO.OUT)

timeBetweenShotsInSeconds = 30 #this is to be in seconds 
GPIO.output(IS_RUNNING,True)

#makes a directory if it doesnt exist
dirname = "/home/pi/Desk"
if not os.path.exists(dirname):
    os.makedirs(dirname)

print "Swansea University Raspberry Pi Timelapse Camera"
print "Please refer to PiTimelapse.pdf for help" 
print "Started - press ctrl-c to end"
#Initialises the camera
camera = PiCamera()

#using a try loop until we hit a problem or told to close
try: 
    #here we are using an infinate loop to keep our program running forever 
    while True: 
        #turns on the not-paused LED
        GPIO.output(NOT_PAUSED,True)

        #States that we are working#
        #format of the image output
        timestr = time.strftime("%H:%M:%S %d.%m.%Y")
        #caputre image
        camera.capture("images/" + timestr + ".jpg")
        #Prints to the command line prompt that we caputred the image
        print "Imaged captured"
    
        #wait loop - we check every .1 of a second whether an image was taken or not.
        #We sample the switch every .1 of a second - this is the minum we can do with 
        #raspberry pi due to OS interupts
        loopAmount = int(timeBetweenShotsInSeconds * 10)
        #Here we once a second (loopAmount is just how much we got to wait for)
        for i in range(loopAmount): 
            #Checks to see whether the switch is pressed or not
            #if pressed we will enter the loop (False states that the switch is pressed)
            if  GPIO.input(SWITCH) == False:
                        #Turns off the PAUSED LED as we pasued 
                        GPIO.output(NOT_PAUSED,False)
                        
                        #We now wait until the button released
                        while  GPIO.input(SWITCH) == False:
                            #stating that we are waiting - we need a command here for python 
                            print"Paused Pressed - waiting for the button to be relased" 
                        while  GPIO.input(SWITCH) == True:
                            print"Paused"
                        while  GPIO.input(SWITCH) == False:
                            print "Unpausing - waiting for the button to be released "
                        print "Released - contiuning as normal"
            GPIO.output(NOT_PAUSED,True)

            #This does the flash
            warningTime = 3 #seconds
            takingPhoto = (timeBetweenShotsInSeconds*10)-(warningTime*10)
            if (i >= int(takingPhoto)):
                GPIO.output(TAKING_IMAGE_LED,True)
            else :
                GPIO.output(TAKING_IMAGE_LED,False)

            time.sleep(0.1)

#Turns off LEDs and releases swich
except KeyboardInterrupt:
    GPIO.cleanup()