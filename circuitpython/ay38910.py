import digitalio


class AY38910:

    def __init__(self, pin_bc1, pin_bc2, pin_bdir, pins_data, is_5V_micro=False):
        self._is_5V_micro = is_5V_micro
        self._pin_bc1 = digitalio.DigitalInOut(pin_bc1)
        self._pin_bc2 = digitalio.DigitalInOut(pin_bc2)
        self._pin_bdir = digitalio.DigitalInOut(pin_bdir)        
        self._pins_data = []
        for p in pins_data:
            if isinstance(p, digitalio.DigitalInOut):
                self._pins_data.append(p)
            else:
                self._pins_data.append(digitalio.DigitalInOut(p))

        self._set_bus_output()
    
        for pin in [self._pin_bdir, self._pin_bc1, self._pin_bc2]:
            pin.direction = digitalio.Direction.OUTPUT
            pin.value = False            

    def get_data_pins(self):
        return self._pins_data    
    
    def _set_bus_output(self):
        for pin in self._pins_data:
            pin.direction = digitalio.Direction.OUTPUT

    def _write_data_pins(self, value):
        bn = 1
        for pin in self._pins_data:
            if value & bn:      
                pin.value = True  
            else: 
                pin.value = False  
            bn = bn << 1

    def write_register(self, reg_addr, value):
        self._write_data_pins(reg_addr)
        self._pin_bc1.value = True
        self._pin_bc1.value = False
        self._write_data_pins(value)
        self._pin_bc2.value = True
        self._pin_bdir.value = True
        self._pin_bdir.value = False
        self._pin_bc2.value = False     
    
    def _set_bus_input(self):
        for pin in self._pins_data:
            pin.direction = digitalio.Direction.INPUT
    
    def _read_data_pins(self):
        bn = 1
        ret = 0
        for pin in self._pins_data:
            if pin.value:
                ret = ret | bn
            bn = bn << 1
        return ret
    
    def read_register(self, reg_addr):
        if not self._is_5V_micro:
            raise Exception("This method is only available for 5V microcontrollers")
        self._write_control(False, False, False)
        self._write_data_pins(reg_addr)
        self._write_control(True, False, False)
        self._write_control(False, False, False)
        self._set_bus_input()
        self._write_control(False, True, False)
        self._write_control(True, True, False)
        ret = self._read_data_pins()
        self._write_control(False, True, False)
        self._write_control(False, False, False)
        self._set_bus_output()
        return ret
