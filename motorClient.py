import RPi.GPIO as GPIO
from time import sleep
import socket
import random
from threading import Thread

def startMotor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    Motor1 = {'EN': 25, 'input1': 24, 'input2': 23}
    Motor2 = {'EN': 17, 'input1': 27, 'input2': 22}

    for x in Motor1:
        GPIO.setup(Motor1[x], GPIO.OUT)
        GPIO.setup(Motor2[x], GPIO.OUT)

    EN1 = GPIO.PWM(Motor1['EN'], 100)    
    EN2 = GPIO.PWM(Motor2['EN'], 100)    

    EN1.start(0)                    
    EN2.start(0)                    

    while True:
        for x in range(40, 100):
            print ("FORWARD MOTION")
            EN1.ChangeDutyCycle(x)
            EN2.ChangeDutyCycle(x)

            GPIO.output(Motor1['input1'], GPIO.HIGH)
            GPIO.output(Motor1['input2'], GPIO.LOW)
            
            GPIO.output(Motor2['input1'], GPIO.HIGH)
            GPIO.output(Motor2['input2'], GPIO.LOW)

            sleep(0.1)
    
        print ("STOP")
        EN1.ChangeDutyCycle(0)
        EN2.ChangeDutyCycle(0)

        sleep(5)
        
        for x in range(40, 100):
            print ("BACKWARD MOTION")
            EN1.ChangeDutyCycle(x)
            EN2.ChangeDutyCycle(x)
            
            GPIO.output(Motor1['input1'], GPIO.LOW)
            GPIO.output(Motor1['input2'], GPIO.HIGH)

            GPIO.output(Motor2['input1'], GPIO.LOW)
            GPIO.output(Motor2['input2'], GPIO.HIGH)

            sleep(0.1)
        
        print ("STOP")
        EN1.ChangeDutyCycle(0)
        EN2.ChangeDutyCycle(0)

        sleep(5)

    GPIO.cleanup()

# init colors
init()

SERVER_HOST = "192.168.1.35"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# prompt the client for a name
name = input("Enter your name: ")
def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)
        if message == "run":
            startMotor()

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()
while True:
    # input message we want to send to the server
    to_send =  input()
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    to_send = f"{to_send}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()