#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""util.py: Collection of useful utilities."""

import sys
from itertools import islice
from collections import defaultdict


LOG_FORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"

def Enum(**enums):
  """An enumeration factory class."""
  obj = type('Enum', (), enums)
  obj.named_value = dict([(a, v) for a,v in vars(obj).items() if not a.startswith('__')])
  obj.value_named = dict([(v, a) for a,v in obj.named_value.items()])
  return obj

def debug(type_, value, tb):
  if hasattr(sys, 'ps1') or not sys.stderr.isatty():
    # we are in interactive mode or we don't have a tty-like
    # device, so we call the default hook
    sys.__excepthook__(type_, value, tb)
  else:
    import traceback, pdb
    # we are NOT in interactive mode, print the exception...
    traceback.print_exception(type_, value, tb)
    print("\n")
    # ...then start the debugger in post-mortem mode.
    pdb.pm()

def grouper(iterable, n):
    while True:
       chunk = tuple(islice(iterable, n))
       if not chunk:
           return
       yield chunk
