import RPi.GPIO as GPIO
import time

motorPin = 11     # define the relayPin
debounceTime = 150

def setup():    
    GPIO.setmode(GPIO.BOARD)       
    GPIO.setup(motorPin, GPIO.OUT)   # set relayPin to OUTPUT mode

def runMotor():
    GPIO.output(motorPin, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(motorPin, GPIO.LOW)
    time.sleep(5)
def destroy():
    GPIO.cleanup()                      

if __name__ == '__main__':     # Program entrance
    print ('Program is starting...')
    setup()
    try:
        runMotor()
        runMotor()
    except KeyboardInterrupt:   # Press ctrl-c to end the program.
        destroy()
