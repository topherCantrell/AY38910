import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class AY38910:

    def __init__(self, pins_data, pin_bc1, pin_bc2, pin_bdir):
        self.pins_data = pins_data
        self.pin_bc1 = pin_bc1
        self.pin_bc2 = pin_bc2
        self.pin_bdir = pin_bdir

        self.set_data_output()

        for p in [pin_bc1, pin_bc2, pin_bdir]:            
            GPIO.setup(p, GPIO.OUT)
            GPIO.output(p, 0)

    def set_data_input(self):
        for p in self.pins_data:
            GPIO.setup(p, GPIO.IN) 

    def set_data_output(self):
        for p in self.pins_data:
            GPIO.setup(p, GPIO.OUT)

    def write_data_pins(self, value):
        bn = 1
        for pin in self.pins_data:
            if value & bn:      
                GPIO.output(pin, 1)                  
            else: 
                GPIO.output(pin, 0)                
            bn = bn << 1

    def read_data_pins(self):
        bn = 1
        ret = 0
        for pin in self.pins_data:
            if GPIO.input(pin):
                ret = ret | bn
            bn = bn << 1
        return ret    

    def write_register(self,address,value):
        self.write_data_pins(address)  # Address to data bus
        GPIO.output(self.pin_bc1,1)    # BC1:BC2:BDIR = 1:0:0 LATCH
        GPIO.output(self.pin_bc1,0)    # BC1:BC2:BDIR = 0:0:0 idle
        self.write_data_pins(value)    # Value to data bus
        GPIO.output(self.pin_bc2,1)    # BC1:BC2:BDIR = 0:1:0 idle
        GPIO.output(self.pin_bdir,1)   # BC1:BC2:BDIR = 0:1:1 WRITE
        GPIO.output(self.pin_bdir,0)   # BC1:BC2:BDIR = 0:1:0 idle
        GPIO.output(self.pin_bc2,0)    # BC1:BC2:BDIR = 0:0:0 idle

    def read_register(self,address):        
        self.write_data_pins(address)
        GPIO.output(self.pin_bc1,1)
        GPIO.output(self.pin_bc1,0)        
        self.set_data_input()
        GPIO.output(self.pin_bc2,1)
        GPIO.output(self.pin_bc1,1)
        time.sleep(0.5)
        ret = self.read_data_pins()
        GPIO.output(self.pin_bc1,0)
        GPIO.output(self.pin_bc2,0) 
        self.set_data_output()
        return ret    
    
ay0 = AY38910([26,19,13,6,5,22,27,17],7,8,25)
# ay1 = AY38910([26,19,13,6,5,22,27,17],21,20,16)        

"""
GPIO AY-3-8910
26    D0
19    D1
13    D2
 6    D3
 5    D4
22    D5
27    D6
17    D7

 7   BC1-A
 8   BC2-A
25   BDIR-A

21   BC1-B
20   BC2-B
16   BDIR-B
"""