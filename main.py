from machine import Pin, SPI, ADC, deepsleep
import sh1106
import framebuf
import time

#Setup Display & Sensors
spi = SPI(1, baudrate=1000000, sck=Pin(18), mosi=Pin(23))
display = sh1106.SH1106_SPI(128, 64, spi, dc=Pin(16), res=Pin(2), cs=Pin(5))

soil = ADC(Pin(34))
soil.atten(ADC.ATTN_11DB)

bat_sensor = ADC(Pin(35)) 
bat_sensor.atten(ADC.ATTN_11DB)

#Image Loading Logic
def load_image(filename):
    try:
        with open(filename, 'rb') as f:
            data = f.read()
            return framebuf.FrameBuffer(bytearray(data), 128, 64, framebuf.MONO_HLSB)
    except:
        return None

img_happy   = load_image('happy.bin')
img_gettingthere = load_image('gettingthere.bin')
img_dry    = load_image('dry.bin')

#Battery Calculation
def get_battery_percentage():
    raw = bat_sensor.read()
    percentage = int((raw / 4095) * 100)
    return min(percentage, 100) # Cap at 100%

#Main Execution (The 20-second window)
val = soil.read()
bat_pc = get_battery_percentage()

display.fill(0)

#Show Moisture Image
if val < 1500:
    if img_happy: display.blit(img_happy, 0, 0)
elif val < 2500:
    if img_gettingthere: display.blit(img_gettingthere, 0, 0)
else:
    if img_dry: display.blit(img_dry, 0, 0)

#Overlay Battery Status (Bottom Right)
display.fill_rect(80, 50, 48, 14, 0) # Clear a small box for text
display.text(f"Bat:{bat_pc}%", 82, 54, 1)

display.show()

time.sleep(20)

display.fill(0)
display.show()
print("Nap time! Press Reset to check again.")
deepsleep() 
