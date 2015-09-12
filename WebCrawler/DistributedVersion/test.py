import sys
sys.path.append('../')
from crawler import task, TaskQueue 
from Connector import Connector
from Crawler import Crawler
from threading import BoundedSemaphore, Event

def main():
	t1 = task("http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/")
	t2 = task("http://stackoverflow.com/questions/15651128/in-this-semaphore-example-is-it-necessary-to-lock-for-refill-and-buy")
	t3 = task("http://bbs.byr.cn/")
	event = Event()
	tasks = TaskQueue(event)
	pages = TaskQueue(None)
	tasks.add(t1)
	tasks.add(t2)
	tasks.add(t3)

	taskLock = BoundedSemaphore(tasks.numOfNewTasks)
	pageLock = BoundedSemaphore(1)
	f = open("test.txt",'w')
	Connector0 = Connector(tasks,taskLock,pages,pageLock,event,'',f, 3000)
	Connector1 = Connector(tasks,taskLock,pages,pageLock,event,'',f, 3001)
	Connector0.start()
	Connector1.start()

	Crawler0 = Crawler('',3000)
	Crawler1 = Crawler('',3001)

	Crawler0.start()
	Crawler1.start()

	Connector1.join()
	Connector0.join()
	Crawler0.join()
	Crawler1.join()
	f.close()

if __name__ == "__main__":
	main()



