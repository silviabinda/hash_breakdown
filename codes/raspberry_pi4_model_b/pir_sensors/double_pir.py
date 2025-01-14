from gpiozero import MotionSensor
import time 
from time import sleep
import subprocess

pir = MotionSensor(21)
pir2 = MotionSensor(4)

def wait_for_any_motion():
	while not (pir.motion_detected or pir2.motion_detected):
		sleep(0.01)
		pass
	print(pir.motion_detected, pir2.motion_detected)
	return
	
while True:
	try:
		wait_for_any_motion()
		print(time.time(), "Motion detected")
		subprocess.run(['amixer', 'set', 'Master', '100%'])
		continue_loud = True
		while continue_loud:
			try:
				sleep(5) # adjust to set time how long it defaultly continues loud after detecting movement 
			except InterruptedError as e:
				print(f"InterruptedError occurred: {e}")
			continue_loud = False
			if pir.motion_detected or pir2.motion_detected:
				continue_loud = True
		subprocess.run(['amixer', 'set', 'Master', '50%'])
	except KeyboardInterrupt:
		print ("\nProcess was interrupted by user. Ending ...")
		#logger.info('Process interrupted by user')
		break 
	
	except BaseException as e:
		print(e)
		continue

