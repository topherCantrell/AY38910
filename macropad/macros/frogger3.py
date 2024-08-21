# MACROPAD Hotkeys for Firia test station

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values

app = {                      # REQUIRED dict, must be named 'app'
    'name' : 'Frogger Music', # Application name
    'macros' : [             # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x400040, 'I7', ['g']),
        (0x400040, 'I8', ['h']),
        (0x400040, 'I9', ['i']),
        # 2nd row ----------
        (0x400040, 'I10', ['j']),
        (0x400040, 'I11', ['k']),
        (0x400040, 'I12', ['l']),
        # 3rd row ----------
        (0x400040, 'I13', ['m']),
        (0x400040, 'I14', ['n']),
        (0x400040, 'I15', ['o']),
        # 4th row ----------
        (0x400040, 'I16', ['p']),
        (0x400040, 'I17', ['q']),
        (0x400040, 'I18', ['r']),
        # Encoder button ---
        (0x400040, 'E', ['$'])
    ]
}
