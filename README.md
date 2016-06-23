
This is the README for bb23. A ping pong collection robot. 




How to setup daemons

python gpiodaemon.py start

python test_comms.py

Notes from 6/22/16:
* On startup we'll run two daemons, the driver daemon and camera daemon
* We'll also run the cortex program, which is the control loop
* The cortex is based on test_comms.py and will make TCP requests to the driver and camera
* The driver and camera daemon will be two daemons based on gpiodaemon and gpiomanager, but stripped down and reorganized

To do for next time:
* Create cortex.py, which will involve copying the basic loop of drive.py
* Reorganize the code for the driver and gpiomanager so it works properly
* Copy that logic for cameramanager
* Put the code from drive.py and bbcamera into cameramanager

Questions:
* Do we need two separate daemons running? Will we be stuck waiting on the camera daemon?
* Or can we have one daemon running with two 'manager' classes, one for the driver and one for the camera

