import abc
import string
from autodbg.utils import prefix_iterator


class State(metaclass=abc.ABCMeta):
  def next(self):
    pass

  def back(self):
    pass

  def forward(self):
    pass


class NumState(State):
  def __init__(self):
    super().__init__()

  def back(self):
    pass

  def forward(self):
    pass


class StrState(State):
  def __init__(self, length, prefix='', suffix='', charset=None, padding='') -> None:
    """
    Args:
      length (int): flag 的长度
      prefix (str): 初始 flagF
      charset (str): 字符集
      padding (str): 默认填充
    """
    self.raw_length = length-len(prefix)-len(suffix)
    self.charset = string.printable if charset == None else charset
    self.padding = self.charset[0] if padding == '' else padding
    self.prefix = prefix
    self.suffix = suffix
    self._raw = self.raw_length*self.padding
    self.iterator = prefix_iterator(self.raw_length, self.charset)

  def pad(self, raw):
    return "{}{}{}".format(self.prefix, raw, self.suffix)

  @property
  def current(self):
    return self.pad(self._raw)

  def next(self,):
    try:
      # iterate
      self._raw = next(self.iterator)
      # join
    except StopIteration:
      # 没有路时回退
      raise Exception("curt_depth < 0, can't trace back anymore!!!")

  def forward(self, n):
    self.prefix += self._raw[:n]
    self.raw_length -= n
    self.iterator = prefix_iterator(self.raw_length, self.charset)

  def back(self, n):
    self.prefix[:len(self.prefix)-n]
    self.raw_length += n
    self.iterator = prefix_iterator(self.raw_length, self.charset)


class CharState(State):
  def __init__(self, length, prefix='', suffix='', charset=None, padding='') -> None:
    """
    Args:
      length (int): flag 的长度
      prefix (str): 初始 flagF
      charset (str): 字符集
      padding (str): 默认填充
    """
    # length
    self.raw_length = length - len(prefix) - len(suffix)
    # charset
    self.charset = string.printable if not charset else charset
    # default padding
    self.padding = charset[0] if not padding else padding
    # prefix & suffix
    self.prefix = prefix
    self.suffix = suffix
    # iterator
    self.depth = 0
    # vertex
    self.vertexes = [iter(self.charset)] * self.raw_length
    # brute chars
    self.brute_chars = [self.padding] * self.raw_length
    self.raw = self.padding*self.raw_length

  def pad(self, raw):
    return "{}{}{}".format(self.prefix, raw, self.suffix)

  @property
  def current(self):
    return self.pad(self.raw)

  def next(self) -> str:
    """返回当前 str + 迭代的 char"""
    try:
      # iterate
      self.brute_chars[self.depth] = next(self.vertexes[self.depth])
      # join
      self.raw = ''.join(self.brute_chars)
    except StopIteration:
      # 没有路时回退
      self.back(1)
      if self.depth < 0:
        raise Exception("curt_depth < 0, can't trace back anymore!!!")
      else:
        return self.next()

  def back(self, n):
    self.brute_chars[self.depth] = self.padding
    # print(self.brute_chars)
    self.depth -= n

  def forward(self, n):
    self.depth += n
    self.vertexes[self.depth] = iter(self.charset)


# if __name__ == '__main__':
#   # suggest that the desired flag is flag{233}
#   fs = StrState(9, "flag{", suffix='}', charset='123', padding=' ')
#   condition = iter(["flag{2", "flag{23", "flag{233}"])
#   current = next(condition)
#   while True:
#     fs.next()
#     f = fs.current
#     print(f)
#     if f.startswith(current):
#       fs.forward(1)
#       try:
#         current = next(condition)
#       except:
#         print("You got the flag")
#         break