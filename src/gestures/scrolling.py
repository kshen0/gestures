import sys
import os
import time

from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventCreateKeyboardEvent
from Quartz.CoreGraphics import CGEventCreateScrollWheelEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGHIDEventTap

def mouseEvent(type, posx, posy):
        theEvent = CGEventCreateMouseEvent(None, type, (posx,posy), kCGMouseButtonLeft)
        CGEventPost(kCGHIDEventTap, theEvent)

def mousemove(posx,posy):
	pass

def scroll_wheel_up(num_times):
	for i in xrange(num_times):
		event = CGEventCreateScrollWheelEvent(None, 0, 1, 1)
		CGEventPost(kCGHIDEventTap, event)

def scroll_wheel_down(num_times):
	for i in xrange(num_times):
		event = CGEventCreateScrollWheelEvent(None, 0, 1, -1)
		CGEventPost(kCGHIDEventTap, event)

def fire_key(keycode):
	# Key bindings from: 
	#http://stackoverflow.com/questions/1918841/how-to-convert-ascii-character-to-cgkeycode
    e = CGEventCreateKeyboardEvent(None, keycode, True)
    CGEventPost(kCGHIDEventTap, e)
    e = CGEventCreateKeyboardEvent(None, keycode, False)
    CGEventPost(kCGHIDEventTap, e)

def mouseclick(posx,posy):
        mouseEvent(kCGEventLeftMouseDown, posx,posy)
        mouseEvent(kCGEventLeftMouseUp, posx,posy)

def main():
	while True:
		scroll_wheel_up(75)
		time.sleep(.7)

if __name__ == '__main__':
	main()