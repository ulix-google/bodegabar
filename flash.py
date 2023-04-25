from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
while True:
    pin.toggle()
    sleep(2) # sleep 2 sec.