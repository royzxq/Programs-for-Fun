import pymongo
import csv
client = pymongo.MongoClient("mongodb://royzxq:leetcode@ds027489.mongolab.com:27489/leetcode")
db = client['leetcode']
collection = db['question_collection']

edgePair = list(list())
for question in collection.find():
	source = question['title']
	for target in question['related']:
		edge = [source, target]
		edgePair.append(edge)
	if not question['related']:
		edge = [source,source]
		edgePair.append(edge)

out = open('edge.csv','w')
a = csv.writer(out)
a.writerows(edgePair)
out.close()
# if test:
# 	collection.update_one({"title":title}, {"$set":{"content":"change content"}})
# else:
# 	collection.insert({"title":title,"content":"new content"})

client.close()