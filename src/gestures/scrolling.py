import sys
import os
import time

from Quartz.CoreGraphics import (CGEventCreateMouseEvent,
									CGEventCreateKeyboardEvent,
									CGEventCreateScrollWheelEvent,
									CGEventPost,
									kCGEventMouseMoved,
									kCGEventLeftMouseDown,
									kCGEventLeftMouseDown,
									kCGEventLeftMouseUp,
									kCGMouseButtonLeft,
									kCGHIDEventTap)

DELAY = .005
BASE_SPEED = 4

def scroll_wheel_up(num_times):
	for i in xrange(1, num_times):
		time.sleep(DELAY)
		multiplier = 1 - (float(i) / num_times)
		velocity = BASE_SPEED * multiplier
		event = CGEventCreateScrollWheelEvent(None, 0, 1, velocity)
		CGEventPost(kCGHIDEventTap, event)

def scroll_wheel_down(num_times):
	for i in xrange(1, num_times):
		time.sleep(DELAY)
		multiplier = 1 - (float(i) / num_times)
		velocity = -BASE_SPEED * multiplier
		event = CGEventCreateScrollWheelEvent(None, 0, 1, velocity)
		CGEventPost(kCGHIDEventTap, event)

def fire_key(keycode):
	# Key bindings from: 
	#http://stackoverflow.com/questions/1918841/how-to-convert-ascii-character-to-cgkeycode
    e = CGEventCreateKeyboardEvent(None, keycode, True)
    CGEventPost(kCGHIDEventTap, e)
    e = CGEventCreateKeyboardEvent(None, keycode, False)
    CGEventPost(kCGHIDEventTap, e)

def main():
	while True:
		scroll_wheel_up(75)
		time.sleep(.7)

if __name__ == '__main__':
	main()