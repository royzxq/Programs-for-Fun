import datetime.datetime as date
from multiprocessing import Lock

class RateLimter:
	message_queue = []
	max_size = 10
	queue_lock = Lock()
	time_lock = Lock()
	mode = "simple"
	count = 0
	def __init__(self, qps, func):
		"""
		for simplicity, qps must be int
		"""
		self.qps = qps
		self.func = func
		self.pre_time = date.now()
		self.allowance = qps
		if self.mode == "bucket":
			self.bucket = [-1] * self.qps

	def callback(self, message):
		with time_lock:
			if self.mode == "simple":
				current = date.now()
				time_passed = (current - self.pre_time)
				time_passed = time_passed.seconds + time_passed.microseconds/1000000.0
				self.pre_time = current
				self.allowance += time_passed * self.qps
				if self.allowance > self.qps:
					self.allowance = self.qps
				elif self.allowance >= 1:
					self.func(message)
					self.allowance -= 1
				else:
					with queue_lock:
						if len(message_queue) < max_size:
							self.message_queue.append(message)
			elif self.mode == "bucket":
				current = date.now()
				time_passed = (current - self.bucket[self.wrap(count-5)])
				if time_passed.seconds + time_passed.microseconds/1000000.0 > 1:
					self.bucket[self.wrap[count]] = current
					count += 1
					self.func(message)
				else:
					with queue_lock:
						if len(message_queue) < max_size:
							self.message_queue.append(message)
	def wrap(self, i):
		while i < 0:
			i += self.qps
		return i % self.qps