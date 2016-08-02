"""
Author: Zheng Yang

This is supposed to be a small collection of helper functions, and this is supposed to parse the output for the command /acq_hist, where the parent file marvin.py writes the terminal output of the histogram, wave descriptor.

It assumes that there is a separator '---' between the two readings.

params:
	fp: 	Location to file to be parsed
		e.g. './acquisition/saves/20150820_1614'

"""

def Parse(fp):
		cfp = '.'
		f = open(cfp+fp, 'r')
		s = ''
		c = 0
		for line in f:
			if c < 2:
				pass
			else:
				s += line
			c += 1
		s = s.split('---')
		hist = s[0]
		desc = s[1]


		def parsehist(s):

			x = s.split('\n')
			x = ''.join(x)
			x = x.strip()
			x = x.split("  ")
			x = map(lambda i: float(i), x)
			return x
		def parsedesc(s):
			s = s.split('"')[1]
			x = s.split('\n')
			c = 0
			desc = {}
			for i in x:
				if c == 0:
					pass
				else:
					j = i.split(':')
					if not len(j) == 2:
						continue
					desc[(j[0]).lower().strip()] = j[1].strip()
				c += 1
			return desc
		def getx(desc, n):
			m = desc['horiz_interval']
			c = desc['horiz_offset']
			print m
			x = ''

		desc = parsedesc(desc)
		hist = parsehist(hist)
		print desc
		#data = getx(desc, len(hist))
		f = open(cfp+fp, 'w')
		for i in xrange(len(hist)):
			f.write(str(i) + '\t' + str(hist[i]) + '\n')
		

