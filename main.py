from machine import Pin, SPI, ADC, deepsleep
import sh1106
import framebuf
import time

# --- Setup Pins ---
spi = SPI(1, baudrate=1000000, sck=Pin(18), mosi=Pin(23))
display = sh1106.SH1106_SPI(128, 64, spi, dc=Pin(16), res=Pin(2), cs=Pin(5))
soil = ADC(Pin(34))
soil.atten(ADC.ATTN_11DB)

def load_image(filename):
    try:
        with open(filename, 'rb') as f:
            return framebuf.FrameBuffer(bytearray(f.read()), 128, 64, framebuf.MONO_HLSB)
    except: return None

img_happy   = load_image('happy.bin')
img_thirsty = load_image('gettingthere.bin')
img_dead    = load_image('dry.bin')

# --- Start the 60-second Monitoring Window ---
start_time = time.time()

print("Monitoring soil for 60 seconds...")

while (time.time() - start_time) < 60:
    # Take an average of 50 readings for stability
    avg_val = 0
    for _ in range(50):
        avg_val += soil.read()
    val = avg_val // 50
    
    display.fill(0)
    
    # Update Image based on current average
    if val < 1500:
        if img_happy: display.blit(img_happy, 0, 0)
    elif val < 2500:
        if img_thirsty: display.blit(img_thirsty, 0, 0)
    else:
        if img_dead: display.blit(img_dead, 0, 0)
        
    #show the raw number for easy calibration
    #display.text(f"Val:{val}", 0, 0, 1)
    
    display.show()
    time.sleep(1) # Refresh every second

# --- Power Down ---
display.fill(0)
display.show()
print("Minute is up. Going to sleep.")
deepsleep()

