# coding:utf-8
import urllib2
import urllib
import re
from string import strip
from itertools import izip


def huya_dota2():
	url = 'http://www.huya.com/g/dota2'
	req = urllib2.Request(url)
	res = urllib2.urlopen(req)
	html = res.read()
	name1 = re.findall(r'<a href="[\s\S]*?" class="clickstat" eid="click/gamelist/card/dota2"[\s\S]*?2">(.*?)</a>', html)
	user = re.findall(r'<i class="nick" title="(.*?)">', html)
	counts = re.findall(r'<i class="js-num">(.*?)</i>', html)
	link1 = re.findall(r'<a href="(.*?)" class="clickstat" eid="click/gamelist/card/dota2"', html)
	sumzhibo = []
	for name1, user, counts, link1 in izip(name1, user, counts, link1):
		temp = []
		# name = name.replace('&nbsp', ' ').decode('utf-8')
		temp.append(name1)
		temp.append(user)
		temp.append(counts)
		temp.append(link1)
		sumzhibo.append(temp)
	for i in sumzhibo:
		for j in i:
			print j
	return sumzhibo
if __name__ == '__main__':
	name = huya_dota2()
