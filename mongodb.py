import pymongo
import logging
from e04dao import Save
'''
singleton裝飾器
利用python decorator修飾db class
達到singleton design pattern的效果
'''
def singletonDecorator(cls,*args,**kwargs):
	instance = {}
	def wrapperSingleton(*args,**kwargs):
		if cls not in instance:
			instance[cls] = cls(*args,**kwargs)
			logging.info('new instance')
		return instance[cls]
	return wrapperSingleton

@singletonDecorator
class database(Save):
	def __init__(self):
		self.__connection = pymongo.MongoClient("localhost",27017)
		self.__db = self.__connection.e04
	def _Save__isExist(self,name):
		return True
	def _Save__createTable(self,name):
		return True
	def insert(self,item):
		if not self._Save__deDuplicate(item):
			collections = self.__db[item['category']]
			collections.insert(item.toDict())
			logging.info("Mongo : insert data success")
			return True
		return False
	def _Save__deDuplicate(self,item):
		collections = self.__db[item['category']]
		result = collections.find_one({'name':item['name']})
		if result:
			return True
		return False
	def close(self):
		self.__connection.close()
