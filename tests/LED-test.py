import gpiod #make sure you have the gpiod module to access the gpio pins
import time #built-in

# Pin 26 on Le Potato (AML-S905X-CC) maps to:
CHIP = '1' #use gpiod cmds to find which chip accesses physical pins
LINE_OFFSET = 87 

def blink_led():
    # Access the GPIO chip
    chip = gpiod.Chip(CHIP)
    # Get the specific line for Pin 26
    line = chip.get_line(LINE_OFFSET)

    # Request the line as an output
    # Consumer label helps identify the script in 'gpioinfo'
    line.request(consumer="BlinkScript", type=gpiod.LINE_REQ_DIR_OUT)

    print(f"Blinking Physical Pin 26 (Chip {CHIP}, Line {LINE_OFFSET})...")
    print("Press Ctrl+C to stop.")

    try:
        while True:
            line.set_value(1)  # Turn ON (3.3V)
            time.sleep(0.5)    # Wait 500ms
            line.set_value(0)  # Turn OFF (0V)
            time.sleep(0.5)    # Wait 500ms
    except KeyboardInterrupt:
        print("\nStopping blink script...")
    finally:
        line.release()  # Always release the pin when finished

if __name__ == "__main__":
    blink_led()

