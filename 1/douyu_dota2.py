# coding:utf-8
import urllib2
import urllib
import re
from string import strip
from itertools import izip


def douyu_dota2():
    url = 'http://www.douyu.com/directory/game/DOTA2'
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    html = res.read()
    counts = re.findall(r'<span class="dy-num fr">(.*?)</span>', html)
    name1 = re.findall(r'<h3 class="ellipsis">(.*?)</h3>', html)
    user = re.findall(r'<span class="dy-name ellipsis fl">(.*?)</span>', html)
    link1 = re.findall(r'<a href="(.*?)"[\s\S]*?<span class="imgbox">', html)
    sumzhibo = []
    for name1, user, counts, link1 in izip(name1, user, counts, link1):
        temp = []
        temp.append(name1)
        temp.append(user)
        temp.append(counts)
        link1 = 'http://www.douyu.com' + link1
        temp.append(link1)
        sumzhibo.append(temp)
    for i in sumzhibo:
        for j in i:
            print j
    return sumzhibo
if __name__ == '__main__':
    name = douyu_dota2()
