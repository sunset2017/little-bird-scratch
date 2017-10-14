# -*- coding:gb2312 -*-
import re
import os
import requests
from bs4 import BeautifulSoup
import urllib2
import uuid
import time
import sets
from robustScratch import va

class GetImage:
    def __init__(self):
        #self.entrance=entranceURL
        self.count=0
        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
        self.urlList=[]
        self.set=sets.Set()
    def getResponse(self,url):
        #request=urllib2.Request(url,headers=self.hdr)
        #response=urllib2.urlopen(request)
        response=va.getResponse(url)
        return response
    
    
    def getAllUrl(self,url):
        #pattern=re.compile(r'alt=\"(.*?)" height',re.S)
        response=self.getResponse(url)
        if response==None:
            self.storeData()
            return
        #content=response.read()
        content=response.text
        soup=BeautifulSoup(content,'lxml',from_encoding='gb18030')
        aList=soup.find('div',class_='picnew clearfix')
        if aList:
            aList=aList.find_all('a')
            for itm in aList:
                #match=re.search(pattern,str(itm))
                nextUrl=itm['href']
                if nextUrl in self.set:
                    continue
                else:
                    self.urlList.append(nextUrl)
                    self.set.add(nextUrl)
                print 'new Picture url found, remaining url: '+str(len(self.urlList))
                self.getPicture(nextUrl,'MMeizitu')
    
    def getPicture(self,url,title): 
        #analysis of the pictures under this url.
        response=self.getResponse(url)
        if response == None:
            self.storeData()
            return
        
        #content=response.read()
        content=response.text
        soup=BeautifulSoup(content,'lxml')
        os.chdir('/Users/haopan/Desktop/mizitu/mizitu3')
        allP=soup.find('div',id='picture')
        if allP:
            allP=allP.find_all('img')
            for itm in allP:
                pictureUrl=itm['src']
                #self.urlList.append(pictureUrl)
                print 'new url added: '+pictureUrl
                if pictureUrl[-3:] == 'gif':
                    continue
                img_html=self.getResponse(pictureUrl)
                if img_html==None:
                    self.storeData()
                    return
                name=title+str(self.count)
                f=open(name+'.jpg','ab')
                #f.write(img_html.read())
                #f.write(img_html.text)
                f.write(img_html.content)
                print 'new Picture saved: '+str(self.count)
                f.close()
                self.count+=1
                time.sleep(1)
     
    def runCatch(self,baseUrl=None):
        num=2000
        if baseUrl!=None:
            self.urlList.append(baseUrl)
        while(len(self.urlList)>0):
            url=self.urlList[0]
            self.urlList.remove(url)
            self.getAllUrl(url)
            if(self.count > num):
                break
            if self.count%50==0:
                print 'sleep a little bit'
                time.sleep(60)
                
    def storeData(self):
        print 'Here in store url data'
        f=open('hellofile.txt','w')
        g=open('visitedList.txt','w')
        for itm in self.urlList:
            f.write(itm+'\n')
        for itm in self.set:
            g.write(itm+'\n')
        f.write('the current index is: '+str(self.count))
        g.close()
        f.close()
        print 'data storation completed'
    
    def resumeLast(self):
        os.chdir('/Users/haopan/Desktop/mizitu/mizitu3')
        f=open('hellofile.txt','r')
        g=open('visitedList.txt','r')
        for lines in f:
            self.urlList.append(lines.strip())
        for lines in g:
            self.set.add(lines.strip())
        g.close()
        f.close()
        self.count=159
        self.runCatch()
        
        
gi=GetImage()
gi.runCatch('http://www.meizitu.com/tag/suxiong_17_1.html')
#gi.resumeLast()