"""Timer context

Copied from http://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python

Then it can be used like this
	with Timer('objective function'):

"""
import time
class Timer(object):

	def __init__(self, name=None):
		self.name = name

	def __enter__(self):
		self.tstart = time.time()

	def __exit__(self, type, value, traceback):
		if self.name:
			print '[%s]' % self.name,
			print 'Elapsed: {0:0.2f} m'.format((time.time() - self.tstart)/60.0)
