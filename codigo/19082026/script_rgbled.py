import microbit
from microbit import pin0, pin1, pin2, sleep

leds = [
    pin0, pin1, pin2
]

def clear_leds(t):
    for l in leds:
        sleep(t)
        l.write_digital(0)

detected = False

while True:
    lvl = microbit.microphone.sound_level()
    
    if lvl > 200 and not detected:
        detected = True
        print(lvl)

        for l in leds:
            l.write_digital(1)
        sleep(5000)
        clear_leds(500)

        detected = False

        
