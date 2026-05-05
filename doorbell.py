import board
import digitalio
import time
import os
import wifi
import socketpool
import adafruit_requests

# 1. NETWORKING SETUP
# Replace with your Le Potato's actual IP (ifconfig)
SERVER_IP = os.getenv("CIRCUITPY_SERVER_IP")
SERVER_URL = f"http://{SERVER_IP}:8000/doorbell"

print("Connecting to WiFi...")
try:
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
    print(f"Connected! Pico IP: {wifi.radio.ipv4_address}")
except Exception as e:
    print(f"WiFi Connection failed: {e}")

pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool)

# 2. HARDWARE SETUP
button = digitalio.DigitalInOut(board.GP15)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# 3. MORSE LIBRARY
MORSE_LIB = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6",
    "--...": "7", "---..": "8", "----.": "9"
}

def send_to_server(msg):
    """Sends the decoded Morse message to the Le Potato server."""
    try:
        led.value = True # Light up while sending
        print(f"Sending to Potato: {msg}")
        
        # FastAPI expects ?message=TEXT
        full_url = f"{SERVER_URL}?message={msg}"
        
        # Using a timeout prevents the Pico from freezing if the server is off
        with requests.post(full_url, timeout=5) as response:
            print(f"Potato Response ({response.status_code}): {response.text}")
            
    except Exception as e:
        print(f"Network Error: {e}")
    finally:
        led.value = False

def main():
    current_code = ""
    decoded_msg = ""
    last_release = time.monotonic()
    
    DOT_MAX = 0.25
    CHAR_GAP = 0.5
    WORD_GAP = 1.2

    print("Morse Client Ready. Tap away!")

    while True:
        # Button logic
        if not button.value:
            start_time = time.monotonic()
            while not button.value:
                pass
            duration = time.monotonic() - start_time
            current_code += "." if duration < DOT_MAX else "-"
            last_release = time.monotonic()
            print(f"Tap: {current_code[-1]}")

        # End of Character (pause > 0.5s)
        if current_code and (time.monotonic() - last_release) > CHAR_GAP:
            char = MORSE_LIB.get(current_code, "?")
            decoded_msg += char
            print(f"Message so far: {decoded_msg}")
            current_code = ""

        # End of Message (pause > 1.2s) -> SEND
        if decoded_msg and (time.monotonic() - last_release) > WORD_GAP:
            send_to_server(decoded_msg)
            decoded_msg = ""

        time.sleep(0.01)

if __name__ == "__main__":
    main()