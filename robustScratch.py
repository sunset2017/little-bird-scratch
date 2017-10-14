'''
Created on Apr 13, 2017
@author: haopan
'''

import requests
import re
import random
import time
import urllib2
from sqlalchemy.pool import proxies

class VaryingAgent:
    def __init__(self):
        self.user_agent=[
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        ]
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        self.ipList=['223.68.1.38:8000',
                    '124.88.67.54:81',
                    '183.62.196.10:3128',
                    '120.132.71.212:80',
                    '117.158.1.210:9999',
                    '124.88.67.31:843',
                    '218.56.132.156:8080',
                    '125.217.199.148:8197',
                    '220.248.229.45:3128',
                    '202.106.16.36:3128',
                    '124.47.7.45:80',
                    '124.47.7.38:80',
                    '219.145.244.250:3128',
                    '122.226.62.90:3128',
                    '121.201.24.248:8088',
                    '60.15.8.130:3128',
                    '111.1.3.36:8000',
                    '60.191.168.181:3128',
                    '218.56.132.155:8080',
                    '123.57.58.164:80',
                    '124.88.67.32:81',
                    '120.52.21.132:8082',
                    '119.29.246.212:8888',
                    '60.191.170.148:3128',
                    '101.251.199.66:3128',
                    '116.242.227.201:3128',
                    '121.40.108.76:80',
                    '59.51.27.213:3128',
                    '123.13.204.109:9999',
                    '58.59.68.91:9797']
        #self.getAgentIp('http://www.haoip.cc/tiqu.htm')
        
    def getAgentIp(self,url):
        request=urllib2.Request(url,headers=self.hdr)
        response=urllib2.urlopen(request)
        content=response.read()
        pattern=re.compile(r'<br/>(.*?)<br/>',re.S)
        match=re.findall(pattern,content)
        if match:
            for itm in match:
                itm=itm.strip()
                print itm
                self.ipList.append(itm)
    
    def getResponse(self,url,tryTime=2,proxy=None):
        agent=random.choice(self.user_agent)
        self.hdr['User-Agent']=agent
        if proxy==None:
            try:
                #request=urllib2.Request(url,headers=self.hdr)
                #response=urllib2.urlopen(request)
                response=requests.get(url,headers=self.hdr,timeout=10)
                return response
            except:
                print 'There is problem in connecting'
                if tryTime>0:
                    print 'try again after 10s, remaining times:'+str(tryTime-1)
                    time.sleep(10)
                    return self.getResponse(url, tryTime-1)
                else:
                    print 'Have try 2 invalid times, change IP and agent'
                    time.sleep(10)
                    iP=''.join(str(random.choice(self.ipList)))
                    proxy={'http':iP}
                    tryTime=2  #Try 5 times using IP agent.
                    return self.getResponse(url, tryTime, proxy)
        
        else:
            try:
#                request=urllib2.Request(url,headers=self.hdr,proxies=proxy)
#                response=urllib2.urlopen(request)
                response=requests.get(url,headers=self.hdr,proxies=proxy,timeout=10)
                return response
            except:
                if tryTime >0:
                    print 'Agent ip is not working, try after 10s, remaining times: '+str(tryTime-1)
                    time.sleep(10)
                    iP=''.join(str(random.choice(self.ipList)))
                    proxy={'http':iP}
                    return self.getResponse(url, tryTime-1, proxy)
                else:
                    print "Agent is not useful either!, try my own ip for last time"
                    try:
#                         request=urllib2.Request(url,headers=self.hdr)
#                         response=urllib2.urlopen(request)
                        response=requests.get(url,headers=self.hdr,timeout=10)
                        return response
                    except:
                        print 'Failed, store data'
                        return None
                    
                
            
va=VaryingAgent()
'''
program running history
# now getting picture from page: 23
# new Picture saved: 163
# There is problem in connecting
# try again after 10s, remaining times:1
# There is problem in connecting
# try again after 10s, remaining times:0
# There is problem in connecting
# Have try 2 invalid times, change IP and agent
# Agent ip is not working, try after 10s, remaining times: 4
# Agent ip is not working, try after 10s, remaining times: 3
# Agent ip is not working, try after 10s, remaining times: 2
# Agent ip is not working, try after 10s, remaining times: 1
# Agent ip is not working, try after 10s, remaining times: 0
# Agent is not useful either!, try my own ip for last time
# Failed, store data
# store picture failed
# store history
# now getting picture from page: 24
'''
# new Picture saved: 165