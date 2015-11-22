import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)


class ServoMotor:
    def __init__(self, pin, freq):
        GPIO.setup(pin, GPIO.OUT)
        self.p = GPIO.PWM(pin, freq)
        
    def move(self, distance, speed):
        ## Move the motor a certain distance
        #self.p.start(x)
        #time.sleep(rotation_time)
        #self.p.stop()
        pass

    def set_pin(self, pin):
        

class MalletManipulator:
    def __init__(self, x_motor, y_motor):
        ## X and Y motor are of class type ServoMotor
        self.x_motor = x_motor
        self.y_motor = y_motor
        self.calibrated = False
        
    def move(self, x, y, speed):
        if not self.calibrated:
            return
        # Compute what x and y distance are
        # based on current position.
        #self.x_motor.move(x_distance)
        #self.y_motor.move(y_distance)
        return #True or new coordinates
        
    def calibrate(self):
        pass
        
    def get_location(self):
        pass
    
    def clean_up(self):  
        GPIO.cleanup()