import sys

sys.path.insert(0, '../helpers/')

from teaspoon import parse

(data, metadata) = (parse("20160404_1120-1354_tsp01.txt"))
