import gpiod
import time

CHIP = '1'
BUTTON_PIN = 85  # Physical Pin 33
SPEAKER_PIN = 87 # Physical Pin 19

def play_tone(line, frequency, duration):
    """Generates a square wave tone on the specified line."""
    if frequency == 0:
        time.sleep(duration)
        return
    
    # Calculate delay (half the period of the frequency)
    delay = 1.0 / (frequency * 2)
    cycles = int(duration * frequency)
    
    for _ in range(cycles):
        line.set_value(1)
        time.sleep(delay)
        line.set_value(0)
        time.sleep(delay)

def main():
    chip = gpiod.Chip(CHIP)
    
    # Setup Button (Input)
    button = chip.get_line(BUTTON_PIN)
    button.request(consumer="Button", type=gpiod.LINE_REQ_DIR_IN, 
                   flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
    
    # Setup Speaker (Output)
    speaker = chip.get_line(SPEAKER_PIN)
    speaker.request(consumer="Speaker", type=gpiod.LINE_REQ_DIR_OUT)

    print("Doorbell Active! (Pin 33 -> Button, Pin 19 -> Speaker)")

    try:
        while True:
            # Button is 0 (GND) when pressed
            if button.get_value() == 0:
                print("Ding Dong!")
                
                # The 'Ding' (Higher pitch)
                play_tone(speaker, 660, 0.4) 
                # The 'Dong' (Lower pitch)
                play_tone(speaker, 523, 0.6) 
                
                # Wait for release to prevent infinite ringing
                while button.get_value() == 0:
                    time.sleep(0.1)
            
            time.sleep(0.05) # Power saving delay
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        speaker.set_value(0) # Ensure speaker is off
        button.release()
        speaker.release()

if __name__ == "__main__":
    main()
