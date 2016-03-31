# coding:utf-8
import urllib2
import urllib
import re
from string import strip
from itertools import izip


def huomao_dota2():
    url = 'http://www.huomaotv.cn/channel/dota2'
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    html = res.read()
    html = re.sub(r'主播正在休息[\s\S]*', '', html)
    name1 = re.findall(r'<h4>(.*?)</h4>[\s\S]+?<p>', html)
    user = re.findall(r'<span class="username">(.*?)</span>', html)
    counts = re.findall(r'<span class="view">(.*?)</span>', html)
    link1 = re.findall(r'<a href="(.*?)" class="play_btn">', html)
    sumzhibo = []
    for name1, user, counts, link1 in izip(name1, user, counts, link1):
        temp = []
        temp.append(name)
        temp.append(user)
        temp.append(counts)
        link1 = 'http://www.huomaotv.com' + link1
        temp.append(link1)
        sumzhibo.append(temp)
    for i in sumzhibo:
        for j in i:
            print j
    return sumzhibo
if __name__ == '__main__':
    name = humao_dota2()

