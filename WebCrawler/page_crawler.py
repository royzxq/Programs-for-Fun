
import urllib2
import re

class page_crawler:
	"""docstring for page_crawler"""

	def __init__(self):
		"""init the page crawler, set up the correct header"""
		self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
		self.headers = { 'User-Agent' : self.user_agent}

	def getPage(self, url):
		"""url is the target url, return the html page"""
		try:
			request = urllib2.Request(url,headers=self.headers)
			response = urllib2.urlopen(request)
			page = response.read()
			return page
		except urllib2.URLError, e:
			if hasattr(e,"reason"):
				print e.reason
			return None
	def getPageItems(self, url, pattern):
		"""pattern is the re pattern that user is interested, like img items"""
		page = self.getPage(url)
		if not page:
			print "page not found"
			return None
		items = re.findall(pattern, page)
		return items




