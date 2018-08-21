#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /home/pi/Desktop/piCam
#making from git
echo 'Pulling from git'
git pull
#Runs a make script 
chmod +=x make.sh
sudo ./make.sh
# Starting app
sudo python main.py