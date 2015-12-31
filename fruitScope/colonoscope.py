import sys
sys.path.insert(0, '../helpers/')
import lecroy
import argparse

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("t", "--duration", help="Duration of acquisition", type = int)
  args = parser.parse_args()
  print args.t
  scope = lecroy.Lecroy()
  
  
main()
