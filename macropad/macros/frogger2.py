# MACROPAD Hotkeys for Firia test station

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                      # REQUIRED dict, must be named 'app'
    'name' : 'Frogger Music', # Application name
    'macros' : [             # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, 'Intro', ['M']),
        (0x004000, 'Main', ['N']),
        (0x004000, 'Fixed', ['O']),
        # 2nd row ----------
        (0x004000, 'Over', ['P']),
        (0x004040, 'Next', ['Q']),
        (0x000000, '', []),
        # 3rd row ----------
        (0x400040, 'I1', ['a']),
        (0x400040, 'I2', ['b']),
        (0x400040, 'I3', ['c']),
        # 4th row ----------
        (0x400040, 'I4', ['d']),
        (0x400040, 'I5', ['e']),
        (0x400040, 'I6', ['f']),
        # Encoder button ---
        (0x000000, 'E', ['#'])
    ]
}
