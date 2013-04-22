import sys
import os
import time
import math

from Quartz.CoreGraphics import (CGEventCreateScrollWheelEvent,
									CGEventPost,
									kCGHIDEventTap)

DELAY = .002

def scroll_wheel(v0, sign, steps=200):
	"""
	Kinematically scrolls the window under the cursor.
	args: v0, the initial velocity of the scroll
		  sign, the direction of scrolling (1 for up, -1 for down)
		  steps, optional arg that determines duration of the scroll
	"""

	r, r0 = 0, 0
	v = v0
	V_CAP = v0 + 4
	v_history = []
	accelerating = True
	a = 0.15
	decel_const = -0.02

	t = 0
	while v > 0:
		# added delay for buttery smoothness
		time.sleep(DELAY)

		# update position
		new_r = r0 + ((v + v0)/2) * t
		scroll_dist = sign * (new_r - r) 
		r = new_r

		# update velocity
		v = min(V_CAP, a * t + v0)
		if v == V_CAP:
			v0 = v

		# keep track of previous N=4 velocities
		if len(v_history) == 4:
			v_history.pop(0)
		v_history.append(v)

		# send the mouse event
		event = CGEventCreateScrollWheelEvent(None, 0, 1, scroll_dist)
		CGEventPost(kCGHIDEventTap, event)

		# decelerate if near the end of the time loop
		if accelerating and t > 0.9 * steps:
			accelerating = False
			a = decel_const 
			v0 = int(sum(v_history) / len(v_history))
			r0 = r
			t = 0

		t += 1
