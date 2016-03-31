# coding:utf-8
import urllib2
import urllib
import re
from itertools import izip
import os
# import model


os.environ['disable_fetchurl'] = "1"  # 关闭sae内置的fetchURL的功能，是dotamax不以sae的IP地址出口


def dotamax(content):
	url = 'http://dotamax.com/search/?q='
	qurl = url + content
	headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
	ips = model.get_ip()  # 从数据库里得到所有的代理ip地址
	if not ips:  # 如果数据库里没有代理IP了
		html = urllib2.urlopen('http://razzl2.sinaapp.com/test').read()  # 就重新获取代理IP
		ips = model.get_ip()#
	for ip in ips:  # 依次遍历所有代理IP，选择可用的，不可用的从数据库中删除
		proxy_support = urllib2.ProxyHandler(ip)
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		req = urllib2.Request(url=qurl, headers=headers)
		try:
			res = opener.open(req)
			break
		except:
			model.delip(ip)
			continue
	html = res.read()
	flag_one = re.findall(r'无法找到我的Dota2数据',html)
	flag_two = re.findall(r'如果因为中途关闭共享而缺少数据', html)
	sumdota = []
	if flag_one:  # 如果无法找到就返回false
		return False

	if flag_two:  # 如果只有一个数据，直接显示
		userid = re.findall(r'<a href="/verify_data/\?acc=(.*?)">', html)  # 注意？是需要转义的
		img = re.findall(r'class="circle-img"><img src="(.*?)" style=', html)
		username = re.findall(r'title:"(.*?) －dotamax.com"', html)
		player = 'http://dotamax.com/player/detail/'+userid[0]
		for img, username, userid in izip(img, username, userid):  # 利用izip的同时迭代的特性
			temp = []
			temp.append(img)
			temp.append(username)
			temp.append(userid)
			temp.append(player)
			sumdota.append(temp)
		return sumdota
	# 如果有多个数据，就采用下列的正则表达式对数据进行提取
	img = re.findall(r'<img class="hero-img-list" src="(.*?)">', html)
	username = re.findall(r'</img> (.*?) <div style="float:', html)
	userid = re.findall(r' <div style="float: right;line-height: 28px;"> (.*?) </div>', html)
	player = re.findall(r'<td onclick="DoNav\(\'(.*?)\'\)"', html)
	for img, username, userid, player in izip(img, username, userid, player):
		temp = []
		temp.append(img)
		temp.append(username)
		temp.append(userid)
		link ='http://dotamax.com'+player
		temp.append(link)
		sumdota.append(temp)
	if len(sumdota) >= 6:  # 如果数据过多，就只显示一部分
		return sumdota[0:5]
	else:
		return sumdota
if __name__ == '__main__':
	dota = dotamax('lalalalal')
