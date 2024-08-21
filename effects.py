
import ay38910
import time

ay = ay38910.ay0

def gunshot():
    '''
    Fig. 28 GUNSHOT SOUND EFFECT CHART

    Registers and values in octal

    R6  017 Set Noise period to mid-value.
    R7  007 Enable Noise only on Channels A,B,C.
    R10 020
    R11 020 Select full amplitude range under direct
    R12 020 control of Envelope Generator.
    R14 020 Set Envelope period to 0.586 seconds.
    R15 000 Select Envelope "decay", one cycle only
    '''
    
    ay.write_register(0o00,0)
    ay.write_register(0o01,0)
    ay.write_register(0o02,0)
    ay.write_register(0o03,0)
    ay.write_register(0o04,0)
    ay.write_register(0o05,0)
    ay.write_register(0o06,0o017)
    ay.write_register(0o07,0o007)
    ay.write_register(0o10,0o020)
    ay.write_register(0o11,0o020)
    ay.write_register(0o12,0o020)
    ay.write_register(0o13,0)
    ay.write_register(0o14,0o020)
    ay.write_register(0o15,0o000)

def explosion():
    '''
    Fig. 29 EXPLOSION SOUND EFFECT CHART

    Registers and values in octal

    R6  000 Set Noise period to max. value.
    R7  007 Enable Noise only, on Channels A,B,C.
    R10 020
    R11 020 Select full amplitude range under
    R12 020 direct control of Envelope Generator.
    R14 070 Set Envelope period to 2.05 seconds.
    R15 000 Select Envelope "decay", one cycle only
    '''   

    ay.write_register(0o00,0)
    ay.write_register(0o01,0)
    ay.write_register(0o02,0)
    ay.write_register(0o03,0)
    ay.write_register(0o04,0)
    ay.write_register(0o05,0)
    ay.write_register(0o06,0o000)
    ay.write_register(0o07,0o007)
    ay.write_register(0o10,0o020)
    ay.write_register(0o11,0o020)
    ay.write_register(0o12,0o020)
    ay.write_register(0o13,0)
    ay.write_register(0o14,0o070)
    ay.write_register(0o15,0o000)

def wolf_whistle():
    '''
    FIG. 32 WOLF WHISTLE SOUND EFFECT CHART

    R6 001 Set Noise period to minimum value
    R7 056 Enable Tone on Channel A, Noise on Channel B.
    R10 017 Select maximum amplitude on Channel A.    
    R11 011 Select lower amplitude on Channel B.

    Sweep effect for Channel A Tone period via a
    processor loop with appoximately 12ms
    wait time between each step from 100 to 040.

    R0 100 (start)
    R0 040 (end)

    Wait appoximately 150ms before continuing

    A processor loop with approximately 25ms
    wait time between each step from 100 to 060.

    R0 100 (start)
    R0 060 (end)

    A processor loop with approximately 6ms
    wait time between each step from 060 to 150.

    R0 060 (start)
    R0 150 (end)

    Turn off Channels A and B to end effect.

    R10 000
    R11 000
    '''

    ay.write_register(0o00,0)
    ay.write_register(0o01,0)
    ay.write_register(0o02,0)
    ay.write_register(0o03,0)
    ay.write_register(0o04,0)
    ay.write_register(0o05,0)
    ay.write_register(0o06,0o001)
    ay.write_register(0o07,0o056)
    ay.write_register(0o10,0o017)
    ay.write_register(0o11,0o011)
    ay.write_register(0o12,0)
    ay.write_register(0o13,0)
    ay.write_register(0o14,0)
    ay.write_register(0o15,0)

    for i in range(0o100, 0o40-1, -1):
        ay.write_register(0o00, i)
        time.sleep(0.012)

    time.sleep(0.150)

    for i in range(0o100, 0o60-1, -1):
        ay.write_register(0o00, i)
        time.sleep(0.025)

    for i in range(0o060, 0o150+1, 1):
        ay.write_register(0o00, i)
        time.sleep(0.006)

    ay.write_register(0o10,0o000)
    ay.write_register(0o11,0o000)
    

def race_car():

    '''
    FIG. 32 RACE CAR SOUND EFFECT CHART

    R3 017 Set Channel Tone period
    R7 074 Enable Tones only on Channels A and B
    R10 017 Select maximum amplitude on Channel A.
    R11 012 Select lower amplitude on Channel B.

    Sweep effect for Channel A Tone period via a  
    processor loop with approximately 3ms wait time between
    each step from 013/000 to 004/000.

    A processor loop with approximately 3ms wait time between
    each step from 011/000 to 003/000.

    A processor loop with approximately 3ms wait time between
    each step from 011/000 to 003/000.

    Turn off Channels A and B to end effect.

    R10 000
    R11 000

    '''

    ay.write_register(0o00,0)
    ay.write_register(0o01,0)
    ay.write_register(0o02,0)
    ay.write_register(0o03,0o017)
    ay.write_register(0o04,0)
    ay.write_register(0o05,0)
    ay.write_register(0o06,0)
    ay.write_register(0o07,0o074)
    ay.write_register(0o10,0o017)
    ay.write_register(0o11,0o012)
    ay.write_register(0o12,0)
    ay.write_register(0o13,0)
    ay.write_register(0o14,0)
    ay.write_register(0o15,0)

    for i in range(0o13<<8, 0o04<<8-1, -1):
        ay.write_register(0o00, i & 0xff)
        ay.write_register(0o01, i >> 8)
        time.sleep(0.003)

    for i in range(0o11<<8, 0o03<<8-1, -1):
        ay.write_register(0o00, i & 0xff)
        ay.write_register(0o01, i >> 8)
        time.sleep(0.003)

    for i in range(0o06<<8, 0o01<<8-1, -1):
        ay.write_register(0o00, i & 0xff)
        ay.write_register(0o01, i >> 8)
        time.sleep(0.006)

    ay.write_register(0o10,0o000)
    ay.write_register(0o11,0o000)

# gunshot()
# explosion()
# wolf_whistle()
race_car()