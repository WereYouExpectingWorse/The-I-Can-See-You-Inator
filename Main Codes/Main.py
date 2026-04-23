import gpiod
import time

CHIP = '1'
BUTTON_PIN = 85
SPEAKER_PIN = 87

# Morse Timing
DOT_MAX = 0.25
WORD_GAP = 1.2  # Time to wait before "submitting" the code

MORSE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', 
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', 
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O', 
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T', 
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y', '--..': 'Z'
}

def play_tone(line, freqs, durations):
    for f, d in zip(freqs, durations):
        if f == 0:
            time.sleep(d)
            continue
        delay = 1.0 / (f * 2)
        cycles = int(d * f)
        for _ in range(cycles):
            line.set_value(1)
            time.sleep(delay)
            line.set_value(0)
            time.sleep(delay)

def FirstEE(spk):
    print("♪ Easter Egg! ♪")
    notes = [349, 392, 415, 440, 0, 349, 392, 415, 349]
    lengths = [0.1, 0.1, 0.1, 0.2, 0.05, 0.1, 0.1, 0.1, 0.4]
    play_tone(spk, notes, lengths)

def main():
    chip = gpiod.Chip(CHIP)
    btn = chip.get_line(BUTTON_PIN); btn.request("Btn", gpiod.LINE_REQ_DIR_IN, gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
    spk = chip.get_line(SPEAKER_PIN); spk.request("Spk", gpiod.LINE_REQ_DIR_OUT)

    current_letter = ""
    decoded_message = ""
    last_release = time.time()

    print("Doorbell Live. Tap GAB for the secret theme.")

    try:
        while True:
            # 1. Capture Taps
            if btn.get_value() == 0:
                start = time.time()
                while btn.get_value() == 0: time.sleep(0.01)
                duration = time.time() - start
                current_letter += "." if duration < DOT_MAX else "-"
                last_release = time.time()

            # 2. Check for Letter/Word completion
            if current_letter != "" and (time.time() - last_release) > 0.5:
                # Character finished, look it up
                char = MORSE_DICT.get(current_letter, "?")
                decoded_message += char
                print(f"Decoded: {decoded_message} (Code: {current_letter})")
                current_letter = "" # Reset for next letter

            # 3. Check Word vs Secret Key
            if decoded_message != "" and (time.time() - last_release) > WORD_GAP:
                if "GAB" in decoded_message:
                    FirstEE(spk)
                else:
                    print("Standard Doorbell")
                    play_tone(spk, [660, 523], [0.4, 0.6])
                
                decoded_message = "" # Clear for next guest

            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        btn.release(); spk.release()

if __name__ == "__main__":
    main()
