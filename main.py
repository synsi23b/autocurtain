#!/usr/bin/python3

from gpiozero.pins.native import NativeFactory
from gpiozero import LED, Device, Button
from time import sleep
import datetime
from stepper import Stepper

Device.pin_factory = NativeFactory()

led = LED(16)
button = Button(12, bounce_time=0.2)
motor = Stepper(22, 23, 24, 25)

print(f"It's now : {datetime.time.now()}")

def close_curtain():
  led.blink(0.2, 0.5, 10)
  motor.turn(500)
  return "closed"


def open_curtain():
  led.blink(0.5, 0.2, 10)
  motor.turn(-500)
  return "open"


def on_button():
  global state
  prevstate = state
  if state == "running":
    print("already running, doing nothing")
    return
  if state == "open":
    state = "running"
    state = close_curtain()
  if state == "closed":
    state = "running"
    state = open_curtain()
  print(f"{prevstate} -> {state}")


button.when_activated = on_button


sleep(1000)