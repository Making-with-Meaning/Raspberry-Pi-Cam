#!/usr/bin/python
#The line above needs to be there and teslls the computer that its a python script
#These are the libaries that we are going to be using
from picamera import PiCamera  #this is to allow us to access the camera
import sys #This allows us to save
import os #allows the us to access the time strucutre
import time #This allows us the time we going to be using
import RPi.GPIO as GPIO

#This configures the GPIO Ports that we use on the raspberry pi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #We don't want any warnings - if there is a problem we ingore it - we need this to stop the program from crashing
#if there is a bad connection somewhere
GPIO.cleanup() #This resets the ports for us - if another program is using it we can now use it and it turns all LED off


#This is the input and output switches that we are using - diagram is shown in booklet 
SWITCH  = 18 
IS_RUNNING = 27
NOT_PAUSED = 17
TAKING_IMAGE_LED = 24

#configures switch 
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP) #This is the Switch that we are using
GPIO.setup(IS_RUNNING,GPIO.OUT) #This is the lught to show that we are running
GPIO.setup(NOT_PAUSED,GPIO.OUT) #This is the switch to show that Recording
GPIO.setup(TAKING_IMAGE_LED,GPIO.OUT) #This is switch that tells us that we are about to take a picture

timeBetweenShotsInSeconds = 10 #this is to be in seconds - this is how long we need to wait before taking the shot 

#WE are going to save the images into this directory
dirname = "images"
#here we check to see if the directory exists
if not os.path.exists(dirname):
    os.makedirs(dirname)
    #if doesnt we create one

GPIO.output(IS_RUNNING,True) # we turn on the is running light - this tells us that this software is now working
#The above code will take less than a second to run

#We print onto the screen to say that the raspberry pi is working - It also makes it clear that the computer is doing soemthing 
print "Making with Meaning Raspberry Pi Timelapse Camera"
print "Please refer to  the handout for helpfor help" 
print "Program is started and working - press ctrl-c to end (kepboard interupt"

#Initialises the camera
camera = PiCamera()
camera.resolution = (1920, 1080)
print "Capturing at 1920 by 1080"


#using a try loop until we hit a problem or told to close
try: 
    files = os.listdir(dirname)
    highestnumber = 0

    #here we keep looking for the file with the highest number
    while True:
        try: 
            #lets see if the file exists
            if os.path.exists("/home/pi/piCam/images/"+ str(highestnumber) + ".jpg" ):
                print "file does exist - lets not overwrite"
                highestnumber = highestnumber + 1
            else:
                print "file does not exist - here we go"
                break #stop looping we found the file we want
        except:
            print "file does not exist - here we go"
            break
      

    photoNumber = highestnumber
    #here we are using an infinate loop to keep our program running forever 
    while True: 
        #turns on the not-paused LED
        GPIO.output(NOT_PAUSED,True)
        #States that we are working
    
        #caputre image... thats it to actaully capture an image and to save it
        camera.capture("/home/pi/piCam/images/"  + str(photoNumber) + ".jpg") 
        #Prints to the command line prompt that we caputred the image
        print "Imaged captured"

        photoNumber = photoNumber + 1
    
    #this loop is designed to allow for a pause button to work 
    #Currently we have stopped using a button *BUT* it might come useful later on 
        #wait loop - we check every .1 of a second whether an image was taken or not.
        #We sample the switch every .1 of a second - this is the minum we can do with 
        #raspberry pi due to OS interupts
        loopAmount = int(timeBetweenShotsInSeconds * 10) 
        #Here we once a second (loopAmount is just how much we got to wait for) - we use range so we have a number 
        for i in range(loopAmount): 
            #Checks to see whether the switch is pressed or not
            #if pressed we will enter the loop (False states that the switch is pressed)
            if  GPIO.input(SWITCH) == False:
                        # Here we know the button has been pressed the first time
                        # Turns off the PAUSED LED as we pasued 
                        GPIO.output(NOT_PAUSED,False)
                        
                        #We now wait until the button released
                        while  GPIO.input(SWITCH) == False:
                            #stating that we are waiting - we need a instruction here for python hence print below
                            print"Paused Pressed - waiting for the button to be relased" 
                        while  GPIO.input(SWITCH) == True:
                            #here the button has been released and were waiting for it to be printed again
                            print"Paused - button has been released"
                        while  GPIO.input(SWITCH) == False:
                            #button has been pressed for a second time.... waiting for release
                            print "Unpausing - waiting for the button to be released "
                        #released
                        print "Released - contiuning as normal"
            
            #were out the loop here - contune as normal and turn light on
            GPIO.output(NOT_PAUSED,True)

            #Here we opperate the waiting time
            warningTime = 8 #This is the amount of warning we want in seconds 

            #here we calculate it in miliseconds and finds the differnece between the two readings
            takingPhoto = (timeBetweenShotsInSeconds*10)-(warningTime*10)
            #here we turn it on if we are going to take a photo or turn it off if were not 
            if (i >= int(takingPhoto)):
                GPIO.output(TAKING_IMAGE_LED,True)
            else :
                GPIO.output(TAKING_IMAGE_LED,False)
                time.sleep(0.1)
except KeyboardInterrupt:
    print("KeyboardInterrupt - turnining off lights ")
    #here we turn off the lights and release the lights
    GPIO.cleanup()

#here we have some code that tidies up our program if something else causes us to crash
except Exception, err:
    print Exception, err
    #here we give the user some help
    print("Unknown ERROR - check for SEGFault - if you do have one we ran out of ram")
    print("Otherwise is the memory card full?")
    print("Or are you running another program? - look at the stack")
    #here we turn off the lights and relase them - this tells the user that something has gone wrong
    GPIO.cleanup()
