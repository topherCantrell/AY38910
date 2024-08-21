# MACROPAD Hotkeys for Firia test station

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                      # REQUIRED dict, must be named 'app'
    'name' : 'Sound Effects', # Application name
    'macros' : [             # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x004000, 'Coin', ['A']),
        (0x400000, 'Squash', ['B']),
        (0x400000, 'Drown', ['C']),
        # 2nd row ----------
        (0x404000, 'Hop', ['D']),
        (0x004000, 'Hurry', ['E']),
        (0x004000, 'Born', ['F']),
        # 3rd row ----------
        (0x004000, 'Extra', ['G']),
        (0x004000, 'Safe', ['H']),
        (0x004000, 'Mate', ['I']),
        # 4th row ----------
        (0x000040, 'Snake', ['J']),
        (0x000040, 'Car', ['K']),
        (0x004000, 'Level', ['L']),
        # Encoder button ---
        (0x000000, 'E', ['@'])
    ]
}
