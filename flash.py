from machine import Pin
from utime import sleep

pin = Pin("LED", Pin.OUT)

print("LED starts flashing...")
while True:
    pin.toggle()
    sleep(1) # sleep 1sec