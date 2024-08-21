import board
from ay38910 import AY38910

def test_tones():
    ay38910_0.write_register(7, 0b11_111_000)
    ay38910_0.write_register(8, 0b0000_1000)
    ay38910_0.write_register(9, 0b0000_1000)
    ay38910_0.write_register(10, 0b0000_1000)
    ay38910_0.write_register(0,128)
    ay38910_0.write_register(1,1)
    ay38910_0.write_register(2,128)
    ay38910_0.write_register(3,2)
    ay38910_0.write_register(4,128)
    ay38910_0.write_register(5,3)

    ay38910_1.write_register(7, 0b11_111_000)
    ay38910_1.write_register(8, 0b0000_1000)
    ay38910_1.write_register(9, 0b0000_1000)
    ay38910_1.write_register(10, 0b0000_1000)
    ay38910_1.write_register(0,255)
    ay38910_1.write_register(1,3)
    ay38910_1.write_register(2,255)
    ay38910_1.write_register(3,2)
    ay38910_1.write_register(4,255)
    ay38910_1.write_register(5,1)

#                 0  1  2  3   4   5   6   7
PINS_DATA =      [board.GP2, board.GP3, board.GP4, board.GP5, board.GP6, board.GP7, board.GP8, board.GP9]
#
PIN_A_BC1 = board.GP10
PIN_A_BC2 = board.GP11
PIN_A_BDIR = board.GP12
#
PIN_B_BC1 = board.GP13
PIN_B_BC2 = board.GP14
PIN_B_BDIR = board.GP15

ay38910_0 = AY38910(PIN_A_BC1, PIN_A_BC2, PIN_A_BDIR, PINS_DATA)
ay38910_1 = AY38910(PIN_B_BC1, PIN_B_BC2, PIN_B_BDIR, ay38910_0.get_data_pins())
