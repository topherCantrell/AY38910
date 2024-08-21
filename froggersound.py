import z80
import ay38910
import time
from evdev import InputDevice, categorize, ecodes
import threading

# OUT ($80),A
# NOTE ... a breakpoint at 0008 causes weird problems
OUT_ADDR = [0x000A,0x0247,0x0253,0x025A,0x026F,0x02C1,0x0309]

# OUT ($40),A
OUT_DATA = [0x000B,0x024A,0x0279,0x030C]

# IN A,($40)
IN_DATA = [0x0257,0x025E,0x02C5]

MACRO_COMMANDS = {
    'KEY_2': [0x00],  # Rotary button
    'KEY_3': [0x00],  # Rotary button
    'KEY_4': [0x00],  # Rotary button
    'KEY_5': [0x00],  # Rotary button
    #
    #
    'KEY_A': [0x01],  # Coin
    'KEY_B': [0x03],  # Squash
    'KEY_C': [0x02],  # Drown
    #
    'KEY_D': [0x04],  # Hop
    'KEY_E': [0x05],  # Hurry
    'KEY_F': [0x06],  # Born
    #
    'KEY_G': [0x07],  # Extra
    'KEY_H': [0xF0],  # Safe
    'KEY_I': [0x18],  # Mate
    #
    'KEY_J': [0x15],  # Snake
    'KEY_K': [0x17],  # Car
    'KEY_L': [0x11, 0x12, 0x13],  # Level
    #
    #
    'KEY_M': [0x09,0x0A,0x0B],  # Intro
    'KEY_N': [0x0F,0x0A,0x0B],  # Main song (broken)
    'KEY_O': [0x0F,0x0A,0x0B], # Main song (fixed)
    #
    'KEY_P': [0x0C,0x0D],  # Game over
    'KEY_Q': [0x08,0x0E],  # Next interlude
    'KEY_R': [], # NOT USED    

}

class FroggerSound(z80.Z80Machine):

    def task_read_macropad(self):        
        dev = InputDevice('/dev/input/event0')
        shifted = False
        for e in dev.read_loop():
            if e.type == ecodes.EV_KEY:
                if e.code == 42 or e.code == 54:
                    shifted = (e.value == 1)
                    continue
                if e.value == 0:
                    # Only interested in key down events
                    continue
                c = ecodes.KEY[e.code]
                if not shifted:
                    c = c.lower()
                print(c)
                if c == 'KEY_N':
                    print('>>> PLAY ORIGINAL')
                    self.memory[0x1065] = 0x96
                    self.memory[0x1134] = 0xDF
                elif c=='KEY_O':
                    print('>>> PLAY FIXED')
                    self.memory[0x1065] = 0xB6
                    self.memory[0x1134] = 0xCF
                if c.startswith('KEY'):
                    self._do_commands += MACRO_COMMANDS.get(c,[])  
                else:
                    i = ord(c[-1]) - ord('a') + 5
                    self._set_interlude = i
                    self._do_commands += [0x08,0x0E]

    def __init__(self):
        super().__init__()

        self.ay = ay38910.ay0
        
        with open('SoundCode.bin', 'rb') as f:
            self.set_memory_block(0, f.read())         
                
        for addr in OUT_ADDR:
            self.set_breakpoint(addr)            
        for addr in OUT_DATA:
            self.set_breakpoint(addr)            
        for addr in IN_DATA:
            self.set_breakpoint(addr)      
        
        self.set_breakpoint(0x70) # Return from interrupt   

        self.set_breakpoint(0x014D) # Processing tick        

        self.set_breakpoint(0x0B75) # Interlude

        self._DEBUG = 0x0097
        # self.set_breakpoint(self._DEBUG)  

        self._register_address = None
        self._tick = False
        self._reg_cache = {}

        # self._do_commands = [0x00, 0x09, 0x0A, 0x0B] # Intro song
        #self._do_commands = [0x00, 0x0C, 0x0D]
        self._do_commands = [0x00, 0x04]
        self._set_interlude = -1

        self._num_ticks_in_a_row = 0

        threading.Thread(target=self.task_read_macropad).start()

    def handle_breakpoint(self):

        pc = self.pc        

        if pc==0x0B75:
            if self._set_interlude>=0:
                self.a = self._set_interlude
                self._set_interlude = -1
            return True

        if pc == 0x70:
            # print(">>> RETURN FROM INTERRUPT")            
            # print('>>>',self.sp)
            if self._do_commands:
                self.pc = 0x0038 # If there is a command, repeat the interrupt
                self._reg_cache[14] = self._do_commands.pop(0) # Next command value
                self._last_command = self._reg_cache[14]            
            else:
                self.pc = 0x014E # Back to where we called the interrupt
            return True
        if pc == 0x014D:
            # print(">>> TICK")
            self._num_ticks_in_a_row += 1
            time.sleep(0.0012) 
            if self._do_commands:
                # If there is one (or more) commands, take the interrupt (returns to 014E)
                self._reg_cache[14] = self._do_commands.pop(0)
                self.pc = 0x0038
            return True
        
        if pc in OUT_ADDR:
            # Read/Writes are always preceded by a register address. We'll just store that here.
            self._register_address = self.a
        elif pc in OUT_DATA:
            # Write a value to the AY register
            self._reg_cache[self._register_address] = self.a      
            if self._num_ticks_in_a_row > 0:
                # print(">>> TICKS",self._num_ticks_in_a_row)
                self._num_ticks_in_a_row = 0      
            # print("OUT_DATA", self._register_address,self.a)    
            self.ay.write_register(self._register_address,self.a)                               
        elif pc in IN_DATA:
            # Register 15 is the timer. We toggle between 0 and 8.
            # TODO timing
            if self._register_address == 15:
                if self._tick:
                    self.a = 0x08
                    self._tick = False                                  
                else:
                    self.a = 0
                    self._tick = True                
            else:
                # Might be a register value we cached or it might be the sound command
                # We handle sound commands elsewhere
                self.a = self._reg_cache[self._register_address]                            
        
        if self.pc == self._DEBUG:
            print(">>> DEBUG STOP",hex(pc),self.a)
            return False
                 
        return True


m = FroggerSound()
m.pc = 0x0000

# for i in range(50000):
#     print(">>>",hex(m.pc))
#     m.ticks_to_stop = 1
#     events = m.run()
#     if events & m._BREAKPOINT_HIT:        
#         raise "BREAKPOINT"

while True:   
    events = m.run()
    if events & m._BREAKPOINT_HIT:        
        if not m.handle_breakpoint():
            break
