# _*_ coding:utf-8 _*_
import web
import web.db
import sae.const


db = web.database(
	dbn='mysql',
	host=sae.const.MYSQL_HOST,
	port=int(sae.const.MYSQL_PORT),
	user=sae.const.MYSQL_USER,
	passwd=sae.const.MYSQL_PASS,
	db=sae.const.MYSQL_DB
)  # 利用web的database连接到sae的mysql


def addfk(username, fktime, fkcontent):  # 增加一个留言
	return db.insert('fk', user=username, time=fktime, fk_content=fkcontent)


def get_fkcontent():  # 得到所有的留言
	return db.select('fk', order='id')


def addip(addip):  # 增加一个代理IP
	return db.insert('dailiip',ip=addip)


def delip(deip):  # 删除一个代理IP
	return db.delete('dailiip', where='ip = $deip', vars=locals())


def get_ip():  # 得到所有的代理IP
	return db.query("SELECT * FROM dailiip")


def delete_all_ip():
	return db.query("DELETE FROM dailiip")
