# I need to add something here that actually explains what is happening if it
# obvious already lolololol

import multiprocessing
import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)

#Rename pins to their associated number rather than
GPIO.setmode(GPIO.BOARD)

#Duty cycles: 7.5=NEUTRAL, 12.5=180, 2.5=0
#for desired angle: (desired angle)/18+2 remember pemdas lol

def servo_setup(pin):
    print('Setting up servos...')
    #Set pin number to be output
    GPIO.setup(pin,GPIO.OUT)
    # Set output of pin to be 50Hz
    pwm = GPIO.PWM(pin,50)

    if pin == 7:
        servo_black(pwm)
    elif pin == 5:
        servo_blue(pwm)

def servo_black(pwm):
    print('Black servo on...')

    tBlack = threading.currentThread()
    # Start pin with duty cycle of 7.5
    pwm.start(7.5)

    try:
        while getattr(tBlack, "do_run", True):
            pwm.ChangeDutyCycle(7.5)
            time.sleep(1.5)
            pwm.ChangeDutyCycle(11.5)
            time.sleep(1.5)
            pwm.ChangeDutyCycle(2.5)
            time.sleep(1.5)
        print('Stopping black servo via do_run command')
    except KeyboardInterrupt:    #If CTRL+C is pressed, exit cleanly
        GPIO.cleanup()

def servo_blue(pwm):
    print('Blue servo on...')

    tBlue = threading.currentThread()

    pwm.start(7.5)

    try:
        while getattr(tBlue, "do_run", True):
            pwm.ChangeDutyCycle(7.5)
            time.sleep(1)
            pwm.ChangeDutyCycle(11.5)
            time.sleep(1)
            pwm.ChangeDutyCycle(3)
            time.sleep(1)
        print('Stopping blue servo via do_run command')
    except KeyboardInterrupt:
        GPIO.cleanup()

# Threads...(target fnction to execute, name of thread, args for target function)
tBlack = threading.Thread(target = servo_setup, name = 'threadBlack', args = [7])
tBlue = threading.Thread(target = servo_setup, name = 'threadBlue', args = [5])

print('starting up threads...')

tBlack.start()
tBlue.start()
time.sleep(10)
tBlack.do_run = False
tBlue.do_run = False
tBlack.join()
tBlue.join()


