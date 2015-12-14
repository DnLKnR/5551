import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

enable_pin_1 = 25
coil_A_1_pin_1 = 12
coil_A_2_pin_1 = 16
coil_B_1_pin_1 = 5
coil_B_2_pin_1 = 6
enable_pin_2 = 4
coil_A_1_pin_2 = 23
coil_A_2_pin_2 = 24
coil_B_1_pin_2 = 17
coil_B_2_pin_2 = 27

GPIO.setup(enable_pin_1, GPIO.OUT)
GPIO.setup(coil_A_1_pin_1, GPIO.OUT)
GPIO.setup(coil_A_2_pin_1, GPIO.OUT)
GPIO.setup(coil_B_1_pin_1, GPIO.OUT)
GPIO.setup(coil_B_2_pin_1, GPIO.OUT)
GPIO.setup(enable_pin_2, GPIO.OUT)
GPIO.setup(coil_A_1_pin_2, GPIO.OUT)
GPIO.setup(coil_A_2_pin_2, GPIO.OUT)
GPIO.setup(coil_B_1_pin_2, GPIO.OUT)
GPIO.setup(coil_B_2_pin_2, GPIO.OUT)
 
GPIO.output(enable_pin_1, 1)
GPIO.output(enable_pin_2, 1)
 
def forward(delay, steps):  
    for i in range(0, steps):
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
 
def backwards(delay, steps):  
    for i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
 
  
def setStep(w1, w2, w3, w4):
    GPIO.output(coil_A_1_pin_1, w1)
    GPIO.output(coil_A_2_pin_1, w2)
    GPIO.output(coil_B_1_pin_1, w3)
    GPIO.output(coil_B_2_pin_1, w4)
    GPIO.output(coil_A_1_pin_2, w1)
    GPIO.output(coil_A_2_pin_2, w2)
    GPIO.output(coil_B_1_pin_2, w3)
    GPIO.output(coil_B_2_pin_2, w4)
try:
    while True:
        delay = input("Delay between steps (milliseconds)?")
        steps = input("How many steps forward? ")
        forward(float(delay), int(steps))
        steps = input("How many steps backwards? ")
        backwards(float(delay), int(steps))
except KeyboardInterrupt:
    GPIO.cleanup()
