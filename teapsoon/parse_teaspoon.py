import sys, os, json
import time, datetime

sys.path.insert(0, '../helpers/')

from teaspoon import parse

print(parse("20160404_1120-1354_tsp01.txt"))
