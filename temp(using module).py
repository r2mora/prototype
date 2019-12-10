
import RPi.GPIO as GPIO
from mcp3208 import MCP3208
import time

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

ch0 = 0
ch1 = 1
adc = 0

def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    global adc
    adc = MCP3208()
    

def main():
    init()
    time.sleep(2)
    print("analog level\n")
    while True:
        temp_value = adc.read(ch0)
        humi_value = adc.read(ch1)
        #temp_value = -66.875 + 218.75 * (temp_value / 3.3)
        #humi_value = -12.5 + 125 * (humi_value / 3.3)
        print("temp: %d" % temp_value)
        print("humid: %d" % humi_value)
        time.sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
