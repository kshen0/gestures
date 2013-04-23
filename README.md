#CIS 192 Final Project

##Team Members
Jocelin Lee (jocelin), Gaby MorenoCesar (gmoren), Kevin Shen (kshen)

##Description
We built an app that uses the webcam to track the user's hand. It translates vertical hand movments into mousewheel scroll events to programatically scroll the window under the cursor.

##Installation and usage
Install dependencies 
Clone repo
cd to src/gestures  
run: python main.py  
Hover mouse over or focus on window you wish to scroll
Move your hand up or down to scroll up or down. The scroll direction will behave according to the computer's natural scrolling setting.

###Keyboard Commands:
* 'h': toggles hand filtering debug window
* 'o': toggles optical flow debug window  
* 'esc': quit 
Note: focus on python app for keyboard commands to work

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


##Library
* Skin Filtering and Contouring Library: http://www.youtube.com/watch?v=ycd3t6K2ofs

We extended the skin filtering and contouring library to include bounding boxes which we used for our motion analysis. Some of the debugging code was also refactored so as to incorporate it into our code. Comments were also translated to English. 

##Similar Work
https://flutterapp.com/
