import RPi.GPIO as io
io.setmode(io.BOARD)

en1_pin = 22
in1_pin = 16
in2_pin = 18

io.setup(en1_pin, io.OUT)
io.setup(in1_pin, io.OUT)
io.setup(in2_pin, io.OUT)


io.output(en1_pin, io.HIGH)
p1 = io.PWM(in1_pin, 500)
p2 = io.PWM(in2_pin, 500)

def set(property, value):
    if property == "delayed":
        pass
    elif property == "mode":
        pass
    elif property == "frequency":
        p1.ChangeFrequency(int(value))
        p2.ChangeFrequency(int(value))
    elif property == "active":
        p1.start(0)
        p2.stop()
        pass
    elif property == "duty":
        p1.ChangeDutyCycle(int(value))
        p2.ChangeDutyCycle(int(value))
        print("Duty Cycle is now at {0}".format(value))
    

#set("delayed", "0")
#set("mode", "pwm")
#set("frequency", "50")
set("active", "1")


def clockwise():
    p1.start(0)
    p2.stop()
    io.output(in1_pin, io.HIGH)    
    io.output(in2_pin, io.LOW)
 
def counter_clockwise():
    p2.start(0)
    p1.stop()
    io.output(in1_pin, io.LOW)
    io.output(in2_pin, io.HIGH)
 
#clockwise()
try:
    while True:
        cmd = input("Command, f/r 0..9, E.g. f5 :")
        direction = cmd[0]
        if direction == "f":
            clockwise()
        else: 
            counter_clockwise()
        speed = int(cmd[1:])
        set("duty", str(speed))
except KeyboardInterrupt:
    io.output(en1_pin, io.LOW)
    p1.stop()
    p2.stop()
    io.cleanup()
