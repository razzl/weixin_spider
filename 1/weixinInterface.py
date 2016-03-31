# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import random
import urllib2,json
import pylibmc
import re
import model
import dotamax
import douyu_dota2
from lxml import etree

class WeixinInterface:
	def __init__(self):
		self.app_root = os.path.dirname(__file__)
		self.templates_root = os.path.join(self.app_root,'templates')#拼出当前目录下的模板路径
		self.render = web.template.render(self.templates_root)#调用web.py 的template 引用模板
	def GET(self):#用来调用微信的接口
		#获取输入的参数
		data = web.input()
		signature = data.signature#根据微信的官方文档 进行调用
		timestamp = data.timestamp
		nonce = data.nonce
		echostr = data.echostr
		#自己的token
		token = "razzl7"
		#字典排序
		list = [token,timestamp,nonce]
		list.sort()
		sha1 = hashlib.sha1()
		map(sha1.update,list)
		hashcode = sha1.hexdigest()
		#sha1 加密算法

		#如果是来自微信的请求，则回复echoster
		if hashcode == signature:
			return echostr
	def POST(self):
		
		str_xml = web.data() #获得post来的数据
		xml = etree.fromstring(str_xml)#进行XML解析
		#content=xml.find("Content").text#获得用户所输入的内容
		msgType=xml.find("MsgType").text
		fromUser=xml.find("FromUserName").text
		toUser=xml.find("ToUserName").text

		mc = pylibmc.Client()#初始化一个memecache的实例保存用户的状态
	
		if msgType == 'event':#根据消息的类型进行判断 是否发生了关注或者取消关注
			mscontent = xml.find("Event").text#如果是事件的话 会存在Event这个值 通过判断Event的值来做出响应
			if mscontent == "subscribe":
				replyText = u"1.输入id或昵称查询dota2战绩\n2.输入d查看所有dota2直播\n3.输入razzl 福利\n4.输入fk+留言" 
				return self.render.reply_text(fromUser,toUser,int(time.time()),replyText)
			if mscontent == "unsubscribe":
					replayText = u'再见= ='
					return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)
		if msgType == 'text':#如果没有事件的发生 就是文本的内容 判断是否发送了m
			content=xml.find("Content").text
			if content.startswith('fk'):
				fktime = time.strftime('%Y-%m-%d %H:%M',time.localtime())
				model.addfk(fromUser,fktime,content[3:].encode('utf-8'))
				return self.render.reply_text(fromUser,toUser,int(time.time()),u'你丫的有个蛋的意见')
			if content.lower()=='bye':
				mc.delete(fromUser+'_razzl')
				return self.render.reply_text(fromUser,toUser,int(time.time()),u'滚！')
			if content.lower()=='razzl':
				mc.set(fromUser+'_razzl','razzl')
				return self.render.reply_text(fromUser,toUser,int(time.time()),u'I am coming!<===========')
			if content.lower() == 'd':

				# name = douyu_dota2.douyu_dota2()
				# reply_text = ''
				# for n in name:
				# 	reply_text +=n[0].decode('utf-8')
				# 	reply_text +=n[1].decode('utf-8')
				# 	reply_text +=n[2].decode('utf-8')
				return self.render.reply_pic(fromUser,toUser,int(time.time()),title=u'dota2直播查询',description = u'douyu直播',picurl ='http://img1.cache.netease.com/catchpic/1/13/1315E9394978B55D884EFE8F8A07CBDD.jpg',url ='http://razzl2.sinaapp.com/sk')

				# name = douyu_dota2.douyu_dota2()
				# reply_text = ''
				# for n in name:
				# 	reply_text +=n[0].decode('utf-8')
				# 	reply_text +=n[1].decode('utf-8')
				# 	reply_text +=n[2].decode('utf-8')
				# return self.render.reply_pic(fromUser,toUser,int(time.time()),'douyu信息查询','dota2','http://img1.cache.netease.com/catchpic/1/13/1315E9394978B55D884EFE8F8A07CBDD.jpg','http://dotamax.com/')
			mcrazzl = mc.get(fromUser+'_razzl')
			if mcrazzl == 'razzl':
				res = xiaohuangji(content)
				return self.render.reply_text(fromUser,toUser,int(time.time()),res)
			# if content.lower() == 'm':
			# 	musicList = [
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/destiny.mp3','Destiny',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/5days.mp3','5 Days',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/Far%20Away%20%28Album%20Version%29.mp3','Far Away (Album Version)',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/%E5%B0%91%E5%B9%B4%E6%B8%B8.mp3',u'少年游',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/%E8%8F%8A.mp3',u'菊--关喆',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/%E7%A6%BB%E4%B8%8D%E5%BC%80%E4%BD%A0.mp3',u'离不开你',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/%E9%99%8C%E7%94%9F%E4%BA%BA.mp3',u'陌生人',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/%E8%8A%B1%E5%AE%B9%E7%98%A6.mp3',u'花容瘦',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/%E4%B9%98%E5%AE%A2.mp3',u'乘客',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/If%20My%20Heart%20Was%20A%20House.mp3',u'If My Heart Was A House',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/Hello%20Seattle%EF%BC%88Remix%E7%89%88%EF%BC%89.mp3',u'Hello Seattle（Remix版',u'razzl7'],
			# 		[r'http://bcs.duapp.com/yangyanxingblog3/music/Everybody%20Hurts.mp3',u'Everybody Hurts',u'razzl7']
			# 	]#
			# 	music = random.choice(musicList)
			# 	musicurl = music[0]
			# 	musictitle = music[1]
			# 	musicdes = music[2]
			# 	return self.render.reply_music(fromUser,toUser,int(time.time()),musictitle,musicdes,musicurl)

			if content == 'help':
				replayText = u'''1.输入id或昵称查询dota2战绩\n2.输入d查看所有dota2直播\n3.输入razzl 福利\n4.输入fk+留言'''
				return self.render.reply_text(fromUser,toUser,int(time.time()),replayText)


			elif type(content).__name__ == 'unicode':
				content = content.encode('utf-8')
			Nword = dotamax.dotamax(content)
			if Nword == False:
				reply_text = '无法找到我的Dota2数据'
				return self.render.reply_text(fromUser,toUser,int(time.time()),reply_text)
			else:
				length = len(Nword)
				return self.render.showdotamax(fromUser,toUser,int(time.time()),Nword,length)
			#return self.render.reply_text(fromUser,toUser,int(time.time()),'11111')
			#return self.render.reply_pic(fromUser,toUser,int(time.time()),title=u'dotamax查询',description = u'点击图片查看更多',picurl ='http://img1.cache.netease.com/catchpic/1/13/1315E9394978B55D884EFE8F8A07CBDD.jpg',url ='http://dotamax.com/search/?q='+content)

def youdao(word):
	qword = urllib2.quote(word)
	baseurl = r'http://fanyi.youdao.com/openapi.do?keyfrom=razzl2&key=937907403&type=data&doctype=json&version=1.1&q='
	url = baseurl+qword
	resp = urllib2.urlopen(url)
	fanyi = json.loads(resp.read())
	#根据json是否返回一个basic的key来判断是否翻译成功
	if fanyi['errorCode'] == 0:
		if 'basic' in fanyi.keys():
			trans = u'%s:\n%s\n%s\n网络释义：\n%s'%(fanyi['query'],''.join(fanyi['translation']),''.join(fanyi['basic']['explains']),''.join(fanyi['web'][0]['value']))
			return trans
		else:
			trans =u'%s:\n基本翻译:%s\n'%(fanyi['query'],''.join(fanyi['translation']))
			return trans
	else:
		return u'您输入的单词遇不可抗力无法翻译'


def xiaohuangji(ask):#加入小黄鸡的功能
	key = '487d7f34be5f45ec2d01fe0b39c6ae7a'
	api = 'http://www.tuling123.com/openapi/api?'
	uask = ask.encode('utf-8')#输进来的字符需要utf-8的编码
	url = api+'key='+key+'&'+'info='+uask
	res = urllib2.urlopen(url).read()
	resp = json.loads(res)['text']#图灵机器人返回的是json格式的数据
	return resp
