from crawler import task, TaskQueue, Crawler
from multiprocess import Process, Event, Queue


def main():
	t1 = task("http://www.laurentluce.com/posts/python-threads-synchronization-locks-rlocks-semaphores-conditions-events-and-queues/")
	t2 = task("http://stackoverflow.com/questions/15651128/in-this-semaphore-example-is-it-necessary-to-lock-for-refill-and-buy")
	t3 = task("http://bbs.byr.cn/")
	event = Event()
	tasks = Queue()
	pages = Queue()
	tasks.put(t1)
	tasks.put(t2)
	tasks.put(t3)

	f = open("test.txt",'a')

	Crawler1 = Crawler(tasks,pages,event,f)
	Crawler2 = Crawler(tasks,pages,event,f)
	Crawler1.start()
	Crawler2.start()
	Crawler1.join()
	Crawler2.join()
	f.close()
if __name__ == "__main__":
	main()
