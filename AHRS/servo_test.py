import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(3,GPIO.OUT) #This is PIN no. 29
p = GPIO.PWM(3,150) #Here we use the PWM function with frequency 50
p.start(7.5)
try:
    while 1:
        #p.ChangeDutyCycle(1)
        #time.sleep(.1)
        #p.ChangeDutyCycle(12.5)
        #time.sleep(10)
        #p.ChangeDutyCycle(2.5)
        time.sleep(.1)
        p.ChangeDutyCycle(100)
except KeyboardInterrupt:
    GPIO.cleanup()
