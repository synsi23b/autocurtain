#!/usr/bin/python3

from gpiozero.pins.native import NativeFactory
from gpiozero.pins.mock import MockFactory
from gpiozero import LED, Device, Button
from stepper import Stepper
from alarm import Alarm
from threading import Thread
from signal import pause
from pathlib import Path
from datetime import datetime
import logging



#Device.pin_factory = MockFactory()
Device.pin_factory = NativeFactory()


led = LED(16)
button = Button(12, hold_time=0.5)
motor = Stepper(22, 23, 24, 25)
turns_to_change = 50000
state_file = Path.home() / "state.txt"
log_file = Path.home() / "curtain.log"

logging.basicConfig(filename=str(log_file), format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)

# set running state, machine will do nothing until fixed
state = "running"
with open(state_file, "r") as f:
  state = f.read().strip()
logging.info(f"Startup state is {state}")


def set_state(new_state):
  global state
  state = new_state
  with open(state_file, "w") as f:
    f.write(new_state)


def close_curtain():
  global state
  if state == "open":
    set_state("running")
    logging.info("Closing curtain!")
    led.blink(0.2, 0.8, 20)
    motor.turn(-turns_to_change)
    logging.info("Done closing")
    set_state("closed")
    motor.power_off()


def open_curtain():
  global state
  if state == "closed":
    set_state("running")
    logging.info("Opening curtain!")
    led.blink(0.8, 0.2, 20)
    motor.turn(turns_to_change)
    logging.info("Done opening")
    set_state("open")
    motor.power_off()


def on_button():
  global state
  logging.info(f"state: {state}")
  if state == "running":
    logging.info("already running, doing nothing")
    return
  if state == "open":
    t = Thread(target=close_curtain)
    t.start()
  if state == "closed":
    t = Thread(target=open_curtain)
    t.start()


open_alarm = Alarm(8, 0, open_curtain)
close_alarm = Alarm(22, 30, close_curtain)

open_alarm.set_alarm()
close_alarm.set_alarm()
button.when_activated = on_button

logging.info("Main Thread going into pause.")
pause()

open_alarm.stop()
close_alarm.stop()
