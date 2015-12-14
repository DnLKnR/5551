import RPi.GPIO as io
io.setmode(io.BOARD)

en_pins = [24,26]
in_pins = [16,18,20,22]


for pin in en_pins + in_pins:
    io.setup(pin, io.OUT)

for enable_pin in 
io.output(en1_pin, io.HIGH)
pwms = []
for pin in in_pins:
    pwms.append(io.PWM(pin, 500))

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
rotation = 1

def clockwise():
    rotation = 1
    #p1.start(0)
    #p2.stop()
    #io.output(in1_pin, io.HIGH)    
    #io.output(in2_pin, io.LOW)
 
def counter_clockwise():
    rotation = -1
    #p2.start(0)
    #p1.stop()
    #io.output(in1_pin, io.LOW)
    #io.output(in2_pin, io.HIGH)
 
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
