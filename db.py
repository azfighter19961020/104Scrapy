import pymysql
import logging
class database:
	def __init__(self):
		config = {
			'host':'127.0.0.1',
			'port':3306,
			'user':'root',
			'password':'charlie11438',
			'db':'e04',
		}
		self.__connection = pymysql.connect(**config)
	def __isExist(self,name):
		with self.__connection.cursor() as cursor:
			cursor.execute('show tables;')
			result = cursor.fetchall()
			if [i for i in result if name in i]:
				return True
			return False
	def __createTable(self,name):
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
		if not self.__isExist(item['category']):
			result = self.__createTable(item['category'])
			if not result:
				return False
		with self.__connection.cursor() as cursor:
			if self.__deDuplicate(item):
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
	def __deDuplicate(self,item):
		with self.__connection.cursor() as cursor:
			cursor.execute('select * from %s where jobname="%s"'%(item['category'],item['name']))
			result = cursor.fetchall()
			if [i for i in result if item['name'] in i]:
				return True
			return False

