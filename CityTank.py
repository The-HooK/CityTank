#! /usr/bin/env python

import sys
import os

try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'libr'))
    sys.path.insert(0, libdir)

sys.path.insert(1, 'libr')
import run
run.main()
