import sys
import os
import time
import math

from Quartz.CoreGraphics import (CGEventCreateScrollWheelEvent,
									CGEventPost,
									kCGHIDEventTap)

DELAY = .002
BASE_SPEED = 7

def scroll_wheel_up(num_times):
	for i in xrange(1, num_times):
		time.sleep(DELAY)
		multiplier = 1 - (float(i) / num_times)
		velocitiescity = BASE_SPEED * multiplier
		event = CGEventCreateScrollWheelEvent(None, 0, 1, velocity)
		CGEventPost(kCGHIDEventTap, event)

def scroll_wheel_down(v0):
	r0 = 	0
	r = r0
	v = v0
	a = 0.15000
	V_CAP = v0 + 4
	end = 200
	v_history = []
	accelerating = True
	decel_const = -0.02

	t = 0
	i = 0
	while v > 0:
		# added delay for buttery smoothness
		time.sleep(DELAY)

		# update position
		new_r = r0 + ((v + v0)/2) * t
		scroll_dist = r - new_r

		# update velocity
		"""
		vsquared = max(0, v0*v0 + 2*a*(r-r0))
		v = min(V_CAP, math.sqrt(vsquared))
		"""
		v = min(V_CAP, a * t + v0)
		if v == V_CAP:
			v0 = v

		# keep track of previous N=4 velocities
		if len(v_history) == 4:
			v_history.pop(0)
		v_history.append(v)

		r = new_r
		print v 


		# send the mouse event
		event = CGEventCreateScrollWheelEvent(None, 0, 1, scroll_dist)
		CGEventPost(kCGHIDEventTap, event)

		# decelerate if near the end of the time loop
		if accelerating and t > 0.9 * end:
			accelerating = False
			a = decel_const 
			v0 = int(sum(v_history) / len(v_history))
			r0 = r
			t = 0

		t += 1
		i += 1
	"""
	for i in xrange(1, num_times):
		time.sleep(DELAY)
		m = 1 - (float(i) / num_times)
		#velocity = -BASE_SPEED * m
		velocity = -1 * (3*m*m + 2*m + 1)
		print velocity
		event = CGEventCreateScrollWheelEvent(None, 0, 1, velocity)
		CGEventPost(kCGHIDEventTap, event)
	"""

def fire_key(keycode):
	# Key bindings from: 
	#http://stackoverflow.com/questions/1918841/how-to-convert-ascii-character-to-cgkeycode
    e = CGEventCreateKeyboardEvent(None, keycode, True)
    CGEventPost(kCGHIDEventTap, e)
    e = CGEventCreateKeyboardEvent(None, keycode, False)
    CGEventPost(kCGHIDEventTap, e)

def main():
	for i in xrange(1, 5):
		time.sleep(2)
		scroll_wheel_down(i)

if __name__ == '__main__':
	main()
