import abc
import ida_dbg


class Actions(metaclass=abc.ABCMeta):
  """ This class wraps all the movements needed to be taken at certain circumstances during debugging with IDA, 
  it also extends IDAPython's API to perform some basic action during debug"""

  def __init__(self):
    # a list of dict, {addr:int, callback:func(self,````````
    self.bpt_actions = []
    self.exit_actions = []
    self.step_over_actions = []

  def request_continue(self):
    ida_dbg.request_step_over()
    ida_dbg.run_requests()
    ida_dbg.request_continue_process()
    ida_dbg.run_requests()


class B():
  def __init__(self, address, callback) -> None:
    self.address = address
    self.callback = callback


class SO():
  def __init__(self, callback) -> None:
    self.callback = callback


class E():
  def __init__(self, callback) -> None:
    self.callback = callback
