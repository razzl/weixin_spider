# -*- coding: UTF-8 -*-
import urllib2
import urllib
import re
import model


def getip():
	url = 'http://www.xicidaili.com/nt/'
	# 从当前的网址中获取代理IP
	headers = {'User-Agent': ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'}
	req = urllib2.Request(url=url, headers=headers)
	res = urllib2.urlopen(req)
	html = res.read()
	ip = re.findall(r'<td><img src="http://fs\.xicidaili\.com/images/flag/cn\.png" alt="Cn" /></td>[\s\S]*?<td>(.*?)</td>[\s\S]*?<td>(.*?)</td>[\s\S]*?<td>透明</td>[\s\S]*?<td>(.*?)</td>', html)  # 注意.是需要转义的
	daili = []
	for item in ip:
		s = item[2].lower()+'://'+item[0]+':'+item[1]
		daili.append({item[2].lower(): s})
	durl = 'http://dotamax.com/search/?q=lalalalal'
	for item in daili:
		proxy_support = urllib2.ProxyHandler(item)
		opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		try:
			opener.open(durl, timeout=3)
			model.addip(str(item))  # 依次增加代理IP，注意参数的传入，dict不接受，先变成str型
		except:
			continue
