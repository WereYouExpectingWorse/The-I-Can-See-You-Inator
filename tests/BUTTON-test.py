import gpiod #make sure you have the gpiod module installed to access and control GPIO pins
import time #built-in

CHIP = '1' #check which chip has access to the physical pins (what you see on the board)
INPUT_LINE = 85  #Physical Pin 33 on your Armbian kernel

def run_doorbell():
    try:
        chip = gpiod.Chip(CHIP)
        line = chip.get_line(INPUT_LINE)

        # Request as INPUT with internal PULL_UP
        # Button pressed = 0 (GND), Button released = 1 (3.3V)
        line.request(consumer="DoorbellInput", type=gpiod.LINE_REQ_DIR_IN, 
                     flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)

        print(f"Doorbell Ready! Monitoring Physical Pin 33 (Line {INPUT_LINE})...")
        print("Press Ctrl+C to stop.")

        while True:
            # Read the current state
            if line.get_value() == 0:
                print("Ding Dong! Button Pressed.")
                # Optional: Add your trigger logic here (e.g., play a sound)
                
                # Simple delay to avoid multiple triggers per press
                while line.get_value() == 0:
                    time.sleep(0.1)
                print("Button Released.")

            time.sleep(0.05) # Small polling delay
            
    except KeyboardInterrupt:
        print("\nShutting down doorbell script.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'line' in locals():
            line.release()

if __name__ == "__main__":
    run_doorbell()