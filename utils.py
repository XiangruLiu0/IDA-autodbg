
import sark


def get_pre_addr(insn_addr, start=None, end=None,):
  segs = sark.segments()
  for s in segs:
    if s.name == '.text':
      if not start:
        start = s.start_ea
      if not end:
        end = s.end_ea

  pre_addr = start
  lines = sark.lines(start=start, end=end)
  for l in lines:
    if l.ea == insn_addr:
      return pre_addr
    pre_addr = l.ea
    # print(hex(l.ea))


def get_next_addr(insn_addr):
  current_line = sark.Line(ea=insn_addr)
  return insn_addr+current_line.size


def suffix_iterator(length, charset):
  if length == 1:
    for c in charset:
      yield c
  else:
    for c in charset:
      for other in suffix_iterator(length-1, charset):
        yield c + other


def prefix_iterator(length, charset):
  for i in suffix_iterator(length, charset):
    yield i[::-1]


def log(*args, **kwargs):
  print(">>>> ", end='')
  print(*args, **kwargs)


def patch_to_nop(start, end):
  import idc
  for ea in range(start, end):
    idc.patch_byte(ea, 0x90)
