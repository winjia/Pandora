from selenium import webdriver
import os
import time
import requests
import threading
import random
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, Time
from datetime import datetime

#engine = create_engine('mysql+mysqldb://root:123456@localhost:3306/taoqueqiao',encoding='UTF-8', echo=True)
engine = create_engine('mysql+mysqlconnector://root:123123@localhost:3306/taoqueqiao',encoding='UTF-8', echo=True)

Base = declarative_base()


class DownloadTask(Base):
    __tablename__ = 'download_task'
    id = Column(Integer, primary_key=True)
    openid = Column(String(128), nullable=False, index=True)
    downloadurl = Column(String(256), nullable=False)
    getcode = Column(String(64), nullable=False, index=True)
    geturl = Column(String(256), nullable=False)
    isdownload = Column(Boolean, default=False)
    isfinish = Column(Boolean, default=False)
    isdelete = Column(Boolean, default=False)
    createtime = Column(Time, default=datetime.time)
    updatetime = Column(Time, default=datetime.time)


def check(filepath):
    print("check")
    global timer
    files = os.listdir(filepath)
    n = 0
    for f in files:
        if f[0]==".":
            continue
        if f.endswith("crdownload") == True:
            print("no finish")
            break
        if f.endswith("rar") == True:
            n += 1
            break
        if f.endswith("pdf") == True:
            n += 1
            break
        if f.endswith("txt") == True:
            n += 1
            break
    if n!=0:
        timer.cancel()
        return
    timer = threading.Timer(5, check, [filepath])
    timer.start()


def checkfile(filepath):
    global timer
    timer = threading.Timer(5, check, [filepath])
    timer.start()

class DriverBuilder():
    def enable_download_in_headless_chrome(self, driver, download_dir):
        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
        command_result = driver.execute("send_command", params)

class FileDownload():
    def __init__(self, downloadpath):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': downloadpath}
        options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(chrome_options=options)
        self.user_login()

    def user_login(self):
        url = "https://passport.csdn.net/account/login"
        self.driver.get(url)
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div/h3/a").click()
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[@id="username"]').send_keys("peter_wjj")
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys("Gz^3AEI7ug1")
        self.driver.find_element_by_xpath('//*[@id="fm1"]/input[8]').click()

    def download_file(self, url):
        print("download...")
        DriverBuilder().enable_download_in_headless_chrome(self.driver, "/Users/wangjj/Documents/code/python/spider/tmp")
        self.driver.get(url)
        self.driver.find_element_by_xpath('//*[@id="download_top"]/div[4]/a[2]').click()
        self.driver.find_element_by_id("vip_btn").click()
        print("finish")
        #start file check

        

    



        


if __name__=="__main__":
    url = "https://download.csdn.net/download/zhilong2276/10593952"
    url = "https://download.csdn.net/download/qq_36973081/10599989"
    Base.metadata.create_all(engine)
    #handle = FileDownload("/Users/wangjj/Documents/code/python/spider/tmp")
    #handle.download_file(url) 
    #checkfile("/Users/wangjj/Documents/code/python/spider/tmp")
    '''
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '/Users/wangjj/Documents/code/python/spider'}
    options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=options)
    user_login(driver)
    driver.get(url)
    '''
    #driver.find_element_by_class_name("direct_download").click()
    #driver.find_element_by_class_name("direct_download vip_download vip_down").click()
    #driver.find_element_by_xpath('//*[@id="download_top"]/div[4]/a[2]').click()
    #print(driver.window_handles)
    #print(driver.current_window_handle)
    #res = driver.find_element_by_xpath('//*[@id="vip_btn"]/a[0]')
    #DriverBuilder().enable_download_in_headless_chrome(driver, "/Users/wangjj/Documents/code/python/spider/tmp")
    #driver.find_element_by_id("vip_btn").click()
    #res = driver.find_element_by_id("vip_btn")
