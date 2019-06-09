#!/usr/bin/env python3

import warnings

print("A")
warnings.warn("ohno", RuntimeWarning)
print("A1")
raise AssertionError("Hi")
print("B")