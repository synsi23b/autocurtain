from gpiozero.pins.native import NativeFactory
from gpiozero.pins.mock import MockFactory
from gpiozero import LED, Device
from time import sleep

#Device.pin_factory = MockFactory()
Device.pin_factory = NativeFactory()

class Stepper:
  def __init__(self, in1, in2, in3, in4):
    l1 = LED(in1)
    l2 = LED(in2)
    l3 = LED(in3)
    l4 = LED(in4)
    self._pins = [l1, l2, l3, l4]
    # static bool sequence[][4] = {{LOW, LOW, LOW, HIGH },
    #                   {LOW, LOW, HIGH, HIGH},
    #                   {LOW, LOW, HIGH, LOW },
    #                   {LOW, HIGH, HIGH, LOW},
    #                   {LOW, HIGH, LOW, LOW },
    #                   {HIGH, HIGH, LOW, LOW},
    #                   {HIGH, LOW, LOW, LOW },
    #                   {HIGH, LOW, LOW, HIGH}};
    self._steps = [
      (l1.off, l2.off, l3.off, l4.on),
      (l1.off, l2.off, l3.on, l4.on),
      (l1.off, l2.off, l3.on, l4.off),
      (l1.off, l2.on, l3.on, l4.off),
      (l1.off, l2.on, l3.off, l4.off),
      (l1.on, l2.on, l3.off, l4.off),
      (l1.on, l2.off, l3.off, l4.off),
      (l1.on, l2.off, l3.off, l4.on),
    ]
    self._rsteps = list(reversed(self._steps))

  def power_off(self):
    for p in self._pins:
      p.off()

  def turn(self, count):
    if count < 0:
      sequence = self._rsteps
      count = abs(count)
    else:
      sequence = self._steps
    count = int(count)
    while count != 0:
      count -= 1
      for step in sequence:
        sleep(0.001)
        for pin in step:
          pin()