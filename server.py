from fastapi import FastAPI, Request, Response
from contextlib import asynccontextmanager
import gpiod
import time

# Hardware Config
CHIP_ID = '1'
SPEAKER_LINE = 87

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- Initializing GPIO ---")
    speaker = None
    try:
        chip = gpiod.Chip(CHIP_ID)
        speaker = chip.get_line(SPEAKER_LINE)
        speaker.request(consumer="Doorbell", type=gpiod.LINE_REQ_DIR_OUT)
        print("--- GPIO Ready ---")
    except Exception as e:
        print(f"GPIO Error: {e}")
    
    # CRITICAL: Yield the speaker as a dictionary to share it
    yield {"speaker": speaker}
    
    if speaker:
        speaker.release()
        print("--- GPIO Released ---")

app = FastAPI(lifespan=lifespan)

@app.post("/doorbell")
async def trigger_doorbell(request: Request, message: str = "Unknown"):
    # Access the speaker from the request state
    speaker = request.state.speaker
    
    print(f"Received Morse: {message}")
    
    if speaker is None:
        return Response(content="no_speaker", media_type="text/plain")

    # Reuse your existing play_tone function logic here
    def play_tone(line, freq, duration):
        delay = 1.0 / (freq * 2)
        cycles = int(duration * freq)
        for _ in range(cycles):
            line.set_value(1)
            time.sleep(delay)
            line.set_value(0)
            time.sleep(delay)
    
    # Trigger the speaker
    if message.upper() == "GABRIEL":
        # Secret Easter Egg tone (Double beep)
        play_tone(speaker, 880, 0.2)
        play_tone(speaker, 950, 0.2)
        play_tone(speaker, 1100, 0.3)
    elif message.upper() == "WILMOTH":
        for i in range(1, 5):
            play_tone(speaker, 1300, 0.1)
            play_tone(speaker, 1200, 0.1)
            play_tone(speaker, 1000, 0.1)
        play_tone(speaker, 800, 0.2)
        play_tone(speaker, 800, 0.2)
        play_tone(speaker, 800, 0.3)
    else:
        # Standard Ding-Dong
        play_tone(speaker, 660, 0.4)
        play_tone(speaker, 523, 0.6)
        
    return {"status": "Success", "received": message}