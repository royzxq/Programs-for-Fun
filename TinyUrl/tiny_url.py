# -*- coding: utf-8 -*-

import random
import LRU
import sqlite3 as lite
import sys
# the tiny url service that support random, cache and expire function and sqlite database

class Shortener():
	"""docstring for Shortener"""
	# LongToShort = {}
	# ShortToLong = {}
	charPool = []
	count = 1
	host = ""
	Random = False
	max_byte = 7
	con = None
	def __init__ (self, host, r = False, useDB = False):
		"""
		type host: str
		type r : bool --> whether use random generator to generate shortenedURL
		type useDB: bool --> whether use db to store data
		"""
		if len(self.charPool) == 0:
			for c in xrange(ord('0'), ord('9')+1):
				self.charPool.append(chr(c))
			for c in xrange(ord('A'), ord('Z') + 1):
				self.charPool.append(chr(c))
			for c in xrange(ord('a'), ord('z') + 1):
				self.charPool.append(chr(c))
		self.LongToShort = LRU.LRUCache(1000)
		self.ShortToLong = LRU.LRUCache(1000)
		self.host = host
		self.Random = r
		self.useDB = useDB
		if self.Random:
			self.ceil = len(self.charPool) ** self.max_byte
			random.seed(0)
			self.visited = set()
		if self.useDB:
			try:
				self.con = lite.connect('url.db')
				self.cur = self.con.cursor()
				self.cur.executescript("""
					DROP TABLE IF EXISTS URL;
					CREATE TABLE URL (ID INT, SHORTURL TEXT, LONGURL TEXT);
					CREATE INDEX SHORTIDX ON URL(SHORTURL);
					CREATE INDEX LONGIDX ON URL(LONGURL);
					""");
				self.con.commit()

			except lite.Error, e:
				if self.con:
					self.con.rollback()
				print "Fail to connect to db"
				sys.exit(1)

	def __del__(self):
		if self.con:
			self.con.close()

	def Insert(self, longURL):
		"""
			type longURL: str
			rtypr shortenedURL: str 
		"""
		if not self.useDB:
			if not self.LongToShort.get(longURL):
				shortURL = self.GenerateShortURL(longURL)
				# self.LongToShort[longURL] = shortURL
				# self.ShortToLong[shortURL] = longURL
				self.LongToShort.set(longURL,shortURL)
				self.ShortToLong.set(shortURL,longURL)
			else:
				# shortURL = self.LongToShort[longURL]
				shortURL = self.LongToShort.get(longURL)
				self.ShortToLong.get(shortURL)
		else:
			self.cur.execute("select SHORTURL from URL where LONGURL = :longURL", {"longURL": longURL})
			data = self.cur.fetchone()
			if not data:
				shortURL = self.GenerateShortURL(longURL)
				self.cur.execute('insert into URL(SHORTURL, LONGURL) VALUES(:shortURL, :longURL )', {"shortURL": shortURL, "longURL": longURL})
				self.con.commit()
			else:
				shortURL = data
		return shortURL


		
	def GenerateShortURL(self, longURL):
		"""
			type longURL: str
			rtypr shortenedURL: str 
		"""
		shortURL = ""
		if not self.Random:
			t = self.count
			self.count += 1
		else:
			t = random.randint(0, self.ceil)
			while t in self.visited:
				t = random.randint(0, self.ceil)
			self.visited.add(t)
		while t:
			m = t % len(self.charPool)
			shortURL += self.charPool[m]
			t /= len(self.charPool)
		shortURL = 'http://' + self.host + '/' + shortURL
		return shortURL

	def GetOriginalURL(self, shortURL):
		# if shortURL in self.ShortToLong:
		# 	return self.ShortToLong[shortURL]
		# else:
		# 	return ""
		if not self.useDB:
			res = self.ShortToLong.get(shortURL)
			if res:
				self.LongToShort.get(res)
		else:
			self.cur.execute("select LONGURL FROM URL WHERE SHORTURL = :shortURL ",  {"shortURL": shortURL} )
			res = self.cur.fetchone()
		return res
	def InsertNewChar(c):
		"""
			type c: str
			rtype: void
		"""
		self.charPool.append(c)
def main():
	tiny_url = Shortener('XZ.com', True, True)
	google = 'www.google.com'
	baidu = 'www.baidu.com'
	google_short = tiny_url.Insert(google)
	baidu_short = tiny_url.Insert(baidu)
	print google_short, baidu_short
	print tiny_url.GetOriginalURL(google_short), tiny_url.GetOriginalURL(baidu_short)
if __name__ == "__main__":

	main()








