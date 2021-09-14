# -*- coding: utf8 -*-

import os
#os.environ["http_proxy"] = "http://127.0.0.1:8081"
#os.environ["https_proxy"] = "http://127.0.0.1:8081"

import logging
logger = logging.getLogger()

logging.basicConfig(level=logging.INFO)

import json
import requests
import random

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def test_url(token):
    logger.info("健康打卡"+token)
    url = 'https://student.wozaixiaoyuan.com/health/save.json'
    headers = GetHeaders(token)
    data = {'answers': '["0","1","36.5"]',
    #此处需要将位置信息改为自己的
     'latitude': str(round(random.uniform(XX.XXXX,XX.XXXX),5)), #经纬度，随机在某个正方形区域内取点
     'longitude': str(round(random.uniform(XXX.XXXX,XXX.XXXX),5)),
     'country': '中国',
     'city': 'XX市',
     'district': 'XX区',
     'province': 'XX省',
     'township': 'XX街道',
     'street': 'XX街',
     'areacode': 'XXXXXX'}
    try:
        r = requests.post(url, data = data, headers = headers, verify = False).json()
        logger.debug(r)
    except Exception as e:
        logger.error('Error:'+str(e))
    if r["code"] != 0:
        logger.error("打卡失败:"+str(r["code"]))
        return
    logger.info("打卡成功")
    return

def GetHeaders(token, type="application/x-www-form-urlencoded"):
    headers = {'Cookie': "",
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    'content-type': type,
    'Referer': "https://servicewechat.com/wxce6d08f781975d91/172/page-frame.html",
    'Accept-Encoding': "gzip, deflate",
    'token': token
    }
    return headers

def DoSign(id,signid,token):
    logger.info("正在签到:"+signid)
    url = 'https://student.wozaixiaoyuan.com/sign/doSign.json'
    headers = GetHeaders(token,type="application/json")
    data = {'id': id,'signid': signid,
    #此处需要将位置信息改为自己的
     'latitude': str(round(random.uniform(XX.XXXX,XX.XXXX),5)), #经纬度，随机在某个正方形区域内取点
     'longitude': str(round(random.uniform(XXX.XXXX,XXX.XXXX),5)),
     'country': '中国',
     'province': 'XX省',
     'city': 'XX市',
     'district': 'XX区',
     'township': 'XX街道'}
    try:
        r = requests.post(url, data = json.dumps(data,ensure_ascii=False).encode("utf-8").decode("latin1"), headers = headers, verify = False).json()
        logger.debug(r)
    except Exception as e:
        logger.error('Error:'+str(e))
        return
    if r["code"] != 0:
        logger.error("签到失败:"+str(r["code"]))
        return
    logger.info("签到成功")
    return

def AutoSign(token):
    logger.info("自动签到:"+token)
    url = 'https://student.wozaixiaoyuan.com/getMessage.json'
    headers = GetHeaders(token)
    try:
        r = requests.post(url, headers = headers, verify = False).json()
        logger.debug(r)
    except Exception as e:
        logger.error('Error:'+str(e))
        return
    if r["code"] != 0:
        logger.error("获取未读消息失败:"+str(r["code"]))
        return
    elif r["data"]["sign"] == 0:
        logger.info("没有未完成的签到...")
        return
    unsignNum = r["data"]["sign"]
    url = 'https://student.wozaixiaoyuan.com/sign/getSignMessage.json'
    data = {'page':"1",'size':"5"}
    try:
        r = requests.post(url, data = data,headers = headers, verify = False).json()
        logger.debug(r)
    except Exception as e:
        logger.error('Error:'+str(e))
        return
    if r["code"] != 0:
        logger.error("获取签到信息失败:"+str(r["code"]))
        return
    AllSigns = r["data"]
    for Sign in AllSigns:
        if Sign["state"] == 1 and Sign["type"] == 0 : # 新签到
            DoSign(str(Sign["logId"]),str(Sign["id"]),token)
        elif Sign["state"] == 2 and Sign["type"] == 0 : # 补签
            DoSign(str(Sign["logId"]),str(Sign["id"]),token)
    logger.info("所有签到处理完毕")
    return

def main_handler(event, context):
    
    # 此处填写抓包得到的token，可填写多个账号
    AllUsers = ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"]
    
    if event["Message"]=="AutoHealth":
        logger.info("AutoHealth...")
        list(map(test_url,AllUsers))
    elif event["Message"]=="AutoSign":
        logger.info("AutoSign...")
        list(map(AutoSign,AllUsers))
    return 0

if __name__ == '__main__':
    main_handler({"Message":"AutoSign"}, "")