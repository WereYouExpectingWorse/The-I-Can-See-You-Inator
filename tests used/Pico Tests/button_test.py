import board
import digitalio
import time

# Hardware Setup
# Button: GP15 (Physical Pin 20) 
# Ground: Any GND pin (e.g., Physical Pin 18 or 22)
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# Onboard LED for Pico W
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

print("--- Physical Button Test ---")
print("Hold the button down: The green LED should light up.")

while True:
    # button.value is True (High) normally due to Pull.UP
    # button.value becomes False (Low) when pressed/grounded
    if not button.value:
        led.value = True
        print("Button: PRESSED (GND detected)")
    else:
        led.value = False
    
    time.sleep(0.05)
