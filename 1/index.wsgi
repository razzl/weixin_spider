#coding: UTF-8
# //                            _ooOoo_  
# //                           o8888888o  
# //                           88" . "88  
# //                           (| -_- |)  
# //                            O\ = /O  
# //                        ____/`---'\____  
# //                      .   ' \\| |// `.  
# //                       / \\||| : |||// \  
# //                     / _||||| -:- |||||- \  
# //                       | | \\\ - /// | |  
# //                     | \_| ''\---/'' | |  
# //                      \ .-\__ `-` ___/-. /  
# //                   ___`. .' /--.--\ `. . __  
# //                ."" '< `.___\_<|>_/___.' >'"".  
# //               | | : `- \`.;`\ _ /`;.`/ - ` : | |  
# //                 \ \ `-. \_ __\ /__ _/ .-` / /  
# //         ======`-.____`-.___\_____/___.-`____.-'======  
# //                            `=---='  
# //  
# //         .............................................  
# //                  佛祖保佑             永无BUG 

import os 
import sae
import web
import model
import urllib2
import json
import douyu_dota2
import zhanqi_dota2
import huomao_dota2
import huya_dota2
import getip
# from sae.storage import Bucket
from itertools import izip
#index.wsgi 是sae的python 入口地址
from weixinInterface import WeixinInterface
urls = (
	'/weixin','WeixinInterface',
	'/ck','feedback',
#	'/creat','createmenu',
#	'/delete','deletemenu',
	# '/t','t',
	'/test','test',
	'/sk','showtv',
	)

app_root = os.path.dirname(__file__)#显示当前的文件路径
templates_root = os.path.join(app_root,'templates')#将templates 加入 形成新的路径
render = web.template.render(templates_root)

class feedback:
	def GET(self):
		fkcon = model.get_fkcontent()
		return render.checkfk(fkcon)
class showtv:
	def GET(self):
		douyuzhibo = douyu_dota2.douyu_dota2()
		zhanqizhibo = zhanqi_dota2.zhanqi_dota2()
		huomaozhibo = huomao_dota2.huomao_dota2()
		huyazhibo = huya_dota2.huya_dota2()
		# sumzhibo = []
		# for name,user,counts in izip(allzhibo[0],allzhibo[1],allzhibo[2]):
		# 	temp = []
		# 	temp.append(name)
		# 	temp.append(user)
		# 	temp.append(counts)
		# 	sumzhibo.append(temp)
		return render.showzhibo(douyuzhibo,zhanqizhibo,huomaozhibo,huyazhibo)
class test:
	def GET(self):
		#model.delete_all_ip()
		#getip.getip()
		return 'ceshi yi xia'
# class t:
# 	def GET(self):
# 		model.delip(str({'http':'http://124.202.181.230:8118'}))
# 		ip = model.get_ip()
# 		return ip[0]
'''
class createmenu:
	def GET(self):
		APPID = 'wx9885de2680cdc51f'
		APPSECRET = 'b1cc239cc39d84073f3684944256374f'
		url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+APPID+'&secret='+APPSECRET
		response = urllib2.urlopen(url)
		html = response.read()
		tokeninfo = json.loads(html)
		access_token = tokeninfo['access_token']
		post = {"button":
		[
					{"name": u"会员服务",
						"sub_button":[
								{"type":"click","name":u"健康咨询","key":"JKZX"},
									]
					},
					{"name":u"申请加入",
					"sub_button":[
							{"type":"view","name":u"企业入会申请","url": ""},
									]
						},
					{"type":"view","name":u"关于","url":""}
						
		]
	}	

		url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+access_token
		req = urllib2.Request(url)
		data = json.dumps(post, ensure_ascii=False).encode('utf-8')
		req.add_header('Content-Type', 'application/json')
		req.add_header('encoding', 'utf-8') 
		response = urllib2.urlopen(req, data)  
		result = response.read()
		print result
		return result
class deletemenu:
	def GET(self):
		APPID = 'wx9885de2680cdc51f'
		APPSECRET = 'b1cc239cc39d84073f3684944256374f'
		url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid='+APPID+'&secret='+APPSECRET
		response = urllib2.urlopen(url)
		html = response.read()
		tokeninfo = json.loads(html)
		access_token = tokeninfo['access_token']
		url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='+access_token
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		return response
'''

app = web.application(urls,globals()).wsgifunc()#创建一个web应用，urls是网站url与执行函数（处理类）的名称的映射，global()包含当前空间的所有变量 类等
application = sae.create_wsgi_app(app)