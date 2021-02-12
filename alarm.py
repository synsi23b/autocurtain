from datetime import datetime, timedelta
from threading import Timer

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
    print(f"Current time: {ima}\nAlarm time: {alarm}")
    diff = alarm - ima
    secs = diff.total_seconds()
    if secs < 0:
      print(f"Timediff less than zero {secs} -> Alarm tomorrow!")
      secs += 86400
    print(f"Setting Alarm in {secs} seconds!")
    self._alarm = Timer(secs, self._triggered)
    self._alarm.start()

  def _triggered(self):
    print(f" {datetime.now()} Alarm triggered!")
    self._alarm = None
    try:
      self._func()
    except Exception as e:
      print(f"Error durring functor: {e}")
    if self._reset:
      self.set_alarm()

  def stop(self):
    if self._alarm:
      self._alarm.cancel()
    