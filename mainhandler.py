import hashlib
import tornado.web
import os
import config
import xml.etree.ElementTree as ET
import time
import template
from accesstoken import AccessToken
from database import DBsession, DownloadTask
from createdir import MakeDir


#loghandle = LogHandle("MainHandler", "./logs/wechat.log")

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        try:
            signature = self.get_argument('signature')
            timestamp = self.get_argument('timestamp')
            nonce = self.get_argument('nonce')
            echostr = self.get_argument('echostr')
            result = self.check_signature(signature, timestamp, nonce)
            if result:
                self.write(echostr)
                #loghandle.write_log("微信sign校验,返回echostr="+echostr)
            else:
                #loghandle.write_log("微信sign校验,校验失败")
                pass
        except Exception as e:
            #loghandle.write_log("微信sign校验,---Exception:"+str(e))
            pass

    def check_signature(self, signature, timestamp, nonce):
        token = config.WXTOKEN 
        L = [timestamp, nonce, token]
        L.sort()
        s = L[0] + L[1] + L[2]
        sha1 = hashlib.sha1(s.encode('utf-8')).hexdigest()
        #loghandle.write_log("sha1="+sha1+"&signature="+signature)
        return sha1 == signature

    def post(self):
        #render = web.template.render("./templates")
        body = self.request.body
        #loghandle.write_log('[微信消息回复中心]收到用户消息:' + str(body))
        session = DBsession()
        dirhandle = MakeDir()
        data = ET.fromstring(body)
        ToUserName = data.find('ToUserName').text
        FromUserName = data.find('FromUserName').text
        MsgType = data.find('MsgType').text
        if MsgType == "event":
            try:
                Event = data.find('Event').text

            except :
                pass
        elif MsgType == "text":
            content = data.find("Content").text
            print(content)
            openid = ToUserName
            url = dirhandle.gen_url()
            code = dirhandle.gen_extract_code()
            dirname = dirhandle.gen_dir()
            task = DownloadTask(openid=openid, downloadurl=content, getcode=code, geturl=url, dirname=dirname)
            session.add_all([task])
            session.commit()
            session.close()
            
            #token = AccessToken().get_accesstoen()
            #print(token)
            text = "您的下载请求已经收到!\n下载网址:%s\n提取码:%s"%("www.taoquansousou.cn/s/"+url,code)
            out = template.TEXTTPL%(FromUserName, ToUserName, int(time.time()), "text", text)
            self.write(out)
        elif MsgType == "image":
            picurl = data.find("PicUrl").text
            #mediaid = data.find("MediaId").text
            imghandle.download_image(picurl, config.IMAGEPATH+"/a.jpg")
            mediaid = imghandle.send_wx_image("")
            print(mediaid)
            out = template.IMAGETPL%(FromUserName,ToUserName, int(time.time()), mediaid)
            self.write(out)
        else:
            #loghandle.write_log("No recognize msgtype!")
            pass


