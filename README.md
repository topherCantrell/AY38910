# AY38910

| Game        | CPU  | Chips | Sound Frequency        | Caps      | CPU Freq |
| ---         | ---  | ---   | ---                    | ---       | ---      |
| Time Pilot  | Z80  | 2     | 14.318M / 8 = 1.78975M | .22 .047  | 1.78975M |
| Moon Patrol | 6803 | 2     | 3.579M / 4 = 0.89475M  | None      | 0.89475M |
| Forgger     | Z80  | 1     | 14.318M / 8 = 1.78975M | .22 .047  | 1.78975M |
| Scramble    | Z80  | 2     | 14.318M / 8 = 1.78975M | .22 .047  | 1.78975M |
| Omega Race  | Z80  | 2     | 15M / 12 = 1.25M       | None      | 1.5M     |
| 1942        | Z80  | 2     | 12M / 4 = 3M           | None      | 1.5M     |
| Tron        | Z80  | 2     | 2M                     | TODO      | 2M       |
| Spy Hunter  | Z80  | 2     | 2M                     | TODO      | 2M       |

The AY understands 3.3V signals. But if you read from the chip, it will return 5V signals, which
will damage a 3.3V micro.

I tried using the 3.3-5V converter boards, but I had trouble with two AYs on the data bus. I can read
from one AY just fine. But a second AY confuses the read. Writing to an AY with two on the bus works
just fine.

# Z80 on the rpi

https://pypi.org/project/z80/

```
mkdir z80
cd z80
git clone https://github.com/kosarev/z80.git
sudo apt-get install cmake
cmake z80
make # There are errors compiling one of the tests, but the main library compiles.
make test
make hello  # Or 'make examples' to build all examples at once.
```

Then the python wrapper:

```
python3 -m pip install z80
```

Have a look at the py files in the examples folder.

# Reading the Macro Pad

https://python-evdev.readthedocs.io/en/latest/tutorial.html

```
python3 -m pip install evdev
```

```python
from evdev import InputDevice, categorize, ecodes
dev = InputDevice('/dev/input/event0')

print(dev)
device /dev/input/event1, name "Dell Dell USB Keyboard", phys "usb-0000:00:12.1-2/input0"

for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))

```

# Effects

  - A Coin inserted
  - B Hop
  - C Die in water
  - D Die in road
  - E Time running out
  - F Next life begins
  - G Extra frog
  - H Landing safe
  - I Pick up mate
  - J Snake
  - K Race car
  - L Level complete
  - M Music: Intro
  - N Music: Main
  - O Play Intro+Main
  - P Music: Game over
  - Q Play next interlude
  - a-t Music: Interlude (20 songs)

# Managing the Frogger sound code

There are 14 spots of IN/OUT. They are all to port 0x40 or 0x80.

The main CPU signals the sound CPU with an interrupt. The sound CPU reads the command value from
the AY register 0x0E. The main loop enables interrupts briefly to check for new commands.

Capacitor filters set by reading from 0x6XXX.

Startup:
  - Clears RAM 4000 throiugh 43FF
  - Set SP to 4400
  - AR:7 = 3F (everything off, both I/O as inputs)
  - Amplitudes to 0

0136: Main loop
  - Wait for AY Port B to have bit 4 clear (700Hz sound loop)
  - Interrupts are on while waiting
  - Wait for AY Port B to set bit 4 clear
  - Process all 3 voices one by one
  - Turn interrupts on briefly between the voices

We'll assume that interrupts are checked/called in the python port B check