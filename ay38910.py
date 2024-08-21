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
        self.write_data_pins(address)
        GPIO.output(self.pin_bc1,1)
        GPIO.output(self.pin_bc1,0)
        self.write_data_pins(value)
        GPIO.output(self.pin_bc2,1)
        GPIO.output(self.pin_bdir,1)
        GPIO.output(self.pin_bdir,0)
        GPIO.output(self.pin_bc2,0)    

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
    
ay0 = AY38910([17,27,22,5,6,13,19,26],16,20,21)
ay1 = AY38910([17,27,22,5,6,13,19,26],24,25,12)        

"""
GPIO AY-3-8910
17     D0
27     D1
22     D2
 5     D3
 6     D4
13     D5
19     D6
26     D7

16     BC1-A
20     BC2-A
21     BDIR-A

24     BC1-B
25     BC2-B
12     BDIR-B
"""