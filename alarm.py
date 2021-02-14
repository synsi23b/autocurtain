from datetime import datetime, timedelta
from threading import Timer
import logging

class Alarm:
  def __init__(self, hour, minute, func, selfreset=True):
    self._func = func
    self._hour = hour
    self._minute = minute
    self._alarm = None
    self._reset = selfreset

  def set_alarm(self):
    if self._alarm:
      self._alarm.cancel()
    ima = datetime.now()
    alarm = datetime(ima.year, ima.month, ima.day, self._hour, self._minute)
    logging.info(f"Current time: {ima} Alarm time: {alarm}")
    diff = alarm - ima
    secs = diff.total_seconds()
    if secs < 0:
      logging.info(f"Timediff less than zero {secs} -> Alarm tomorrow!")
      secs += 86400
    logging.info(f"Setting Alarm in {secs} seconds!")
    self._alarm = Timer(secs, self._triggered)
    self._alarm.start()

  def _triggered(self):
    logging.info("Alarm triggered!")
    self._alarm = None
    try:
      self._func()
    except Exception as e:
      logging.error(f"Error durring functor: {e}")
    if self._reset:
      self.set_alarm()

  def stop(self):
    if self._alarm:
      self._alarm.cancel()
    