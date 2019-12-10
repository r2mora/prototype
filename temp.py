import RPi.GPIO as GPIO
import time

SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

ch0 = 0
ch1 = 1

def init():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)

def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)	
    GPIO.output(clockpin, False)  
    GPIO.output(cspin, False)
    commandout = adcnum
    commandout |= 0x18  
    commandout <<= 3    
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
    
    adcout = 0
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1
        
        if (GPIO.input(misopin)):
            adcout |= 0x1
            
    GPIO.output(cspin, True)
    adcout >>= 1
    return adcout

def main():
    init()
    time.sleep(2)
    print("analog level\n")
    while True:
        temp_value = readadc(ch0, SPICLK, SPIMOSI, SPIMISO, SPICS)
        humi_value = readadc(ch1, SPICLK, SPIMOSI, SPIMISO, SPICS)
       # temp_value = (-66.875 + 218.75 * (temp_value / 3.3))
       # humi_value = (-12.5 + 125 * (humi_value / 3.3))
        print("temp: %d" % temp_value)
        print("humi: %d" % humi_value)
        time.sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()
