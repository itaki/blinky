from gpiozero import RGBLED, LED, Button
from signal import pause

led = RGBLED(5, 6, 12)
#led.color = (0, 1, 1)

led.pulse(fade_in_time=1, fade_out_time=1, on_color=(1, 1, 1), off_color=(0, 0, 0), n=None, background=True)

pause()