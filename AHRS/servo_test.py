import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36,GPIO.OUT)
GPIO.setup(38,GPIO.OUT) #This is PIN no. 29
GPIO.output(36,1)
GPIO.output(38,1)
#GPIO
en = GPIO.PWM(36, 500)
p = GPIO.PWM(38,500) #Here we use the PWM function with frequency 50
#p2 = GPIO.PWM(10,150)
en.start(100)
p.start(100)

#p2.start(7.5)
try:
    while 1:
        #p.ChangeDutyCycle(1)
        #time.sleep(.1)
        #p.ChangeDutyCycle(12.5)
        #time.sleep(10)
        #p.ChangeDutyCycle(2.5)
        time.sleep(.1)
        #p.ChangeDutyCycle(50)
except KeyboardInterrupt:
    GPIO.cleanup()
