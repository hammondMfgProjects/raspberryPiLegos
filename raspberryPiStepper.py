#!/usr/bin/python

#********************************************************
# 
# Raspberry Pi Robot Script 
# Igor Kolesnik
# Hammond Manufacturing
# 03/09/2016
# 
# Based on Matt Hawkins Stepper Motor Test Script
#       https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/stepper.py
# 
# Keys:
#       'D' - Move forward 
#       'S' - Move backwared
#       'A' - Turn left
#       'D' - Turn right
#       'Space' - Stop
#       'ESC' - Exit
#********************************************************

# Import required libraries
import sys
import select
import tty
import termios
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)


def moveForward(speed, nbc, direction):
    StepPinsL = [18,23,12,16]
    StepPinsR = [17,22,6,19]

    for pin in StepPinsL:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
 
    for pin in StepPinsR:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    SeqR = [[1,0,0,1],
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]]

    SeqL = SeqR
    
    StepCount = 8

    if direction == "forward":
       StepDirR = -2
       StepDirL = 2

    if direction == "reverse":
       StepDirR = 2
       StepDirL = -2

    print "Stepper Motor Speed"
    print speed
    WaitTime = speed/float(1000)

    StepCounterR = 0
    StepCounterL = 0

    while True:
        for pin in range(0, 4):
            xpin = StepPinsR[pin]
            if SeqR[StepCounterR][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
 
        for pin in range(0,4):
            xpin = StepPinsL[pin]
            if SeqL[StepCounterL][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
            
        StepCounterR += StepDirR
        StepCounterL += StepDirL
            
        # If we reach the end of the sequence
        # start again
        if (StepCounterR>=StepCount):
            StepCounterR = 0
        if (StepCounterR<0):
            StepCounterR = StepCount+StepDirR

        if (StepCounterL>=StepCount):
            StepCounterL = 0
        if (StepCounterL<0):
            StepCounterL = StepCount+StepDirL

        # Wait before moving on
        time.sleep(WaitTime)
        if nbc.get_data() == ' ':
            print "exiting out of left motor"
            return

 
def rotateLeftMotors(speed, nbc):
    StepPins = [18,23,12,16]

    for pin in StepPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    Seq = [[1,0,0,1],
           [1,0,0,0],
           [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1]]

    StepCount = 8
    StepDir = 2

    print "Stepper Motor Speed"
    print speed
    WaitTime = speed/float(1000)

    StepCounter = 0

    while True:
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
            
        StepCounter += StepDir
            
        # If we reach the end of the sequence
        # start again
        if (StepCounter>=StepCount):
            StepCounter = 0
        if (StepCounter<0):
            StepCounter = StepCount+StepDir
        # Wait before moving on
        time.sleep(WaitTime)
        if nbc.get_data() == ' ':
            print "exiting out of left motor"
            return 

def rotateRightMotors(speed, nbc):
    StepPins = [17,22,6,19]

    for pin in StepPins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)

    # Define advanced sequence
    # as shown in manufacturers datasheet
    Seq = [[1,0,0,1],
           [1,0,0,0],
           [1,1,0,0],
           [0,1,0,0],
           [0,1,1,0],
           [0,0,1,0],
           [0,0,1,1],
           [0,0,0,1]]

    StepCount = 8
    StepDir = -2

    print "Stepper Motor Speed"
    print speed
    WaitTime = speed/float(1000)

    StepCounter = 0

    while True:
        for pin in range(0, 4):
            xpin = StepPins[pin]
            if Seq[StepCounter][pin]!=0:
                GPIO.output(xpin, True)
            else:
                GPIO.output(xpin, False)
            
        StepCounter += StepDir
            
        # If we reach the end of the sequence
        # start again
        if (StepCounter>=StepCount):
            StepCounter = 0
        if (StepCounter<0):
            StepCounter = StepCount+StepDir
        # Wait before moving on
        time.sleep(WaitTime)
        if nbc.get_data() == ' ':
            print "exiting out of right motor"
            return   

class NonBlockingConsole(object):

    def __enter__(self):
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)


    def get_data(self):
        if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
            return sys.stdin.read(1)
        return False

if __name__ == '__main__':
    with NonBlockingConsole() as nbc:
        while True:
            if nbc.get_data() == 'd':
                print "d"
                rotateRightMotors(2, nbc)
            if nbc.get_data() == 'a':
                print "a"
                rotateLeftMotors(2, nbc)
            if nbc.get_data() == 'w':
                print "w"
                moveForward(2, nbc, "forward")
            if nbc.get_data() == 's':
                print "s"
                moveForward(2, nbc, "reverse")
            if nbc.get_data() == '\x1b':  # x1b is ESC
                break
       


