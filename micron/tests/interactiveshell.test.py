#!/usr/bin/env python3

class Hmm():
	def __init__(self):
		pass

	def hi(self):
		print("Hi")

	def bye(self):
		print("Bye")

	def __enter__(self):
		return self

	def __exit__(self, e_type, e_val, traceback):
		print("exiting")
		pass


if __name__ == '__main__':
	with Hmm() as x:
		# import pdb; pdb.set_trace()
		import code; code.interact(local=locals())