# Line Follower Robot Code for Jetbot
# Deigned by: Akshat Bisht (a.bisht@auckland.ac.nz)
# Designed for: University of Auckland
# Date 18 July 2022

import multiprocessing
# import Queue
import Jetson.GPIO as GPIO
import time
import signal

from jetbot import Robot
robot = Robot()

# Pin Definitions
# input_pin = 13  # BCM pin 18, BOARD pin 12
# input_pin_2 = 15

queue = multiprocessing.Queue()


def lfInit():
	global queue, input_pin, input_pin_2
	print(GPIO.JETSON_INFO)
	print("Initilising Line Following Jetbot")
    # Pin Setup:
# 	signal.signal(signal.SIGINT, self.exit_gracefully)
# 	signal.signal(signal.SIGTERM, self.exit_gracefully)

    
    
	p = multiprocessing.Process(target=line_follow_run, args=(queue,robot))
	p.start()
# 	q = multiprocessing.Process(target=demo_test, args=(queue,))
# 	q.start()
    
    # queue.close()
    # queue.join_thread()
    # p.join()
    # q.join()
def lfDeinit():
	global queue
	sendDic = {'stop':-1}
	queue.put(sendDic)
	print("Deinitialised")

def lfStop():
	global queue
	sendDic = {'stop':1}
	queue.put(sendDic)

def lfStart():
	global queue
	sendDic = {'stop':0}
	queue.put(sendDic)

def lfSpeed(setSpeed):
	global queue
	sendDic = {'speed':setSpeed}
	queue.put(sendDic)

def lfTurnSpeed(setSpeed):
	global queue
	sendDic = {'turnSpeed':setSpeed}
	queue.put(sendDic)


# def demo_test(q):
#     while True:
#         print("Hello")
#         time.sleep(1)
#         print(speed)
#     speed = speed - 0.01
#     q.put(speed)

def line_follow_run(q,lRobot):
	input_pin= 15
	input_pin_2 = 16
	next_move = 0
	prev_move = -10
	speed = 0.15
	turnSpeed = 0.25
	stop = 1
	oldSpeed = speed

	GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi
	GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin
	GPIO.setup(input_pin_2, GPIO.IN)

	while True:
        #speed = q.get()
		try:
			revDic = q.get(False)
			for key in revDic.keys():
				if key == "speed":
					print("speed"+str(revDic[key]))
					speed = revDic[key]
				if key == "stop":
					print("stop"+str(revDic[key]))
					stop = revDic[key]
				if key == "turnSpeed":
					print("turn speed"+str(revDic[key]))
					turnSpeed = revDic[turnSpeed]
		except:
			pass

		if stop == -1:
			lRobot.stop();
			prev_move = 100
			break
		if stop == 1:
			lRobot.stop()
			prev_move = 100            
			continue

		if oldSpeed != speed:
			oldSpeed = speed
			print(speed)
			prev_move = 100

		value = GPIO.input(input_pin)
		if value == GPIO.HIGH:
			value_str = "HIGH"
			next_move = 1
		else:
			value_str = "LOW"

		value = GPIO.input(input_pin_2)
		if value == GPIO.HIGH:
			value_str_2 = "HIGH"
			next_move = -1
		else:
			value_str_2 = "LOW"
# 		print(" {} -- {}".format(value_str,value_str_2))
# 		print(next_move)        
		if value_str == "HIGH" and value_str_2 == "HIGH":
			next_move = 2
		if prev_move != next_move:
			robot.stop()
			if next_move == -1:
				lRobot.set_motors(-0.1,turnSpeed)
			if next_move  == 1:
				lRobot.set_motors(turnSpeed,-0.1)
			if next_move == 0:
				lRobot.forward(speed)
			if next_move == 2:
				lRobot.backward(speed)
			#time.sleep(0.05)
			prev_move = next_move
            
		next_move = 0
#    finally:
	GPIO.cleanup()






