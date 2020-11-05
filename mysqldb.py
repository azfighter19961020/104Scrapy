import pymysql
import logging
from e04dao import Save
'''
singleton裝飾器
利用[python decorator]修飾db class
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
		config = {
			'host':'127.0.0.1',
			'port':3306,
			'user':'root',
			'password':'charlie11438',
			'db':'e04',
		}
		self.__connection = pymysql.connect(**config)

	def _Save__isExist(self,name):
		with self.__connection.cursor() as cursor:
			cursor.execute('show tables;')
			result = cursor.fetchall()
			if [i for i in result if name in i]:
				return True
			return False
	def _Save__createTable(self,name):
		with self.__connection.cursor() as cursor:
			sql = "create table %s(jobname varchar(255),jobLink varchar(255),company varchar(255),companyAddress varchar(255),companyLink varchar(255),jobArea varchar(255),experience varchar(255),school varchar(255),description varchar(255),salary varchar(255));" % name
			try:
				cursor.execute(sql)
			except Exception as e:
				logging.info(e)
				self.__connection.rollback()
				return False
			else:
				logging.info("create table %s success"%name)
				self.__connection.commit()
				return True
	def insert(self,item):
		if not self._Save__isExist(item['category']):
			result = self._Save__createTable(item['category'])
			if not result:
				return False
		with self.__connection.cursor() as cursor:
			if self._Save__deDuplicate(item):
				return False
			sql = 'insert into %s values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (item['category'],item['name'],item['jobLink'],item['company'],item['companyAddress'],item['companyLink'],item['jobArea'],item['experience'],item['school'],item['description'],item['salary'])
			try:
				cursor.execute(sql)
			except Exception as e:
				logging.info(e)
				self.__connection.rollback()
				return False
			else:
				logging.info("insert data %s success"%item['name'])
				self.__connection.commit()
				return True
	def _Save__deDuplicate(self,item):
		with self.__connection.cursor() as cursor:
			cursor.execute('select * from %s where jobname="%s"'%(item['category'],item['name']))
			result = cursor.fetchall()
			if [i for i in result if item['name'] in i]:
				return True
			return False
	def close(self):
		self.__connection.close()

