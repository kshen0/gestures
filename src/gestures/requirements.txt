CIS 192 Final Project

##Features
* Skin filtering used for hand detection
* Bounding boxes used to determine direction and speed of motion
* Smooth scrolling with speed proportional to speed of hand movement


##Dependencies
* OpenCV and OpenCV2: http://opencv.willowgarage.com/wiki/InstallGuide
* numpy (dependency of opencv)
* pyobjc: http://pythonhosted.org/pyobjc/
* pyobjc Quartz framework: https://pypi.python.org/pypi/pyobjc-framework-Quartz

* OpenCV and OpenCV2 were used to capture webcam frames and process the images.
* numpy, a dependency of opencv, was used for determining vector fields and directinon of movement
* PyObjC and its Quartz framework were used for handling mouse events


##Library
* Skin Filtering and Contouring Library: http://www.youtube.com/watch?v=ycd3t6K2ofs

We extended the skin filtering and contouring library to include bounding boxes which we used for our motion analysis. Some of the debugging code was also refactored so as to incorporate it into our code. Comments were also translated to English. 


##Installation and usage
* Ensure dependencies are installed
* Clone the repo at https://github.com/kshen0/gestures and cd to src/gestures
* run main.py
* Move your hand up or down to scroll up or down. The scroll direction will behave according to the computer's natural scrolling setting. 
* The app can scroll any scrollable window under the cursor


##Keyboard Commands:
Focus the python app first
* 'h': toggles hand filtering debug window
* 'o': toggles optical flow debug window  
* 'esc': quit 


##Limitations
* Skin filter detects anything flesh-colored, including the face and skin-toned objects. This is a minor issue because the app only sends a scroll event if movement speed is above a certain threshold.


##Similar Work
https://flutterapp.com/
