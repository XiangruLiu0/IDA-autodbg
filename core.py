import ida_dbg
from autodbg.actions import Actions, B, E, SO
from autodbg.utils import log


class AutoCracker(ida_dbg.DBG_Hooks):
  def __init__(self, actions: Actions = None,) -> None:
    ida_dbg.DBG_Hooks.__init__(self)
    self.actions = actions

  def run(self):
    for a in self.actions.bpt_actions:
      a: B
      ida_dbg.add_bpt(a.address)
    self.hook()
    ida_dbg.request_start_process()
    ida_dbg.run_requests()

  def hook(self):
    for a in self.actions.bpt_actions:
      a: B
      ida_dbg.add_bpt(a.address)
    super().hook()

  def set_bs(self, _b: Actions):
    self.actions = _b

  def dbg_bpt(self, tid, ea) -> "int":
    """
    Returns: int : 1 to display a breakpoint warning dialog if the process is suspended; 0 to never display a
    breakpoint warning dialog; 1 to always display a breakpoint warning dialog.
    """
    # return values:

    # ac.log(hex(ea))
    for a in self.actions.bpt_actions:
      a: B
      if ea == a.address:
        a.callback()
    return 0

  def dbg_step_over(self, *args):
    for so in self.actions.step_over_actions:
      so: SO
      so.callback()

  def dbg_process_exit(self, pid, tid, ea, code):
    self.unhook()
    log("unhooked")
    for a in self.actions.bpt_actions:
      a: B
      ida_dbg.del_bpt(a.address)
    log("bpts removed")
    for e in self.actions.exit_actions:
      e: E
      e.callback()
    log("exit actions finished")
