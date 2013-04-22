#CIS 192 Final Project

##Team Members
Jocelin Lee (jocelin), Gaby MorenoCesar (gmoren), Kevin Shen (kshen)

##Description
We built an app that uses the webcam to track the user's hand. It translates vertical hand movments into mousewheel scroll events to programatically scroll the window under the cursor.

##Use cases
Scrolling news articles without touching the trackpad while eating messy foods with your hands.

##Dependencies
* OpenCV and OpenCV2: http://opencv.willowgarage.com/wiki/InstallGuide
* numpy (dependency of opencv)
* pyobjc: http://pythonhosted.org/pyobjc/
* pyobjc Quartz framework: https://pypi.python.org/pypi/pyobjc-framework-Quartz

OpenCV and OpenCV2 were used to capture webcam frames and process the images.   
numpy, a dependency of opencv, was used for determining vector fields and directinon of movement  
PyObjC and its Quartz framework were used for handling mouse events  

##Installation and usage
Ensure dependencies are installed  
Clone the repo and cd to src/gestures  
run main.py  
Move your hand up or down to scroll up or down. The scroll direction will behave according to the computer's natural scrolling setting.
Press d to toggle debug video feed  
Press esc to quit 

##Similar Work
https://flutterapp.com/
