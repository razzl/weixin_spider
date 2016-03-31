# coding:utf-8
import urllib2
import re
from string import strip
from itertools import izip


def zhanqi_dota2():
    url = 'http://www.zhanqi.tv/games/dota2'
    req = urllib2.Request(url)
    res = urllib2.urlopen(req)
    html = res.read().decode('utf-8')
    html = re.sub(r'<script[\s\S]*?</script>', '', html)
    html = re.sub(r'<div class="list-loading hidden"><i class="loading"></i></div>[\s\S]*', '', html)
    name1 = re.findall(r'<span class="name">(.*?)</span>', html)
    user = re.findall(r'<i class="icon-eye dv">[\s\S]*?<span class="dv">(.*?)</span>', html)
    counts = re.findall(r'<span class="anchor anchor-to-cut dv">(.*?)</span>', html)
    link1 = re.findall(r'<a href="(.*?)" class="js-jump-link">', html)
    sumzhibo = []
    for name1, user, counts, link1 in izip(name1, user, counts, link1):
        temp = []
        temp.append(strip(name1))
        temp.append(strip(user))
        temp.append(counts)
        link1 = 'http://www.zhanqi.tv' + link1
        temp.append(link1)
        sumzhibo.append(temp)
    return sumzhibo

if __name__ == '__main__':
    name = zhanqi_dota2()
