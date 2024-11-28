import z80
import ay38910
import time
from evdev import InputDevice, ecodes
import threading

import RPi.GPIO as GPIO

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
                if e.code == 42 or e.code == 54:  # Shift keys
                    shifted = (e.value == 1)  # UP or DOWN status
                    continue
                if e.value == 0:
                    # Only interested in key down events
                    continue
                c = ecodes.KEY[e.code]
                if not shifted:
                    c = c.lower()
                print(c)
                if c == 'KEY_N':
                    # There is a bug in the original code that plays the main song.
                    # This puts the bad values back in memory (reverting the fix).                    
                    self.memory[0x1065] = 0x96
                    self.memory[0x1134] = 0xDF
                elif c=='KEY_O':
                    # There is a bug in the original code that plays the main song.
                    # This puts the fixed values in memory to play the main song. 
                    self.memory[0x1065] = 0xB6
                    self.memory[0x1134] = 0xCF
                if c.startswith('KEY'):
                    # For upper case keys, we have a list of sounds commands for each
                    self._do_commands += MACRO_COMMANDS.get(c,[])  
                else:
                    # For lower case keys, we poke the interlude song number into
                    # memory where the game will pick it up. Then we send the the
                    # play-interlude command.
                    i = ord(c[-1]) - ord('a') + 4
                    self.memory[0x42A7] = i
                    self._do_commands += [0x08,0x0E]

    def __init__(self):
        super().__init__()

        self.ay = ay38910.ay0

        GPIO.setup(16, GPIO.OUT)
        GPIO.output(16, 0)
        self.debug_pin_state = 0
        
        with open('SoundCode.bin', 'rb') as f:
            self.set_memory_block(0, f.read())     

        self.set_output_callback(self.handle_OUT)
        self.set_input_callback(self.handle_IN)           
        
        # This is start of the processing tick. This is where we trigger the interrupt if there
        # are commands to be processed. We also use this as a timing point for the 700MHz timer.
        self.set_breakpoint(0x014D) 

        # This is the return from interrupt command. We loop back to repeat the interrupt
        # for any queued sound commands.
        self.set_breakpoint(0x70)                              

        self._register_address = None  # The last selected AY register address
        self._tick = False  # The 700MHz timer bit value
        self._reg_cache = {}  # Cache of AY register values
        
        self._do_commands = [0x00, 0x04]  # Hopping sound at startup
        self._set_interlude = -1  # Greater than -1 means set the interlude to this value

        # Start the thread to read the macropad key inputs
        threading.Thread(target=self.task_read_macropad).start()

    def handle_OUT(self, address, value):                

        address &= 0xFF
        
        if address == 0x80:  # Hardware: latch AY register
            # Reads/Writes are always preceded by a register address. We'll just store that here.
            self._register_address = value            
        else:  # Must be 0x41, Hardware: Write AY register
            # Cache the value for reading back            
            self._reg_cache[self._register_address] = value
            # Write a value to the AY register
            self.ay.write_register(self._register_address,value)  

    def handle_IN(self, _):
        # We only ever read port 0x40 (AY register data)
        if self._register_address == 15:
            # AY port B is the 700MHz timer. We toggle between 0 and 8 (bit 3).
            # There is a wait-loop in the frogger code that checks for the
            # rising edge of this bit. We'll use a breakpoint to implement the
            # wait. Here, we return a change every time.
            if self._tick:
                ret = 0x08                               
            else:
                ret = 0
            self._tick = not self._tick
        else:
            # Any other AY register -- return the cached value. The command
            # injector will set the cache value for AY register 14 (sound command).
            ret = self._reg_cache[self._register_address]
        return ret

    def handle_breakpoint(self):

        GPIO.output(16, self.debug_pin_state)
        self.debug_pin_state = not self.debug_pin_state
        
        pc = self.pc              

        if pc == 0x014D:
            # Start of the timing tick. The original code waits 1/700MHz = 0.0014s.
            # The sleep value below is a little less, but it matches the speed of the
            # original hardware (timed against with the main intro music).
            time.sleep(0.0012)  

            # If there is one (or more) commands, take the interrupt (returns to 014E)
            if self._do_commands:                
                self._reg_cache[14] = self._do_commands.pop(0)
                self.pc = 0x0038  # Interrupt service routine
            return True   

        if pc == 0x70:            
            # This the return from the interrupt. But if there is another command, we
            # repeat the vector to read them all.
            if self._do_commands:
                self.pc = 0x0038 # If there is a command, repeat the interrupt
                self._reg_cache[14] = self._do_commands.pop(0) # Next command value
                self._last_command = self._reg_cache[14]            
            else:
                # Back to where we called the interrupt
                self.pc = 0x014E 
            return True        
                 
        return False


m = FroggerSound()
m.pc = 0x0000  # Startup goes to address 0x0000

while True:   
    events = m.run()
    # Run until we hit an unhandled breakpoint
    if events & m._BREAKPOINT_HIT:        
        if not m.handle_breakpoint():
            break
