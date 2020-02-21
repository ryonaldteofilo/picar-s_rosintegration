#!/usr/bin/env python
from SunFounder_Line_Follower import Line_Follower
from picar import front_wheels
import time
import picar

picar.setup()

REFERENCES = [200, 200, 200, 200, 200]
turning_angle = 90
delay = 0.0005
fw = front_wheels.Front_Wheels(db='config')
lf = Line_Follower.Line_Follower()
lf.references = REFERENCES
fw.ready()
fw.turning_max = 45

def line_follower():
	global turning_angle
	a_step = 3
	b_step = 10
	c_step = 30
	d_step = 50
	while True:
		lt_status_now = lf.read_digital()
		print(lt_status_now)

		if	lt_status_now == [1,1,0,1,1]:
			step = 0
		elif lt_status_now == [1,0,0,1,1] or lt_status_now == [1,1,0,0,1]:
			step = a_step
		elif lt_status_now == [1,0,1,1,1] or lt_status_now == [1,1,1,0,1]:
			step = b_step
		elif lt_status_now == [0,0,1,1,1] or lt_status_now == [1,1,1,0,0]:
			step = c_step
		elif lt_status_now == [0,1,1,1,1] or lt_status_now == [1,1,1,1,0]:
			step = d_step

		if	lt_status_now == [1,1,0,1,1]:
			turning_angle = 90
		elif lt_status_now in ([1,0,0,1,1],[1,0,1,1,1],[0,0,1,1,1],[0,1,1,1,1]):
			turning_angle = int(90 - step)
		elif lt_status_now in ([1,1,0,0,1],[1,1,1,0,1],[1,1,1,0,0],[1,1,1,1,0]):
			turning_angle = int(90 + step)
		elif lt_status_now == [1,1,1,1,1]:
			print("Off track")

		fw.turn(turning_angle)
		time.sleep(delay)

def destroy():
	fw.turn(90)

if __name__ == '__main__':
	try:
		try:
			while True:
				line_follower()
		except Exception as e:
			print(e)
			print('error try again in 5')
			destroy()
			time.sleep(5)
	except KeyboardInterrupt:
		destroy()
