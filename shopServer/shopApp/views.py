from django.shortcuts import render
from django.shortcuts import redirect



import re
from django.http import HttpResponse
from qrcode.main import QRCode
import os
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFilter
from PIL import ImageFont
import json, urllib
from urllib.parse import urlencode



from urllib import parse,request

import requests

import datetime 
import time
from django import forms
from django.shortcuts import render_to_response
from django.core.files.uploadedfile import InMemoryUploadedFile
from shopApp.mytool import *
from django.db import connection
# from aip import  AipSpeech
import json
import base64
import subprocess

import string

import hashlib

from django.views.decorators.csrf import csrf_exempt

from django.core.cache import cache
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring


my_global_host_url = MyTool.global_domain()


# 获取城市列表数据
def get_chinese_address(request):

    add_file = "./shopApp/static/my_data/china_address_v4.json.json"

    fileobj = open(add_file , "r");
    add_content = fileobj.read()
    data = json.loads(add_content)


    return HttpResponse(json.dumps({"data":data , "status":"ok" , "message":"成功...."}) , content_type = "application/json")

    
# 查询用户上下级的方法
def getUserShangxiaji(request):
    wxid = request.POST.get("wxid" , "")

    if wxid == "":
        return HttpResponse(json.dumps({"status":"error" , "message":"请先获取用户信息..."}) , content_type = "application/json")



    cursor = connection.cursor()
    data = {}
    # 下级
    sqlStr = "select wxid from user where upperson = '%s'" % (wxid)
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    
    data["xiaji"] = []
    for item in rows:
        data["xiaji"].append(getUserDetailByWxid(item[0]))

    # 下下级
    data["xiaxiaji"] = []
    if data["xiaji"] != []:
        for onePerson in data['xiaji']:
            sqlStr = "select wxid from user where upperson = '%s'" % (onePerson.get("wxid" , ""))
            cursor.execute(sqlStr)
            rows = cursor.fetchall()
        
            for item in rows:
                data["xiaxiaji"].append(getUserDetailByWxid(item[0]))

    sqlStr = "select * from serversetting where id = 1"
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    data["bili"] = {}
    for item in rows:
        data["bili"]["wo"] = item[2]
        data["bili"]["shangji"] = item[3]
        data["bili"]["shangshangji"] = item[4]

    cursor.close()
    return HttpResponse(json.dumps({"data":data , "status":"ok" , "message":"成功...."}) , content_type = "application/json")


# 查询用户上下级的方法 准备删除掉了
def getUserShangxiaji111(request):
    wxid = request.POST.get("wxid" , "")
    cursor = connection.cursor()
    data = {}


    # 上级
    sqlStr = "select shangjiId from shangji where wxid = '%s'" % (wxid)
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    
    data["shangji"] = ""
    for item in rows:
        data["shangji"] = getUserDetailByWxid(item[0])

    # 上上级
    data["shangshangji"] = ""
    if data["shangji"] != "":
        sqlStr = "select shangjiId from shangji where wxid = '%s'" % (data["shangji"].get("wxid" , ""))
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        
        for item in rows:
            data["shangshangji"] = getUserDetailByWxid(item[0])


    # 下级
    sqlStr = "select xiajiId from xiaji where wxid = '%s'" % (wxid)
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    
    data["xiaji"] = []
    for item in rows:
        data["xiaji"].append(getUserDetailByWxid(item[0]))

    
    # 下下级
    sqlStr = "select xiaxiajiId from xiaxiaji where wxid = '%s'" % (wxid)
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    
    data["xiaxiaji"] = []
    for item in rows:
        data["xiaxiaji"].append(getUserDetailByWxid(item[0]))
        

    sqlStr = "select * from serversetting where id = 1"
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    data["bili"] = {}
    for item in rows:
        data["bili"]["wo"] = item[2]
        data["bili"]["shangji"] = item[3]
        data["bili"]["shangshangji"] = item[4]

    cursor.close()
    return HttpResponse(json.dumps({"data":data , "status":"ok" , "message":"成功...."}) , content_type = "application/json")


# 添加用户上级方法
# 如果城测试成功,就把 addUserShangxiaji 这个方法删掉了
def addUserShangjiNewFn(request):
    wxid = request.POST.get("wxid" , "")
    upperson = request.POST.get("upperson" , "")
    cursor = connection.cursor()
    is_you_guanxi = False

    one = ''

    sql_str1 = "select upperson from user where wxid = '%s'" % wxid

    cursor.execute(sql_str1)
    result1 = cursor.fetchall()


    for row in result1:
        one = row[0]


    if one != "":
        return HttpResponse(json.dumps({"status":"error" , 'message': '该用户已经有上级了'}) , content_type = "application/json")
    else :
        sqlStr1 = "update user set upperson = '%s' where wxid = '%s'" % (upperson , wxid) 
        cursor.execute(sqlStr1)

        return HttpResponse(json.dumps({"status":"ok" , 'message': '添加成功'}) , content_type = "application/json")




    
# 添加用户的上下级 不再用了  准备删除该方法
def addUserShangxiaji(request):
    wxid = request.POST.get("wxid" , "")
    shangjiId = request.POST.get("shangjiId" , "")
    cursor = connection.cursor()
    sqlStr1 = "insert into shangji (wxid , shangjiId) values ('%s' , '%s')" % (wxid , shangjiId) 
    sqlStr2 = "insert into xiaji (wxid , xiajiId) values ('%s' , '%s')" % (shangjiId , wxid)

    cursor.execute(sqlStr1)
    cursor.execute(sqlStr2)

    sqlStr3 = "select shangjiId from shangji where wxid='%s'" % shangjiId
    shangshangji = ""
    cursor.execute(sqlStr3)

    rows = cursor.fetchall()
    for item in rows:
        shangshangji = item[0]

    if shangshangji == "":
        pass
    else:
        sqlStr4 = "insert into xiaxiaji (wxid , xiaxiajiId) values ('%s' , '%s')" % (shangshangji , wxid)
        cursor.execute(sqlStr4)

    # 查看 wxid 有没有下级
    sqlStr5 = "select xiajiId from xiaji where wxid='%s'" % wxid
    cursor.execute(sqlStr5)
    
    rows = cursor.fetchall()
    for item in rows:
        sqlStr6 = "insert into xiaxiaji (wxid , xiaxiajiId) values ('%s' , '%s')" % (shangjiId , item[0])
        cursor.execute(sqlStr6)

    
    
    
    cursor.close()

    return HttpResponse(json.dumps({"ssss":"jjj"}) , content_type = "application/json")



# 工具方法
# 为用户生成二维码，并保存
def saveQrcodeImg(wxid):
    if wxid == "":
        return ""
    
    qrcodeImg = createQrcodeByString(wxid)

    filepath = "./shopApp/static/myfile/userQrcode";
    filepath = filepath + "/" + wxid + ".jpg"

    qrcodeImg.save(filepath)

    return "static/myfile/userQrcode/" + wxid + ".jpg"

# 生成二维码图片的方法
def createQrcodeByString(qrcodeStr):
    qr = QRCode()
    qrcodeStr = 'http://' + my_global_host_url + '/static/vue-shop/dist/index.html?wxid=' + qrcodeStr
    qr.add_data(qrcodeStr)
    im = qr.make_image()
    # im.show()
    return im

# 测试方法
def ceshi(request):
    cursor = connection.cursor()
    sqlStr = "update wxToken set common_token = '2222' where id = 1"
    cursor.execute(sqlStr)
    return HttpResponse(json.dumps({'status':"error" , 'message':'测试方法'}) , content_type = "application/json")
    

# 订单rows ---》  订单Data
def orderRows_to_orderData(rows):
    dataArr = []
    for row in rows:
        tempDic = {}
        tempDic["userinfo"] = getUserDetailByWxid(row[0])
        tempDic["orderId"] = row[1]
        tempDic["createTime"] = MyTool.none_or_strftime(row[2])
        tempDic["status"] = row[3]
        tempDic["freightPrice"] = row[4]
        tempDic["freightRiskPrice"] = row[5]
        tempDic["payTime"] = row[6]
        tempDic["addressId"] = getAddressByAddressid(row[7])
        tempDic["wxOrderId"] = row[8]
        tempDic["transportMethod"] = row[9]
        tempDic["invoiceType"] = row[10]
        tempDic["invoiceContent"] = row[11]
        tempDic["deliveryTime"] = row[12]
        tempDic["noGoodsMethod"] = row[13]
        tempDic["sendCompany"] = row[14]
        tempDic["fahuoTime"] = row[15]
        tempDic["originFreightPrice"] = row[16]
        tempDic["comment"] = row[17]
        dataArr.append(tempDic)
    return dataArr


# 微信 : 获取用户信息 新来的方法
# 与另一个通过code值获取用户信息的方法看看是否冲突 需要删除那一个
def get_detail_user_info(request):
    open_id = request.POST.get("openid" , "")
    if open_id == "":
        return HttpResponse(json.dumps({'status':"error" , 'message':'参数错误'}) , content_type = "application/json")

    user_info =  getUserDetailByWxid(open_id)



    if user_info == {}:
        acces_tok = getAccess_token()

        user_info = getUserInfoByWxServer(acces_tok , open_id);

        if user_info.get("errcode" , "") != "" or user_info == "" or user_info == 'null':
            return HttpResponse(json.dumps({'status':"error" , 'message':'用户信息获取失败，请关闭该界面重新获取' , 'user_info':user_info}) , content_type = "application/json")
        else:
            user_info['wxid'] = user_info['openid']
            user_info['headimg'] = user_info['headimgurl']
            insertUserWxInfoToTable(user_info)
            user_info["is_first_register"] = "true"
            return HttpResponse(json.dumps({'status':"ok" , 'message':'获取成功' , 'data':user_info}) , content_type = "application/json")
    else :
        user_info['headimgurl'] = user_info['headimg']
        user_info['openid'] = user_info['wxid']
        user_info["is_first_register"] = "false"
        return HttpResponse(json.dumps({'status':"ok" , 'message':'获取成功' , 'data':user_info}) , content_type = "application/json")


def ad_row_to_dic(data):
    adid=data[0];
    imgPath=data[1];
    position=data[2];   
    adtime=MyTool.none_or_strftime(data[3])
    address=data[4]; 
    introduce=data[5]; 
    tempDic = {"imgPath":imgPath , "adid":adid , "position":position,"adtime":str(adtime) , "address":address , "introduce":introduce}
    return tempDic    
    
# app首页数据
def appHomePageData(request):
    
    cursor = connection.cursor();

    # 广告数据
    adData=[];
    sql="select * from ad";
    cursor.execute(sql)
    datas=cursor.fetchall();
    for data in datas:
        tempDic = ad_row_to_dic(data)
        adData.append(tempDic)

    # 已上架商品数据
    sqlStr = "select * from goods where status = '1'"
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    goodsData = []
    for row in rows:
        oneData = goodsDataRowToDic(row)
        goodsData.append(oneData)

    # 推荐商品
    cursor.execute("SELECT * FROM recommendGoods")
    datas=cursor.fetchall();
    recommendData = recommendGoodsRow_to_dic(datas)

    cursor.close()
    temp_data = {
        'adData': adData , 
        'goodsData': goodsData , 
        'recommendData': recommendData
    }
    return HttpResponse(json.dumps({'status':"ok" , 'message':'获取成功' , 'data':temp_data}) , content_type = "application/json")

# 微信 : 通过code 获取openid 新来的方法
def getOpenidByCode_new_fn(request):
    # 自己的appid和secret
    # appid = "wx619c085e365678c4"
    # secret = "12abb748fd981b90aa22f165817d231f"

    # 刘润东的appid和secret
    # appid = "wxe0df1aa623047849"
    # secret = "cd3f7ae6c5cb67e73a9317acaf8d0658"


    # 明川的appid和secret
    appid = "wxd789a73b4cea944d"
    secret = "c920a96414e839d4509c19d6d1741882"


    code = request.POST.get("code" , "")
    getAccess_tokenUrl = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=" + appid + "&secret=" + secret + "&code=" + code + "&grant_type=authorization_code"
    res = requests.get(getAccess_tokenUrl)
    res = res.text
    res = json.loads(res)

    if res.get("errcode" , "") != "" or res.get("access_token" , "") == "" or res.get("openid" , "") == "":
        # 获取出错
        return HttpResponse(json.dumps({'status':"error" , 'message':'用户信息获取失败，请关闭该界面重新获取' , 'data':{'errcode':res.get("errcode" , "") , 'access_token':res.get("access_token" , "") , 'openid':res.get("openid" , "")}}) , content_type = "application/json")
    else :
        open_id = res.get('openid' , '111')
        user_info =  getUserDetailByWxid(open_id)

        if user_info == {}:
            user_info = getUserInfoByWxServer(res.get("access_token" , "") , open_id);
            if user_info.get("errcode" , "") != "" or user_info == "" or user_info == 'null':
                return HttpResponse(json.dumps({'status':"error" , 'message':'用户信息获取失败，请关闭该界面重新获取' , 'user_info':user_info}) , content_type = "application/json")
            else:
                
                insertUserWxInfoToTable(user_info)
                user_info["is_first_register"] = "true"
                user_info =  getUserDetailByWxid(open_id)
                return HttpResponse(json.dumps({'status':"ok" , 'message':'获取成功' , 'data':user_info}) , content_type = "application/json")
        else :
            user_info["is_first_register"] = "false"
            return HttpResponse(json.dumps({'status':"ok" , 'message':'获取成功' , 'data':user_info}) , content_type = "application/json")

# 服务器验证
def wxService(request):
    signature = request.GET.get("signature" , "")
    timestamp = request.GET.get("timestamp" , "")
    nonce = request.GET.get("nonce" , "")
    echostr = request.GET.get("echostr" , "")

    token = "liuxiangyu"

    userInfo = ""

    openid = request.GET.get("openid" , "")

    return HttpResponse(echostr)

    if openid == "":
        return HttpResponse(json.dumps({'message':"openid获取失败" , "status":"error"}) , content_type = "application/json")

    userData = getUserDetailByWxid(openid)

    if userData == {}:
        pass
    else: 
        # 拿到用户信息了
        pass

    


    if echostr == "":
        # return HttpResponse(result , content_type = "application/json")
        return HttpResponse("llllll")
    else:
        return HttpResponse(echostr)

# 微信 : 将用户的微信资料保存到数据库
def insertUserWxInfoToTable(userObj):
    openid = userObj.get("openid" , "")
    cursor = connection.cursor()

    qrCodeImgPath = saveQrcodeImg(openid)

    sqlStr = "insert into user \
    (wxid , nickName , gender , city , \
    province , country , headimg , qrcode) \
    values ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s')" % (userObj.get("openid" , "") , userObj.get("nickname" , "") , userObj.get("sex" , "") , userObj.get("city" , "") , userObj.get("province" , "") , userObj.get("country" , "") , userObj.get("headimgurl" , "").replace("\/" , "/") , qrCodeImgPath)

    
    cursor.execute(sqlStr)
    cursor.close()



# 微信 : 从微信服务器中获取用户信息 新来的方法
def getUserInfoByWxServer(access_token , openid):

    # userInfo_url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token=" + access_token + "&openid=" + openid + "&lang=zh_CN"
    
    userInfo_url = 'https://api.weixin.qq.com/sns/userinfo?access_token=' + access_token + '&openid=' + openid + '&lang=zh_CN'

    myrequest = requests.get(userInfo_url)
    result = myrequest.text
    resultObj = json.loads(result)
    

    return resultObj

# 微信 : 通过url获取普通access_token 新来的方法
def get_access_token_by_url():
    
    # 自己的appid和secret
    # appid = "wx619c085e365678c4"
    # secret = "12abb748fd981b90aa22f165817d231f"

    # 刘润东的appid和secret
    # appid = "wxe0df1aa623047849"
    # secret = "cd3f7ae6c5cb67e73a9317acaf8d0658"

    # 明川的appid和secret
    appid = "wxd789a73b4cea944d"
    secret = "c920a96414e839d4509c19d6d1741882"

    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (appid , secret)

    myrequest = requests.get(access_token_url)
    result = myrequest.text
    resultObj = json.loads(result)
   
    access_token = resultObj.get("access_token" , "")

    return access_token



def ceshiTupiandizhi(request):
    
    media_id = request.POST.get('media_id' , '')
    comment_id = request.POST.get('comment_id' , '')
    access_token = getAccess_token()

    img_url = r'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=' + access_token + '&media_id=' + media_id

    response = requests.get(img_url)
    img_data = response.content
    filepath = "./shopApp/static/myfile/pinglunimg/" + media_id + ".jpg"
    sqlPath = "static/myfile/pinglunimg/" + media_id + ".jpg"
    xie_img = open(filepath , "wb")
    xie_img.write(img_data)

    cursor = connection.cursor()
    commImgId = randomString()

    sqlStr = "insert into commImg (comImgId , commId , img) values ('%s' , '%s' , '%s')" % (commImgId , comment_id , sqlPath)
    cursor.execute(sqlStr)
    cursor.close()
    
    return HttpResponse(json.dumps({'status':"ok" , 'message':'保存成功'}) , content_type = "application/json")

# 获取token的api
def getAccess_token_api(request):
    access_token = getAccess_token()
    return HttpResponse(json.dumps({'status':"ok" , 'data':access_token}) , content_type = "application/json")

# 微信 : 工具方法 获取普通token  新来的方法
def getAccess_token():
    
    cursor = connection.cursor()

    # acces_tok = get_access_token_by_url()
    # sqlStr = "update wxToken set common_token = '%s' where id = 1" % acces_tok
    # cursor.execute(sqlStr)
    
    # 当前时间
    nowTime = datetime.datetime.now();
    nowTime = nowTime + datetime.timedelta(hours = 8)
    nowTime = nowTime.strftime("%Y%m%d%H%M%S")

    # 数据库时间
    sqlStr = "select * from wxToken where id=1";
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    sqlTime = ""
    acces_tok = ""

    for item in rows:
        sqlTime = item[2]
        acces_tok = item[1]
    
    sqlTime = sqlTime + datetime.timedelta(hours=1.8)
    sqlTime = sqlTime.strftime("%Y%m%d%H%M%S")

    if int(sqlTime) >= int(nowTime):
        pass
    else: 
        acces_tok = get_access_token_by_url()
        sqlStr = "update wxToken set common_token = '%s' where id = 1" % acces_tok
        cursor.execute(sqlStr)
    return acces_tok

# 微信 : 通过url 获取js ticket 票据 新来的方法
def getJsapi_ticket_buy_url(access_token):
    jsapi_ticket_url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % access_token
    myrequest = requests.get(jsapi_ticket_url)
    result = myrequest.text
    resultObj = json.loads(result)
    jsapi_ticket = resultObj.get("ticket" , "")

    return jsapi_ticket

# 微信 : 工具方法 获取 js ticket 票据 新来的方法
def get_jsapi_ticket(access_token):
    cursor = connection.cursor()
    
    # 当前时间
    nowTime = datetime.datetime.now();
    nowTime = nowTime + datetime.timedelta(hours = 8)
    nowTime = nowTime.strftime("%Y%m%d%H%M%S")

    # 数据库时间
    sqlStr = "select * from wxJsapi where id=1";
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    sqlTime = ""
    jsapi = ""

    for item in rows:
        sqlTime = item[2]
        jsapi = item[1]
    
    sqlTime = sqlTime + datetime.timedelta(hours=1.8)
    sqlTime = sqlTime.strftime("%Y%m%d%H%M%S")

    if int(sqlTime) >= int(nowTime):
        pass
    else: 
        jsapi = getJsapi_ticket_buy_url(access_token)
        sqlStr = "update wxJsapi set jsapi = '%s' where id = 1" % jsapi
        cursor.execute(sqlStr)
        
        
    return jsapi

# 清楚 access_token 和 jsapi_ticket 没用的方法
def clearAccess_tokenAndJsapi_ticket(request):
    
    return HttpResponse(json.dumps({'message':'清空成功' , 'status':'ok'}) , content_type = "application/json")

def wxjsqianmingFn(request):
    nonce_str = 'lkjiu8765tgyhuj7' 
    timestamp = str(int(time.time()))
    jsapi_ticket = 'kgt8ON7yVITDhtdwci0qeZob5-f597xcWetFxB0Aywh2an0dJQ0RCW6rUx-Lp0DS_ip-eFnMN-agbS1aENZboQ' 
    url = request.POST.get('url' , "")


    pinjieString = 'jsapi_ticket=' + jsapi_ticket + '&noncestr=' + nonce_str + '&timestamp=' + timestamp + '&url=' + url
    
    hash = hashlib.sha1()
    hash.update(pinjieString.encode("utf-8"))
    signature = hash.hexdigest()

    package = {
        'url':url , 
        'jsapi_ticket': jsapi_ticket , 
        'timestamp': timestamp,
        'nonceStr': nonce_str,
        'signature': signature,
    }
    return HttpResponse(json.dumps(package) , content_type = "application/json")



# 微信 : JS-SDK 签名包生成 新来的方法
def getJsApiPackage(access_token , jsapi_ticket , url):
    nonce_str = 'lkjiu8765tgyhuj7'  
    timestamp = str(int(time.time())) 

    
    pinjieString = 'jsapi_ticket=' + jsapi_ticket + '&noncestr=' + nonce_str + '&timestamp=' + timestamp + '&url=' + url
    


    hash = hashlib.sha1()
    hash.update(pinjieString.encode("utf-8"))
    signature = hash.hexdigest()

    package = {
        'url':url , 
        'jsapi_ticket': jsapi_ticket , 
        'timestamp': timestamp,
        'nonceStr': nonce_str,
        'signature': signature,
    }
    return package

# 微信 : jssdk 新来的方法
def wxjssdk(request):
    access_token = getAccess_token()
    jsapi_ticket = get_jsapi_ticket(access_token)

    url = request.GET.get("url" , "")

    package = getJsApiPackage(access_token , jsapi_ticket , url)


    return HttpResponse(json.dumps(package) , content_type = "application/json")


    



# from dwebsocket.decorators import accept_websocket,require_websocket
# import dwebsocket

# from websocket import create_connection
# import websocket

# serversetting 表
def insertServerSetting(request):
    try:
        fanliValue = request.POST.get("fanliValue" , "")
        wo = request.POST.get("wo" , "")
        shangji = request.POST.get("shangji" , "")
        shangshangji = request.POST.get("shangshangji" , "")
        # if fanliValue == "":
        #     return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type="application/json")

        sqlStr = "update serversetting set fanli = '%s' , wo='%s' , shangji='%s' , shangshangji='%s' where id=1" % (fanliValue , wo , shangji , shangshangji)
        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        cursor.close()
        if result >= 1:
            return HttpResponse(json.dumps({'status':'error' , 'message':'操作成功'}) , content_type="application/json")
        else :
            return HttpResponse(json.dumps({'status':'error' , 'message':'操作失败'}) , content_type="application/json")
    except Exception as e:    
        raise e
        return HttpResponse(json.dumps({'status':'error' , 'message':'服务器设置表插入操作失败，请联系服务器管理人员'}) , content_type="application/json")

# 获取设置信息
def getServerSetting(request):
    try:
        settingId = request.POST.get("id" , "")
        if settingId == "":
            return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type="application/json")

        sqlStr = "select * from serversetting where id=%d" % int(settingId)
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        cursor.close()
        tempDic = {}
        for row in rows:
            tempDic["id"] = row[0]
            tempDic["fanli"] = row[1]
            tempDic["wo"] = row[2]
            tempDic["shangji"] = row[3]
            tempDic["shangshangji"] = row[4]
        return HttpResponse(json.dumps({'status':'ok' , 'data':tempDic}) , content_type="application/json")
       
    except Exception as e:    
        raise e
        return HttpResponse(json.dumps({'status':'error' , 'message':'服务器设置表查询操作失败，请联系服务器管理人员'}) , content_type="application/json")
 


# 工具方法

# 根据 wxid 查询用户的 地址记录列表
def getAddressListByWxid(wxid):
    myData = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM address WHERE wxid='%s'" % wxid)
    datas = cursor.fetchall()
    cursor.close()
    for data in datas:
        addid = data[0]
        wxid = data[1]
        username = data[2]
        tel = data[3]
        address = data[4]
        mailcode = data[5]
        flag = data[6]
        tempDic = {"addid":addid , "wxid":wxid , "username":username , "tel":tel , "address":address , "mailcode":mailcode , "flag":flag}
        myData.append(tempDic)

    return myData

# 根据订单id 获取订单下所有商品的信息
def getGoodsInfoArrByOrderId(orderid):
    sqlStr = "select * from order_goods_table where orderTableId='%s'" % orderid
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    cursor.close()
    bigDic = {
        'totalNum':0 , 
        'totalMoney':0 , 
        'totalFreightMoney':0 , 
        'totalRebateMoney':0 , 
        'goodsArr':[]
    }
    for row in rows:
        tempDic = {
            'orderTableId':row[0] , 
            'goods':{} , 
            'buyNumber':row[2] , 
            'transportId':row[3] , 
            'params':row[4] , 
            'is_pingjia': row[5] , 
            'status': row[6] , 
            'fahuotime': row[7]
        }


        tempDic["goods"] = getGoodsDetailByGoodsid(row[1])

        bigDic["totalNum"] = bigDic["totalNum"] + int(row[2])
        bigDic["totalMoney"] = float(bigDic["totalMoney"]) + float(tempDic["goods"].get("shop_price" , 0)) * int(tempDic.get("buyNumber"))
        bigDic["totalRebateMoney"] = float(bigDic["totalRebateMoney"]) + float(tempDic["goods"].get("shop_price" , 0)) * float(tempDic["goods"].get("rebate" , 0)) * int(tempDic.get("buyNumber"))
        bigDic["totalFreightMoney"] = bigDic["totalFreightMoney"] + int(tempDic["goods"].get("transportmoney" , 0))
             

        bigDic["goodsArr"].append(tempDic)


    return bigDic

# 工具方法： 根据地址id 查询地址信息
def getAddressByAddressid(addressid):
    tempDic = {}
    sqlStr = "select * from address where addid='%s'" % addressid
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    for row in rows:
        tempDic["addid"] = row[0]
        tempDic["wxid"] = row[1]
        tempDic["username"] = row[2]
        tempDic["tel"] = row[3]
        tempDic["address"] = row[4]
        tempDic["mailcode"] = row[5]
        tempDic["flag"] = row[6]

    return tempDic

# 商品评论数量 + 1
def addOneCommentNumberByGoodsid(goodsid):
    sqlStr = "update goods set commentNumber=commentNumber+1 where goodsid='%s'" % goodsid
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    cursor.close()



# 根据商品id获取轮播图数组
def getLunboImagesByGoodsid(rows):
    lunboArr = []
    for row in rows:
        tempDic = {
            'id':row[0] , 
            'image':row[1]
        }

        lunboArr.append(tempDic)

    return lunboArr


# 将一行商品数据转变成一个字典的方法
def goodsDataRowToDic(row):
    goods = {
        'goodsid':row[0],
        'goodsname':row[1],
        'product_number':row[2],
        'market_price':row[3],
        'shop_price':row[4] , 
        'product_brief_info':row[6] , 
        'details':row[7] , 
        'goodsparams1':row[8] , 
        'goodsparams2':row[9] , 
        'product_weight':row[10],
        'counts':row[11],
        'warning_counts':row[12],
        'shopname':row[13],
        'product_brand':row[14],
        'status':row[15],
        'uptime':MyTool.none_or_strftime(row[17]),
        'downtime':MyTool.none_or_strftime(row[18]),
        'transportmoney':row[19],
        'addtime':MyTool.none_or_strftime(row[16]),
        'sellcount':row[20] , 
        'isinfudai':row[21] , 
        'isinmiaosha':row[22] , 
        'miaosha_info': '',
        'keywords':row[23] , 
        'songjifen':row[24] , 
        'jifenprice':row[25] , 
        'commentNumber':row[26] , 
        'origin_image':row[27] , 
        'product_image':row[28] , 
        'product_thumb_image':row[29] , 
        'is_jingpin':row[30] , 
        'is_rexiao':row[31] , 
        'is_commen_product':row[32] , 
        'is_entity_product':row[33] , 
        'xiaoClassiData':'' , 
        'haoping': row[35] , 
        'yiban': row[36] , 
        'chaping': row[37],
        'is_temai': row[38],
        'is_zhiying': row[39]
    }

    # 商品分类信息
    cursor = connection.cursor()
    sqlStr = "select xiao.id , xiao.fatherid , xiao.name , xiao.image , \
        xiao.bigName , xiao.midName , big.id \
        from minfenlei as xiao,midfenlei as mid,bigfenlei as big \
        where xiao.id='%s' and xiao.fatherid=mid.id and mid.fatherid = big.id" % row[34]
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    goods['xiaoClassiData'] = getAllFenleiInfoByMinfenleiId(rows)

    # 返利信息
    rebateValue = row[5]
    if rebateValue != "" and float(rebateValue) >= 0 and float(rebateValue) <= 1 :
        goods["rebate"] = rebateValue
    else:
        sqlStr = "select fanli from serversetting where id=1"
        cursor.execute(sqlStr)
        fanlis = cursor.fetchall()
        for fanli in fanlis:
            rebateValue = fanli[0]
        goods["rebate"] = rebateValue

    # 商品的秒杀信息
    if goods["isinmiaosha"] == "true":
        miaosha_sql = "SELECT * FROM secondkill where goodsid = '%s'" % goods["goodsid"]
        cursor.execute(miaosha_sql)
        miaosha_info = cursor.fetchall()
        for ms in miaosha_info:
            tempDic = {}
            tempDic["killid"] = ms[0]
            tempDic["goodsid"] = ms[1]
            tempDic["starttime"] = MyTool.none_or_strftime(ms[2])
            tempDic["stoptime"] = MyTool.none_or_strftime(ms[3])
            tempDic["miaoShaCount"] = ms[4]
            tempDic["alreadyMiaoShaNumber"] = ms[5]
            goods["miaosha_info"] = tempDic
    

    # 轮播图信息
    sqlStr = "select id , image from lunbo where goodsid='%s' order by addtime desc" % row[0]
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    lunboArr = getLunboImagesByGoodsid(rows)
    goods["lunbo"] = lunboArr

    cursor.close()

    return goods

# 获取所有的小分类
""" 
    商品属性管理
"""
def getAllXiaoFenlei(request):
    sqlStr = "select id , name , attrCounts from minfenlei"
    data = []
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    cursor.close()
    for item in rows:
        tempDic = {}
        tempDic["id"] = item[0]
        tempDic["name"] = item[1]
        tempDic["attrCounts"] = item[2]
        
        data.append(tempDic)

    return HttpResponse(json.dumps(data) , content_type="application/json")


# 根据小分类id获取整个分类信息
def getAllFenleiInfoByMinfenleiId(rows):
    
    tempDic = {}
    for row in rows:
        tempDic["minFenleiId"] = row[0]
        tempDic["minName"] = row[2]
        tempDic["image"] = row[3]

        tempDic["midId"] = row[1]
        tempDic["midName"] = row[5]

        tempDic["bigId"] = row[6]
        tempDic["bigName"] = row[4]
    return tempDic


def home(request):
    is_login = request.session.get('IS_LOGIN')
    
    return render(request , "base.html");


def error(request):
    return HttpResponse("我是404");

def adsecondkill(request):
    return render(request , "adsecondkill.html");
def secondkillManage(request):
    return render(request , "secondkillManage.html");

def notInMiaoshaGoods(request):
    try:
        page = request.POST.get("page" , 1)
        if int(page) <= 1:
            page = 1
        start = (int(page) - 1) * 10
        sqlStr = "select * , (SELECT COUNT(0) FROM goods where isinmiaosha='false' ) from goods where isinmiaosha='false' limit %d , 10" % start
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        
        data = []
        goodscount = 0
        for row in rows:
            oneData = goodsDataRowToDic(row)
            data.append(oneData)
            goodscount = row[40]

        cursor.close()
        return HttpResponse(json.dumps({'data':data, 'status':'ok' , 'count':goodscount}), content_type="application/json");

    except Exception as e:
        raise e    
        return HttpResponse(json.dumps({'message':'添加用户积分操作异常,请联系服务器管理人员', 'status':'error'}), content_type="application/json");


def goodsManage(request):
    baseSelectName = ''
    try:
        baseSelectName = request.POST["baseSelectName"]
    except:
        pass
    Dict = {'baseSelectName':baseSelectName}
    if baseSelectName == "":
        return render(request , "goodsManage.html");
    else:
        return render(request , "goodsManage.html" , {'Dict':json.dumps(Dict)});
    


def adPage(request):
    return render(request , "adPage.html");


def test(request):
    return render(request , "test.html");


def test111(request):
    
    user_info =  getUserDetailByWxid("oJgVUt2mHIg6ewbRl3s-ZcaZq8os")
    return HttpResponse(json.dumps({"status":"ok" , "message":"删除成功" , "data": user_info}) , content_type="application/json")



def userManage(request):
    return render(request , "userManage.html");

def orderManage(request):
    return render(request , "orderManage.html");

def adManage(request):
    return render(request , "adManage.html");

def cartsManage(request):   
    return render(request , "cartsManage.html");

def activeManage(request):

    return render(request , "activeManage.html");

def addGoods(request):
    
    return render(request, "goodsAdd.html")
def changeLunbo(request):
    return render(request,"addLunbo.html")

def recomendGoods(request):
    return render(request,"recomendGoods.html")


def fenleiListPage(request):
    return render(request,"fenleiListPage.html")

def editFenleiAttrPage(request):
    return render(request,"editFenleiAttrPage.html")


# 积分商城界面
def jifenGoods(request):
    return render(request , "jifenGoods.html")

# 商品导出界面
def exportGoods(request):
    return render(request , "exportGoods.html")

#改变轮播图界面
def changePic(request):
    return render(request,"changePic.html");

def drawManage(request):
    return render(request,"drawManage.html")


# 登录界面
def login(request):
    request.session['IS_LOGIN'] = True
    return render(request , "login.html");

# 修改小分类属性
def modifyFenleiAttr(request):
    attrId = request.POST.get("attrId" , "")
    attrName = request.POST.get("attrName" , "")
    attrValue = request.POST.get("attrValue" , "")
    if attrId == "":
        return HttpResponse(json.dumps({"status":"error" , "message":"参数错误"}) , content_type="application/json")


    sqlStr = "update fenleiAttr set attrName = '%s' , attrValue = '%s' where id = '%s'" % (attrName , attrValue , attrId)
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    cursor.close()

    if result >= 1:

        return HttpResponse(json.dumps({"status":"ok" , "message":"修改成功"}) , content_type="application/json")
    else:
        return HttpResponse(json.dumps({"status":"error" , "message":"修改失败"}) , content_type="application/json")


# 获取小分类属性列表
def getFenleiAttr(request):
    fenleiId = request.POST.get("fenleiId" , "")
    currentId = randomString()
    if fenleiId == "":
        return HttpResponse(json.dumps({"status":"error" , "message":"参数错误"}) , content_type="application/json")


    sqlStr = "select * from fenleiAttr where fenleiId='%s'" % fenleiId
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    cursor.close()

    data = []
    for item in rows:
        tempDic = {}
        tempDic["id"] = item[0]
        tempDic["fenleiId"] = item[1]
        tempDic["fenleiName"] = item[2]
        tempDic["attrName"] = item[3]
        tempDic["attrValue"] = item[4]
        data.append(tempDic)

    return HttpResponse(json.dumps({"status":"ok" , "data":data}) , content_type="application/json")



# 给小分类添加属性列表
def addFenleiAttr(request):
    fenleiId = request.POST.get("fenleiId" , "")
    fenleiName = request.POST.get("fenleiName" , "")
    attrName = request.POST.get("attrName" , "")
    attrValue = request.POST.get("attrValue" , "")
    currentId = randomString()

    if fenleiId == "" or attrName == "" or attrValue == "":
        return HttpResponse(json.dumps({"status":"error" , "message":"参数错误"}) , content_type="application/json")


    sqlStr = "insert into fenleiAttr (id , fenleiId , fenleiName , attrName , attrValue) values ('%s' , '%s' , '%s' , '%s' , '%s')" % (currentId , fenleiId , fenleiName , attrName , attrValue)
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)

    sqlStr = "update minfenlei set attrCounts = attrCounts + 1 where id = '%s'" % fenleiId
    cursor.execute(sqlStr)
    cursor.close()

    if result >= 1:
        return HttpResponse(json.dumps({"status":"ok" , "message":"添加成功" , "id":currentId}) , content_type="application/json")

    else :
        return HttpResponse(json.dumps({"status":"error" , "message":"添加失败"}) , content_type="application/json")


# 删除小分类的某一个属性列表
def deleteFenleiAttr(request):
    deleteId = request.POST.get("id" , "")
    fenleiid = request.POST.get("fenleiid" , "")
    
    if deleteId == "" or fenleiid == "":
        return HttpResponse(json.dumps({"status":"error" , "message":"参数错误"}) , content_type="application/json")


    sqlStr = "delete from fenleiAttr where id = '%s'" % deleteId
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    if result >= 1:
        sqlStr = "update minfenlei set attrCounts = attrCounts - 1 where id = '%s'" % fenleiid
        cursor.execute(sqlStr)
    cursor.close()

    if result >= 1:

        return HttpResponse(json.dumps({"status":"ok" , "message":"删除成功"}) , content_type="application/json")

    else :
        return HttpResponse(json.dumps({"status":"error" , "message":"删除失败"}) , content_type="application/json")



# 登录接口 (ok)
def loginApi(request): 
    userName = request.POST.get("username" , "")
    password = request.POST.get("password" , "")

    if userName == "" or password == "":
        errorMSG = MyTool.resultError("参数出错");
        return HttpResponse(json.dumps(errorMSG) , content_type="application/json")


    cursor = connection.cursor()
    sqlResult = cursor.execute('SELECT * FROM manager WHERE username=\"%s\" AND pwd=\"%s\"'%(userName , password))
    
    
    cursor.close()
    if sqlResult >= 1:
        
        successMSG = MyTool.resultOk("登陆成功");
        return HttpResponse(json.dumps(successMSG) , content_type="application/json")
    else:
        
        errorMSG = MyTool.resultError("登录失败");
        return HttpResponse(json.dumps(errorMSG) , content_type="application/json")

    
   
    



# 用户消费 积分 账户余额 返利等字段的 接口  已完成
def useUserNumber(request):
    try:
        wxid = request.POST["wxid"]
        optionNumber = request.POST["optionNumber"]
        optionName = request.POST["optionName"]


        optionNumber = json.loads(optionNumber)
        optionName = json.loads(optionName)

        sqlStr = "update user set "

        for index , item in enumerate(optionName):
            sqlStr = sqlStr + item + " = " + item + " - " + str(optionNumber[index]) + ","
        sqlStr = sqlStr[0:-1]

        sqlStr = sqlStr + " where wxid = '%s'" % wxid

        cursor = connection.cursor()
        cursor.execute(sqlStr)

        return HttpResponse(json.dumps({'message':'消费成功', 'status':'ok'}), content_type="application/json")
    
    
    except Exception as e:  
        raise e
        return HttpResponse(json.dumps({'message':'消费用户积分操作异常,请联系服务器管理人员', 'status':'error'}), content_type="application/json");
# 添加用户 积分 返利 账户余额 等接口 已完成
def addUserSomeNumber(request):
    try:
        wxid = request.POST["wxid"]
        optionNumber = request.POST["optionNumber"]
        optionName = request.POST["optionName"]

        optionNumber = json.loads(optionNumber)
        optionName = json.loads(optionName)

        sqlStr = "update user set "

        for index , item in enumerate(optionName):
            sqlStr = sqlStr + item + " = " + item + " + " + str(optionNumber[index]) + ","
        sqlStr = sqlStr[0:-1]

        sqlStr = sqlStr + " where wxid = '%s'" % wxid

        cursor = connection.cursor()
        cursor.execute(sqlStr)

        sqlStr = "select jifen , acountmoney from user where wxid='%s'" % wxid
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        
        
        data = getUserDetailByWxid(wxid)

        return HttpResponse(json.dumps({'message':'更新成功', 'data':data , 'status':'ok'}), content_type="application/json")
    
    
    except Exception as e:    
            return HttpResponse(json.dumps({'message':'添加用户积分操作异常,请联系服务器管理人员', 'status':'error'}), content_type="application/json");

def user_row_to_dic_one(rows):
    oneData = {}
    for row in rows:
        oneData = {
            "username":row[0] , 
            "headimg":row[1] , 
            "phone":row[2] , 
            "pwd":row[3] , 
            "wxid":row[4] , 
            "activecode":row[5] , 
            "redpack":row[6] , 
            "upperson":row[7] , 
            "downperson":row[8] , 
            "integral":row[9] , 
            "bankcard":row[10] , 
            "power":row[11] , 
            "registertime":MyTool.none_or_strftime(row[12]),
            "qrcode":row[13] , 
            "country":row[14] , 
            "gender":row[15] , 
            "city":row[16] , 
            "province":row[17] , 
            "privilege":row[18] , 
            "jifen":row[19] , 
            "buyMoney":row[20] ,
            "rebate":row[21] ,
            "acountmoney":row[22] ,
            "rewardmoney":row[23] ,
            "isFirstBuy":row[24] ,
            "qianDaoTime":row[25] ,
            "nickName":row[26],
            "qiandaoDays":row[27]
        }
    return oneData
        
# 工具方法: 根据 wxid 获取用户信息
# 微信 : 根据openid从数据库中获取用户的信息
# 成功 返回 userObj
# 失败 返回 {}
def getUserDetailByWxid(wxid):
    sqlStr = "select * from user where wxid = '%s'" % wxid
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    cursor.close()
    oneData = user_row_to_dic_one(rows)
    
    return oneData


# 用户签到流程 完成
def modifyUserQianDaoTime(request):
    try:
        wxid = request.POST.get("wxid" , "")
        # qianDaoTime = request.POST.get("qianDaoTime" , "")
        # qiandaoDays = request.POST.get("qiandaoDays" , "")

        sqlStr = "select qianDaoTime , qiandaoDays , jifen from user where wxid='%s'" % wxid
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        
        resultData = {}
        data = {}
        for row in rows:
            data["qiandaoTime"] = row[0]
            data["qiandaoDays"] = row[1]
            data["jifen"] = row[2]

        # 当前时间
        nowTime = datetime.datetime.now();
        nowTime = nowTime + datetime.timedelta(hours = 8)
        nowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")

        if data["qiandaoTime"] == "":
            # 第一次签到
            resultData["message"] = "第一次签到"
            resultData["status"] = "ok"
            resultData["days"] = 1
            resultData["jifen"] = data["jifen"] + 5
            resultData["qiandao_time"] = nowTime
            sqlStr = "update user set jifen = jifen + 5 , qianDaoTime = '%s' , qiandaoDays = 1 where wxid = '%s'" % (nowTime , wxid)
            cursor.execute(sqlStr)
            pass
        else :
            sqlTime = data["qiandaoTime"]
            # 判断数据库时间 与 当前时间 是否是同一天
            if nowTime[:10] == sqlTime[:10]:
                # 同一天
                resultData["message"] = "今天已经签到了"
                resultData["status"] = "error"
            else:
                # 不是同一天
                # 判断是否是连续签到
                if nowTime[:4] != sqlTime[:4]:
                    # 年份不一样
                    resultData["message"] = "签到成功"
                    resultData["status"] = "ok"
                    resultData["days"] = 1
                    resultData["jifen"] = data["jifen"] + 5
                    resultData["qiandao_time"] = nowTime
                    sqlStr = "update user set jifen = jifen + 5 , qianDaoTime = '%s' , qiandaoDays = 1 where wxid = '%s'" % (nowTime , wxid)
                    cursor.execute(sqlStr)
                else:
                    # 年份一样,在判断月份是否一样
                    if nowTime[5:7] != sqlTime[5:7]:
                        # 月份不一样 
                        resultData["message"] = "签到成功"
                        resultData["status"] = "ok"
                        resultData["days"] = 1
                        resultData["jifen"] = data["jifen"] + 5
                        resultData["qiandao_time"] = nowTime
                        sqlStr = "update user set jifen = jifen + 5 , qianDaoTime = '%s' , qiandaoDays = 1 where wxid = '%s'" % (nowTime , wxid)
                        cursor.execute(sqlStr)
                    else :
                        # 月份一样
                        # 从日期上判断是否是连续签到
                        if int(nowTime[8:10]) - int(sqlTime[8:10]) == 1:
                            # 是连续签到
                            resultData["message"] = "连续签到成功"
                            resultData["status"] = "ok"
                            resultData["days"] = data["qiandaoDays"] + 1
                            up_fen = 5
                            if 7 <= resultData["days"] < 30:
                                up_fen = 10
                            if resultData["days"] >= 30:
                                up_fen = 20
                            resultData["jifen"] = data["jifen"] + up_fen
                            resultData["qiandao_time"] = nowTime
                            sqlStr = "update user set jifen = jifen + %d , qianDaoTime = '%s' , qiandaoDays = qiandaoDays + 1 where wxid = '%s'" % (up_fen , nowTime , wxid)
                            cursor.execute(sqlStr)
                        else:
                            # 不是连续签到
                            resultData["message"] = "签到成功"
                            resultData["status"] = "ok"
                            resultData["days"] = 1
                            resultData["jifen"] = data["jifen"] + 5
                            resultData["qiandao_time"] = nowTime
                            sqlStr = "update user set jifen = jifen + 5 , qianDaoTime = '%s' , qiandaoDays = 1 where wxid = '%s'" % (nowTime , wxid)
                            cursor.execute(sqlStr)
        cursor.close()
        return HttpResponse(json.dumps(resultData),content_type="application/json");
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({'status':"error" , 'message':"修改签到时间操作异常,请联系服务器管理人员"}),content_type="application/json");



# 用户积分兑换余额接口
def jifenToAccount(request):
    try:
        wxid = request.POST.get("wxid" , "")
        jifen = request.POST.get("jifen" , 0)
        jifen = int(jifen)
        if wxid == "" or jifen == 0:
            return HttpResponse(json.dumps({'message':'请传入wxid', 'status':'error'}), content_type="application/json");

        jifen = jifen / 200
        jifen = int(jifen)

        sqlStr = "update user set acountmoney = acountmoney + %d , jifen = jifen - %d where wxid = '%s'" % (jifen , jifen * 200 , wxid)

        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        cursor.close()

        if result >= 1:
            return HttpResponse(json.dumps({'message':"积分兑换成功", 'status':'ok'}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({'message':"积分兑换失败", 'status':'error'}), content_type="application/json");

    except Exception as e:   
        raise e 
        return HttpResponse(json.dumps({'message':'用户节分兑换操作异常，请联系服务器管理人员', 'status':'error'}), content_type="application/json");


# 根据 微信id 获取用户信息 已完成 
def getUserInfoByWxid(request):
    try:
        wxid = request.POST.get("wxid" , "")
        if wxid == "":
            return HttpResponse(json.dumps({'message':'请传入wxid', 'status':'error'}), content_type="application/json");
        else :
            data = getUserDetailByWxid(wxid)
            return HttpResponse(json.dumps({'data':data, 'status':'ok'}), content_type="application/json");
    except Exception as e:    
        return HttpResponse(json.dumps({'message':'根据wxid查询用户信息失败，请联系服务器管理人员', 'status':'error'}), content_type="application/json");


# 获取用户的二维码
def getUserQrcode(request):
    try:
        openid = request.POST.get("wxid" , "")
        if openid == "":
            return HttpResponse(json.dumps({'message':'参数错误', 'status':'error'}), content_type="application/json");

        sqlStr = "select qrcode from user where wxid='%s'" % openid
        qrcodePath = ""
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            qrcodePath = row[0]

        return HttpResponse(json.dumps({'qrcodeImgPath':qrcodePath, 'status':'ok'}), content_type="application/json");
    except Exception as e:    
        return HttpResponse(json.dumps({'message':'获取用户二维码出错，请联系服务器管理人员', 'status':'error'}), content_type="application/json");


# 用户添加接口 已完成
def userManageJsonAdd(request):
    try:
        userData = json.loads(request.POST["userData"])

        sqlStr = "select wxid from user where wxid = '%s'" % userData["wxid"]

        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        if result == 1:
            cursor.close()
            return HttpResponse(json.dumps({"status":"error" , "message":"该用户已经存在"}) , content_type = "application/json");
        else: 
            sqlStr1 = "insert into user ("
            sqlStr2 = " values ("
            for key in userData :
                sqlStr1 = sqlStr1 + key + ","
                sqlStr2 = sqlStr2 + "'" + str(userData[key]) + "',"

            # 为用户生成二维码，并保存
            qrcodeImg = createQrcodeByString(userData["wxid"])

            filepath = "./shopApp/static/myfile/userQrcode";
            filepath = filepath + "/" + userData["wxid"] + ".jpg"

            qrcodeImg.save(filepath)

            saveToSqlPath = "/static/myfile/userQrcode/" + userData["wxid"] + ".jpg"

            sqlStr1 = sqlStr1 + "qrcode,"
            sqlStr1 = sqlStr1[0:-1]
            sqlStr1 = sqlStr1 + ")"

            sqlStr2 = sqlStr2 + "'" + saveToSqlPath +"',"
            sqlStr2 = sqlStr2[0:-1]
            sqlStr2 = sqlStr2 + ")"

            sqlStr = sqlStr1 + sqlStr2

            cursor = connection.cursor()
            result = cursor.execute(sqlStr)

            cursor.close() 

            if result == 1:
                return HttpResponse(json.dumps({"status":"ok" , "message":"用户添加成功"}) , content_type = "application/json");
            else:
                return HttpResponse(json.dumps({"status":"error" , "message":"用户添加失败"}) , content_type = "application/json");

    except Exception as e:    
        return HttpResponse(json.dumps({'message':"添加用户操作异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json");


def addUserAcountMoney(request):
    try:
        wxid = request.POST.get("wxid" , "")
        acountmoney = request.POST.get("acountMoney" , 0)
        
        if wxid == "":
            return HttpResponse(json.dumps({"message":'参数错误' , "status":"error"}) , content_type="application/json");

        acountmoney = float(acountmoney)
        sqlStr = "update user set acountmoney=acountmoney+%d where wxid='%s'" % (acountmoney , wxid)


        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        cursor.close()
        
        if result >= 1:
            return HttpResponse(json.dumps({"message":'充值成功' , "status":"ok"}) , content_type="application/json");
        else :
            return HttpResponse(json.dumps({"message":'充值失败' , "status":"error"}) , content_type="application/json");
    except Exception as e:

        return HttpResponse(json.dumps({'message':"充值操作异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json");




# 用户查询接口
def userManageJsonSelect(request):
    

    try:
        username = request.POST.get("username" , "")
        phone = request.POST.get("phone" , "")
        sqlStr = "select * from user where nickName like '%%%%%s%%%%'" % username
        if phone != "":
            sqlStr = "select * from user where phone = '%s'" % phone

        cursor=connection.cursor()

        allUsertables = []
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        cursor.close()
        for row in rows:
            allUsertables.append(getUserDetailByWxid(row[4]))
            
        cursor.close();
        return HttpResponse(json.dumps({'message':'查询成功' , 'data':allUsertables, 'status':'ok'}), content_type="application/json")
   
    except Exception as e:    
        raise e
        return HttpResponse(json.dumps({'data':[], 'status':'error' , 'message':'操作异常'}), content_type="application/json");
def userManageJsonDelete(request):
    for key in request.POST:
        wxid = request.POST.getlist(key)[0]

    #删除头像图片
    cursor=connection.cursor();
    headimg = ""
    cursor.execute("SELECT * FROM user WHERE wxid= %s "%(wxid));
    datas = cursor.fetchall()
    for data in datas:
        headimg = data[2]  
    aa = os.listdir("../shopServer/shopApp/static/myfile/")
    for item in aa:
        if item == headimg:
            os.remove("../shopServer/shopApp/static/myfile/"+headimg);
    cursor.close();

    #删除二维码图片
    cursor=connection.cursor();
    secondimg = ""
    cursor.execute("SELECT * FROM user WHERE wxid= %s "%(wxid));
    datas = cursor.fetchall()
    for data in datas:
        secondimg = data[18]  
    aa = os.listdir("../shopServer/shopApp/static/myfile/")
    for item in aa:
        if item == secondimg:
            os.remove("../shopServer/shopApp/static/myfile/"+secondimg);
    cursor.close();

    cursor=connection.cursor();
    try:
        cursor.execute("DELETE FROM user WHERE wxid = %s"%(wxid))
        connection.commit();
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
            
    except Exception as e:   
         # connection.rollback();
         return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
def userManageJsonUpdate(request):
    cursor = connection.cursor()
    datas = request.POST
    wxid= request.POST["wxid"]
    wxid = str(wxid)
    if request.FILES:
        #前台传过来的图片
        headImgs = request.FILES["headimg"];
        #随机字符串存取图片名字
        headImgsName = randomString() + ".jpg";
        #当上传头像的时候必然会传过来用户的Id,方法根据前台来决定
        
        cursor.execute("select headimg from user where wxid='%s'" % wxid)
        data = cursor.fetchall();
        if data[0][0]:
            tempimg = data[0][0];
            if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
            else:
                pass;
        filepath = "./shopApp/static/myfile/";
        #路径组合
        filepath = os.path.join(filepath,headImgsName)
        #在路径中创建图片名字
        fileobj = open(filepath , "wb");
        #并把前端传过来的数据写到文件中
        fileobj.write(headImgs.__dict__["file"].read());
        cursor.execute("update user set headimg='%s' where wxid=%s"%(headImgsName , datas["wxid"]))
    for key in datas:
        if key != 'wxid' and datas[key] != "":
            cursor.execute("update user set %s='%s' where wxid=%s"%(key , datas[key] , datas["wxid"]))
    cursor.close();                   
    return HttpResponse(json.dumps(MyTool.resultOk("更新成功")) , content_type="application/json");



# 按时间获取随机字符串
def randomString():
    randomId = ""
    for i in range (0,10):  
        nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S");  
        randomNum=random.randint(0,100);
        if randomNum<=10:  
            randomNum=str(0)+str(randomNum);  
        randomId=str(nowTime)+str(randomNum);
    return str(int(randomId) * 3)


# 轮播图删除接口
def deleteOneLunboById(request):
    lunboid = request.POST.get("lunboid" , "")
    image = request.POST.get("image" , "")
    if lunboid == "" or image == "":
        return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type = "application/json");

    sqlStr = "delete from lunbo where id='%s'" % lunboid
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    if result >= 1:
        removePath = "../shopServer/shopApp/" + image
        os.remove(removePath);
        return HttpResponse(json.dumps({'status':'ok' , 'message':'删除成功'}) , content_type = "application/json");
    else:
        return HttpResponse(json.dumps({'status':'error' , 'message':'删除失败'}) , content_type = "application/json");

 

# 工具方法 轮播图有关数据和图片的删除方法
# 删除轮播图表中的数据和图片
def deleteLunboInfoByGoodsId(goodsid):

    try:
        cursor = connection.cursor()

        sqlStr1 = "select image from lunbo where goodsid='%s'" % goodsid
        cursor.execute(sqlStr1)
        rows = cursor.fetchall()

        for row in rows:
            if isinstance(row , tuple) and len(row) > 0:
                os.remove("../shopServer/shopApp/" + row[0]);
            else :
                os.remove("../shopServer/shopApp/" + row);

        sqlStr2 = "delete from lunbo where goodsid='%s'" % goodsid
        
        cursor.execute(sqlStr2)
        cursor.close()   
    except Exception as e: 
        pass

     
    
def deleteManyLunboImage(request):
    # goodsid = request.POST.get("goodsid" , "")
    # if goodsid == "":
    #     return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type = "application/json");

    # deleteLunboInfoByGoodsId(goodsid)

    try:
        deleteArr = json.loads(request.POST.get("deleteArr" , []))
        for item in deleteArr:
            os.remove("../shopServer/shopApp/" + item);



        return HttpResponse(json.dumps({'status':'ok' , 'message':'删除成功'}) , content_type = "application/json");
   
    except Exception as e: 
        raise e
        return HttpResponse(json.dumps({'status':'error' , 'message':'删除失败,请重试'}) , content_type = "application/json");




# 获取轮播图列表接口 已完成
def getLunboList(request):
    goodsid = request.POST.get("goodsid" , "")
    if goodsid == "":
        return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type = "application/json");

    sqlStr = "select id , image from lunbo where goodsid='%s' order by addtime desc" % goodsid
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    cursor.close()

    lunboArr = getLunboImagesByGoodsid(rows)
    return HttpResponse(json.dumps({'status':'ok' , 'data':lunboArr}) , content_type = "application/json");

   


# 多张轮播图添加 新方法
def addLunboImages(request) :
    try:
        resultData = {"errno":0 , "data":[]}
        goodsid = request.GET.get("goodsid" , "")
        if goodsid == "":
                return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type = "application/json");

        cursor = connection.cursor()
        for key in request.FILES:

            imgs = request.FILES[key];
            imgName = randomString()

            imgName = imgName + ".jpg"; 
            filepath = "./shopApp/static/myfile/lunbo/";
            filepath = filepath + imgName

            
            fileHandle = open(filepath , "wb");
            fileHandle.write(imgs.__dict__["file"].read());
            fileHandle.close();

            sqlImgPath = "/static/myfile/lunbo/" + imgName
            lunboid = randomString()
            sqlStr = "insert into lunbo (id , goodsid , image) values ('%s' , '%s' , '%s')" % (lunboid , goodsid , sqlImgPath)
            cursor.execute(sqlStr)
            cursor.close()
            resultData["data"].append("http://" + my_global_host_url + "/static/myfile/uploadImage/" + imgName)

        return HttpResponse(json.dumps(resultData),content_type="application/json")

    except Exception as e: 
        return HttpResponse(json.dumps({'status':'error' , 'message':'轮播图添加操作失败，请联系服务器管理人员'}) , content_type = "application/json");



# 为商品添加轮播图 已完成
def addGoodsLunbo(request):
    try:
        goodsid = request.POST.get("goodsid" , "")
        if goodsid == "":
            return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type = "application/json");


        imgs = request.FILES.get("imgsFile" , "")
        if imgs == "":
            return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type = "application/json");

        
        imgsName = randomString() + ".jpg";
        filepath = "./shopApp/static/myfile/lunbo/";
        filename = os.path.join(filepath,imgsName)
        filehandle = open(filename , "wb");
        filehandle.write(imgs.__dict__["file"].read());
        sqlfilename = 'static/myfile/lunbo/' + imgsName

        lunboid = randomString()
        cursor = connection.cursor();
        sqlStr = "insert into lunbo (id , goodsid , image) values ('%s' , '%s' , '%s')" % (lunboid , goodsid , sqlfilename)
        result=cursor.execute(sqlStr);
        cursor.close()
        if result >= 1:
            
            return HttpResponse(json.dumps({'status':'ok' , 'message':'添加轮播图操作成功...'}) , content_type = "application/json");
        else :
            
            return HttpResponse(json.dumps({'status':'error' , 'message':'图片保存失败....'}) , content_type = "application/json");
    except Exception as e: 
        # raise e
        return HttpResponse(json.dumps({'status':'error' , 'message':'轮播图添加操作失败，请联系服务器管理人员'}) , content_type = "application/json");

        
  

#添加广告接口
def adManageJsonAdd(request):
                    
    adPosition=request.POST["adPosition"];
    adName=request.POST["adName"];
    adAddress=request.POST["adAddress"];
    imgs = request.FILES["images"];
    adId = randomString()

    imgsName = adId + ".jpg"; 

    try: 
        filepath = "./shopApp/static/myfile/adImgs";
        # filename = os.path.join(filepath,imgsName)
        filename = filepath + "/" + imgsName
        
        filename = open(filename , "wb");
        filename.write(imgs.__dict__["file"].read());
        filename.close();
    except Exception as e: 
        statusDic = MyTool.resultError("图片保存失败")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
   
   
   
    try:
        cursor = connection.cursor();
        sqlfilename = "static/myfile/adImgs" + "/" + imgsName
        sqlStr = "INSERT INTO ad(adid,position , imgs , adAddress , adIntroduce) VALUES ('%s','%s' , '%s' , '%s' , '%s' )" % (adId,adPosition , sqlfilename , adAddress , adName)
        result = cursor.execute(sqlStr);
        cursor.close()
        
        
        if result == 1:
            tempDic = {"imgPath":sqlfilename , "adid":adId , "position":adPosition,"adtime":"" , "address":adAddress , "introduce":adName}
            statusDic = {"status" : "ok" , "message" : "添加成功" , "data":tempDic};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else :
            
            statusDic = MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

    except Exception as e: 
        statusDic = MyTool.resultError("数据库操作失败")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
# 广告添加接口
def saveOneImageToServer(request):
    

    imgs = request.FILES["imgsFile"];
    imgsName = randomString() + ".jpg";
    filepath = "./shopApp/static/myfile";
    filename = os.path.join(filepath,imgsName)
    filename = open(filename , "wb");
    filename.write(imgs.__dict__["file"].read());
    filename.close();
    statusDic = {"status" : "ok" , "message" : "添加成功" , "imagePath":imgsName};
    
    
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json");

def adManageJsonSelectFn(position = ''):
    myData=[];
    cursor = connection.cursor();
    if position!="":
        sql=("select * from ad where position='%s'"%(position));
    else:
        sql="select * from ad";
    cursor.execute(sql)
    #取出数据
    datas=cursor.fetchall();
    cursor.close();
    for data in datas:
        tempDic = ad_row_to_dic(data)
        myData.append(tempDic)
    return myData

# 广告列表接口 兼 广告查询接口
def adManageJsonSelect(request):
    try:
        position = request.POST.get('position' , '')
        myData = adManageJsonSelectFn(position)
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}) , content_type="application/json");
    except Exception as e: 
        # raise e   
        return HttpResponse(json.dumps({'status':'error', 'message':'数据库操作失败'}), content_type="application/json");


# 广告删除接口 韩乐天
def adManageJsonDelete(request):
    try:
        adids = request.POST.get("adids" , [])
        imgs = request.POST.get("imgs" , [])

        adids = json.loads(adids)
        imgs = json.loads(imgs)

        for oneImg in imgs:
            removePath = "../shopServer/shopApp/" + oneImg
            if os.path.exists(removePath) == True:
                os.remove(removePath);

        sqlStr = "delete FROM ad WHERE adid in ("
        for deleteId in adids:
            sqlStr = sqlStr + "'" + deleteId + "' ,"

        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"

        cursor = connection.cursor()

        result = cursor.execute(sqlStr);
        cursor.close()

        if result >= 1:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":'广告删除操作异常,请联系服务器管理人员...' , "status":"error"}) , content_type="application/json");

        
    
        
    
    
# 修改广告接口
def adManageJsonUpdate(request):
    try:
        columnName = request.POST.get("columnName" , "")
        columnValue = request.POST.get("columnValue" , "")
        adid = request.POST.get("adid" , "")

        if columnName == "" or columnValue == "" or adid == "":
            return HttpResponse(json.dumps({"message":'参数错误' , "status":"error"}) , content_type="application/json");

        sqlStr = "update ad set %s = '%s' where adid = '%s'" % (columnName , columnValue , adid)
        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        cursor.close()

        if result >= 1:

            return HttpResponse(json.dumps({"message":'修改成功' , "status":"ok"}) , content_type="application/json");
        else:
            return HttpResponse(json.dumps({"message":'修改失败' , "status":"error"}) , content_type="application/json");

    except Exception as e:
        raise e
        return HttpResponse(json.dumps({'message': '广告修改操作异常,请联系服务器管理人员','status':'error'}), content_type="application/json");



# 返利添加接口
def rebateTableAdd(request):
    try:
        rebateid = randomString()
        wxid = request.POST.get("wxid" , "")
        goodsid = request.POST.get("goodsid" , "")

        goodsid = json.loads(goodsid)

        allRebateMoney = 0

        cursor = connection.cursor()

        for oneGoodsId in goodsid:
            oneGoods = getGoodsDetailByGoodsid(oneGoodsId)
            goodsRebate = oneGoods.get("rebate" , 0)
            allRebateMoney = allRebateMoney + int(goodsRebate)
            if int(goodsRebate) > 0:
                sqlStr = "insert into rebatetable (rebateid , wxid , goodsid , rebateMoney) values ('%s' , '%s' , '%s' , %d)" % (rebateid , wxid , oneGoodsId , int(goodsRebate))
                cursor.execute(sqlStr)
        
        sqlStr = "update user set rebate=rebate+%d where wxid='%s'" % (int(allRebateMoney) , wxid)
        result = cursor.execute(sqlStr)
        cursor.close()
        
        if result >= 1:
            
            return HttpResponse(json.dumps({'message': '添加返利成功','status':'ok'}), content_type="application/json");
        else: 
            cursor.close()
            return HttpResponse(json.dumps({'message': '添加返利失败','status':'error'}), content_type="application/json");
    


    except Exception as e:
        return HttpResponse(json.dumps({'message': '返利添加操作异常,请联系服务器管理人员','status':'error'}), content_type="application/json");
# 返利查询接口
def rebateTableQuery(request):
    try:
        wxid = request.POST.get("wxid" , "")
        sqlStr = "select * from rebatetable where wxid='%s'" % wxid
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        cursor.close()

        datas = []

        for row in rows:
            rebateid = row[0]
            wxid = row[1]
            goodsid = row[2]
            rebatetime = MyTool.none_or_strftime(row[3])
            rebateMoney = row[4]

            # 根据 wxid 获取用户信息
            user = getUserDetailByWxid(wxid)
            

            # 根据 goodsid 获取商品信息
            goods = getGoodsDetailByGoodsid(goodsid)

            tempDic = {
                'rebateid':rebateid , 
                'user': user, 
                'goods': goods, 
                'rebatetime': rebatetime , 
                'rebatemoney':rebateMoney
            }

            datas.append(tempDic)

        return HttpResponse(json.dumps({'data': datas,'status':'ok'}), content_type="application/json");

    except Exception as e:
        return HttpResponse(json.dumps({'message': '返利添加操作异常,请联系服务器管理人员','status':'error'}), content_type="application/json");
    

#红包管理页面
def redpack(request):
    return render(request,"redpack.html")
#红包添加 已完成
def redpackAdd(request):
    try:
        wxid=request.POST["wxid"];
        redpackid = randomString()
        getpath=request.POST["getpath"];
        money=request.POST["money"];
        title=request.POST["title"];
        description=request.POST["description"];
        starttime=request.POST["starttime"];
        endtime=request.POST["endtime"];
        detail=request.POST["detail"];
        cursor=connection.cursor();
        cursor.execute("INSERT INTO redpack(wxid,redpackid,getpath,money , title , description , starttime , endtime , detail) VALUES ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s')"% (wxid,redpackid,getpath,money , title , description , starttime , endtime , detail))
        
        statusDic=MyTool.resultOk("添加成功")
        cursor.close()
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except Exception as e :
        raise e
        statusDic=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#红包添加的通用方法(非接口路由使用)
def redpackAddCurrency(wxid, getpath, money):
    redpackid = randomString()
    try:
        cursor=connection.cursor();
        cursor.execute("INSERT INTO redpack(wxid,redpackid,getpath,money) VALUES (%s,%s,%s,%s)"% (wxid,redpackid,getpath,money))
        return True;
    except Exception as e :
        return False;
#红包删除 已完成
def redpackDelete(request):
    try:
        redpackids = request.POST["redpackids"]
        redpackids = json.loads(redpackids)
        cursor=connection.cursor();


        sqlStr = "delete FROM redpack WHERE redpackid in ("
        for deleteId in redpackids:
            sqlStr = sqlStr + "'" + deleteId + "' ,"

        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"
        result = cursor.execute(sqlStr)
        cursor.close();
        return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
    
    except Exception as e:
        return HttpResponse(json.dumps({'message': '红包删除接口异常,请联系服务器管理人员','status':'error'}), content_type="application/json");
# 红包查询 已完成
def redpackApi(request):
    try:
        wxid=request.POST["wxid"];
        sql="SELECT * from redpack WHERE wxid = '%s'" % wxid 
        allOrdertables = [];
        cursor = connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            ordertable = {
                'wxid':row[0],
                'redpackid':row[1],
                'getpath':row[2],
                'money':row[3],
                'addtime':MyTool.none_or_strftime(row[4]),
                'title':row[5],
                'description':row[6],
                'starttime':row[7],
                'endtime':row[8],
                'detail':row[9],
                'isuse':row[10]
            }
            allOrdertables.append(ordertable)
        cursor.close()
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({'message':'查询红包失败,请联系服务器人员', 'status':'error'}), content_type="application/json")

        

# 商品添加接口 已完成
def goodsManageJsonAdd(request):
    datas = request.POST
    goodsid = randomString()


    cursor = connection.cursor()

    xiaofenleiId = ""

    sql = "INSERT INTO goods ("
    
    for item in datas:
        if item == "bigClassiData" or item == "minClassiData" or item == 'paramsType' or item == 'params1Type' or item == 'file':
            pass;
        else :
            # if item == "xiaoClassiData":
            #     xiaofenleiStr = "select id from minfenlei where name='%s'" % datas[item]
            #     cursor.execute(xiaofenleiStr)
            #     xiaofenleiResult = cursor.fetchall()
            #     for oneItem in xiaofenleiResult:
            #         xiaofenleiId = oneItem[0]
            sql = sql + item + ","
        
    sql = sql + "goodsid) values ("
    for key in datas:
        if key == "bigClassiData" or key == "minClassiData" or key == 'paramsType' or key == 'params1Type' or key == 'file':
            pass
        else :
            # oneValue = ""
            oneValue = datas[key]
            # if key == "xiaoClassiData":
            #     oneValue = xiaofenleiId
            # else:
            #     oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        
        
    sql = sql + "'" + goodsid + "'" ")"

    try:
        
        result = cursor.execute(sql)  
        cursor.close();  
        if result == 1:
            
            # statusDic=MyTool.resultOk("添加成功")
            statusDic = {"status":"ok" , "message":"添加成功" , "goodsid":goodsid}
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else :
            
            statusDic=MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:
        raise e  
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");

def getShangjiaGoodsListFn():
    cursor = connection.cursor()
    sqlStr = "select * from goods where status = '1'"
    
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    cursor.close()
    data = []
    for row in rows:
        oneData = goodsDataRowToDic(row)
        data.append(oneData)
    return data
    

# 查询已上架的商品列表 供移动端使用 已完成
def getShangjiaGoodsList(request):
    try:
        # pageNumber = request.GET.get("page" , 0)
        # startNumber = int(pageNumber) * 20
        data = getShangjiaGoodsListFn()
        return HttpResponse(json.dumps({'data':data, 'status':'ok'}), content_type="application/json")
    except Exception as e: 
        return HttpResponse(json.dumps({'message':'已上架商品列表接口异常，请联系服务器管理人员', 'status':'error'}), content_type="application/json");
# 商品列表接口 已完成
def goodsManageJsonSelect(request):
    myData=[];
    mypage = 0
    mypage = (int(request.GET["page"]) - 1) * 10
    cursor = connection.cursor();
    cursor.execute("SELECT * FROM goods LIMIT %d , 10"%mypage);
    datas=cursor.fetchall();
    try:
        for row in datas:
            goods = goodsDataRowToDic(row)
            myData.append(goods);
        cursor.close();
        cursor = connection.cursor();
        cursor.execute("SELECT COUNT(*) FROM goods")
        goodscount  = cursor.fetchall();
        goodscount = goodscount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'goodscount':str(goodscount) }), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");
# 根据分类 查询商品 已完成
def getGoodsByClassify(request):
    try:
        allGoodMes = []
        bigClassifyName = request.POST["bigClassifyName"]
        minClassifyName = request.POST["minClassifyName"]
        classifyName = bigClassifyName + "-" + minClassifyName
        sql = "SELECT * FROM goods WHERE standard like '%s'" % classifyName
        cursor = connection.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():
            goods = goodsDataRowToDic(row)
            allGoodMes.append(goods)
            
        cursor.close()
        return HttpResponse(json.dumps({'data':allGoodMes, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'message':"根据分类查询商品异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json")

# 根据多个商品id获取多个商品信息 已完成
def getGoodsByManyGoodsid(request):
    try:
        goodsArr = request.POST.getlist("goodsidArr")
        sqlStr = "SELECT * from goods where goodsid in ("
        for item in goodsArr:
            sqlStr = sqlStr + "'" + item + "',"
        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"


        cursor = connection.cursor()
        cursor.execute(sqlStr)

        resultData = []
        for row in cursor.fetchall():
            goods = goodsDataRowToDic(row)
            resultData.append(goods) 

        cursor.close()

        return HttpResponse(json.dumps({'data':resultData, 'status':'ok'}), content_type="application/json")
          

    except Exception as e:
        raise e
        return HttpResponse(json.dumps({'message':"根据分类查询商品异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json")



# 在搜索框列表上选中之后的的查询方法 已完成
def getGoodsListByQueryString (request):
    try:
        resultData = []
        queryStr = request.POST["queryStr"]
        fieldName = request.POST["fieldName"]


        cursor = connection.cursor()
        sqlStr = "select * from goods where " + fieldName + " like '%%%%%s%%%%'" % queryStr


        if fieldName == 'keywords' or fieldName == 'goodsname':
            sqlStr = "SELECT * FROM goods where concat(goodsname , product_brief_info , shopname , product_brand , keywords) like '%%%%%s%%%%'" % (queryStr)
     

        if fieldName == "standard":
            sqlStr = "SELECT * FROM goods where xiaoClassiData in (select id from minfenlei where concat(name , bigName , midName) like '%%%%%s%%%%')" % queryStr

        cursor.execute(sqlStr)
        for row in cursor.fetchall():
            goods = goodsDataRowToDic(row)
            resultData.append(goods) 

        cursor.close()

        return HttpResponse(json.dumps({'data':resultData, 'status':'ok'}), content_type="application/json")
                
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({'message':"商品移动端列表选中后的模糊查询失败,请联系服务器管理人员", 'status':'error'}), content_type="application/json")
# 商品模糊查询 供移动端使用 已完成
def getGoodsBySomething(request):
    try:
        resultData = []
        queryStr = request.POST["queryStr"]
        fieldName = request.POST["fieldName"]

        cursor = connection.cursor()
        sqlStr = "select " + fieldName + " from goods where " + fieldName + " like '%%%%%s%%%%'" % queryStr

        if fieldName == "standard":
            sqlStr = "select name , bigName , midName from minfenlei where concat(name , bigName , midName) like '%%%%%s%%%%'" % queryStr


        cursor.execute(sqlStr)
        for row in cursor.fetchall():

            getString = row[0]

            if fieldName == "standard":
                getString = row[1] + "-" + row[2] + "-" + row[0]
            # getString = getString[getString.index(queryStr):]
            resultData.append(getString) 

        cursor.close()

        # 数组去重
        resultData = list(set(resultData))

        return HttpResponse(json.dumps({'data':resultData, 'status':'ok'}), content_type="application/json")
                
    except Exception as e:
        return HttpResponse(json.dumps({'message':"商品移动端模糊查询失败,请联系服务器管理人员", 'status':'error'}), content_type="application/json")

# 添加商品原始图 图片 缩略图 已完成
def addGoodsSomeImage(request):
    try:
        goodsid = request.POST.get("goodsid" , "")
        imgs = request.FILES.get("imgsFile" , "")
        columnName = request.POST.get("columnName" , "")

        if goodsid == "" or imgs == "" or columnName == "":
            return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type = "application/json");
        
        imgsName = randomString() + ".jpg";
        filepath = "./shopApp/static/myfile/goodsImage/";
        filename = os.path.join(filepath,imgsName)
        filehandle = open(filename , "wb");
        filehandle.write(imgs.__dict__["file"].read());
        sqlfilename = 'static/myfile/goodsImage/' + imgsName

        cursor = connection.cursor();


        # 删除原来的图片
        selectSqlStr = "select %s from goods where goodsid='%s'" % (columnName , goodsid)
        cursor.execute(selectSqlStr)
        rows = cursor.fetchall()
        for tempimg in rows:
            if os.path.exists("../shopServer/shopApp/"+tempimg[0])==True:
                os.remove("../shopServer/shopApp/"+tempimg[0]);



        sqlStr = "update goods set %s='%s' where goodsid='%s'" % (columnName , sqlfilename , goodsid)
        result=cursor.execute(sqlStr);
        

        


        cursor.close()

        if result >= 1:
            
            return HttpResponse(json.dumps({'status':'ok' , 'message':'添加图片成功'}) , content_type = "application/json");
        else :
            
            return HttpResponse(json.dumps({'status':'error' , 'message':'添加图片失败'}) , content_type = "application/json");
    except Exception as e: 
        raise e
        return HttpResponse(json.dumps({'status':'error' , 'message':'商品图添加操作失败，请联系服务器管理人员'}) , content_type = "application/json");


# 工具方法 根据商品id 删除 推荐商品中的数据
def deleteRecommends(goodsidArr):
    cursor = connection.cursor()
    imgArr = []
    sqlStr = "select recomendImg FROM recommendGoods WHERE goodsid in ("
    for goodsid in goodsidArr:
        sqlStr = sqlStr + "'" + goodsid + "' ,"

    sqlStr = sqlStr[0:-1]
    sqlStr = sqlStr + ")"
    
    cursor.execute(sqlStr);
    imgRows = cursor.fetchall()
    for row in imgRows:
        imgArr.append(row[0])

    for imgPath in imgArr:
        removePath = "../shopServer/shopApp" + imgPath
        os.remove(removePath);

    sqlStr = "delete FROM recommendGoods WHERE goodsid in ("
    for goodsid in goodsidArr:
        sqlStr = sqlStr + "'" + goodsid + "' ,"

    sqlStr = sqlStr[0:-1]
    sqlStr = sqlStr + ")"
    
    cursor.execute(sqlStr);
    cursor.close()

    
    



# 商品列表删除接口 已完成
def goodsManageJsonDelete(request):
    try:
        goodsidsDict =  request.POST
        goodsids = goodsidsDict.getlist("goodsids")

        cursor=connection.cursor();
        result = 0
        images = goodsidsDict.getlist("images")
        for imgPath in images:
            removePath = "../shopServer/shopApp/static/myfile/" + imgPath
            if os.path.exists(removePath)==True:
            
                os.remove(removePath);
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({"message":'有关图片删除操作异常' , "status":"error"}) , content_type="application/json");


    try:
        for goodsid in goodsids:
            cursor.execute("DELETE FROM lucky where goodsid = '%s'"%(goodsid))
            cursor.execute("DELETE FROM secondkill where goodsid = '%s'"%(goodsid))
            deleteRecommends([goodsid])
            result += cursor.execute("DELETE FROM goods where goodsid = '%s'"%(goodsid))
            # 删除轮播图表中的数据和图片
            deleteLunboInfoByGoodsId(goodsid)
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

    except Exception as e:  
        raise e 
        return HttpResponse(json.dumps({"message":'商品删除操作异常' , "status":"error"}) , content_type="application/json");
# 工具方法: 根据 goodsid 获取商品详情 已完成
def getGoodsDetailByGoodsid(goodsid):
    sqlStr = "SELECT * FROM goods WHERE goodsid = '%s'" % goodsid
    goods = {}
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    for row in cursor.fetchall():
        goods = goodsDataRowToDic(row)
    cursor.close()
    return goods

#商品详情列表展示 有待测试 吕健威 已完成 新方法 
# 等所有请求都用成这个方法了 就把下面的goodsSelectByid这个方法删掉
def goodsSelectByidNew(request):
    goodsid = request.POST.get("goodsid" , "")
    wxid = request.POST.get("wxid" , "")
    tablename = request.POST.get("tablename" , "")
    myData = {}

    if goodsid == "":
        return HttpResponse(json.dumps({'message':'缺少商品id', 'status':'error'}), content_type="application/json")


    
    if wxid == "" or tablename == "":
        myData['shoucang_list'] = []
        myData['pinglun_list'] = []
    else :
        myData['shoucang_list'] = favoriteAndLookTableManageJsonSelectFn(wxid , tablename)
        current_data = commentJsonQueryFn(wxid , goodsid)
        myData['pinglun_list'] = current_data['myData']


    myData['goods'] = getGoodsDetailByGoodsid(goodsid)
    
    return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")

# 积分商城列表接口 已完成
def jifenListJson(request):

    try:
        page = request.POST.get("page" , 1)
        if int(page) <= 1:
            page = 1
        start = (int(page) - 1) * 10

        sortType = request.POST.get("sortType" , "jifenprice")
        sortDirection = request.POST.get("sortDirection" , "desc")
        if sortType == "goodsname":
            sortType = "CONVERT(goodsname USING gbk)"
        if sortType == "jifenprice":
            sortType = "CONVERT(jifenprice,SIGNED)"
        sqlStr = "select * from goods where CONVERT(jifenprice,SIGNED) > 0 order by %s %s limit %d , 10" % (sortType , sortDirection , int(start))
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        goodsList = []
        for row in rows:
            oneGoods = goodsDataRowToDic(row)
            goodsList.append(oneGoods)

        cursor.execute("SELECT COUNT(*) FROM goods where CONVERT(jifenprice,SIGNED) > 0")
        goodscount  = cursor.fetchall();
        cursor.close()
        goodscount = goodscount[0][0]

        return HttpResponse(json.dumps({'data':goodsList, 'status':'ok' ,'count':goodscount }), content_type="application/json")
    

    except Exception as e:   
        raise e
        return HttpResponse(json.dumps({'message':'积分商城列表接口异常，请联系服务器管理人员', 'status':'error'}), content_type="application/json");

# 积分批量删除接口
def deleteManyJifenprice(request):
    try:
        goodsArr = request.POST.get("goodsids" , "[]")
        goodsArr = json.loads(goodsArr)
        sqlStr = "UPDATE goods SET jifenprice = '0' WHERE goodsid in ( "
        for goodsid in goodsArr:
            sqlStr = sqlStr + "'" + goodsid + "',"

        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"

        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        cursor.close()
        if result >= 1:
            return HttpResponse(json.dumps({'message':'积分更新成功', 'status':'ok'}), content_type="application/json");
        else:
            return HttpResponse(json.dumps({'message':'积分更新失败', 'status':'error'}), content_type="application/json");


    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'message':'商品列表异常，请联系服务器管理人员', 'status':'error'}), content_type="application/json");


# 商品模糊查询接口 黄景召 胡亚洲改 已完成
def commodityQuery(request):
    
    try:
        myData = []
        mypage = (int(request.POST.get("page" , 1)) - 1) * 10
        commName = request.POST.get("commName" , "")
        sortType = request.POST.get("sortType" , "addtime")
        sortDirection = request.POST.get("sortDirection" , "desc")

        clientType = request.POST.get("clientType" , "phone")

        if sortType == "goodsname":
            sortType = "CONVERT(goodsname USING gbk)"

        if sortType == "jifenprice":
            sortType = "CONVERT(jifenprice,SIGNED)"

        fromStr = request.POST.get("from" , " ")
        if fromStr == "jifenshangcheng":
            fromStr = " CONVERT(jifenprice,SIGNED) > 0 and "


        sqlStr = "SELECT * FROM goods where" + fromStr + "concat(goodsname , product_brief_info , shopname , product_brand , keywords) like '%%%%%s%%%%' order by %s %s LIMIT %d , 10" % (commName , sortType , sortDirection , mypage)
        

        if clientType == "phone":
            sqlStr = "SELECT * FROM goods where" + fromStr + "status='1' and concat(goodsname , product_brief_info , shopname , product_brand , keywords) like '%%%%%s%%%%' order by %s %s LIMIT %d , 10" % (commName , sortType , sortDirection , mypage)
        

        cursor = connection.cursor()
        cursor.execute(sqlStr);
        datas = cursor.fetchall()

        for row in datas:
            goods = goodsDataRowToDic(row)
            myData.append(goods);
        
        if clientType == "phone":
            cursor.execute("SELECT COUNT(*) FROM goods where" + fromStr + "status='1' and concat(goodsname , product_brief_info , shopname , product_brand , keywords) like '%%%%%s%%%%'" % (commName))
        else:
            cursor.execute("SELECT COUNT(*) FROM goods where" + fromStr + "concat(goodsname , product_brief_info , shopname , product_brand , keywords) like '%%%%%s%%%%'" % (commName))
        goodscount  = cursor.fetchall();
        goodscount = goodscount[0][0]
        cursor.close();

        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'count':goodscount }), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'message':'商品列表异常，请联系服务器管理人员', 'status':'error'}), content_type="application/json");
# 商品修改列表修改接口 有待测试 黄景召 已完成
def goodsManageJsonUpdata(request):

    datas = request.POST
    goodsid = request.POST.get("goodsid" , "")
    if goodsid == "":
        return HttpResponse(json.dumps({"message":"商品参数传入失败"}) , content_type = "application/json");

    cursor = connection.cursor()

    xiaofenleiId = ""

    sql = "update goods set "
    
    for item in datas:
        if item == "bigClassiData" or item == "minClassiData" or item == "goodsid" or item == "params1Type" or item == "paramsType" or item == "file":
            pass;
        else :
            sql = sql + item + "='" + datas[item] + "',"
        
    sql = sql[0:-1]
    sql = sql + " where goodsid='" + goodsid + "'"


    try:
        result = cursor.execute(sql)  
        cursor.close(); 
        if result == 1:
            
            statusDic=MyTool.resultOk("修改成功")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else :
            
            statusDic=MyTool.resultError("修改失败")
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:
        raise e  
        return HttpResponse(json.dumps({'message':"商品更新操作异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json");


# 修改商品的一些参数 已完成
def modifyGoodsSomeNumber(request):
    try:
        goodsid = request.POST["goodsid"]
        optionNumber = request.POST["optionNumber"]
        optionName = request.POST["optionName"]


        optionNumber = json.loads(optionNumber)
        optionName = json.loads(optionName)

        sqlStr = "update goods set "

        addOrSubtraction = "+" 

        for index , item in enumerate(optionName):
            if item == "counts":
                addOrSubtraction = "-"
            else:
                addOrSubtraction = "+"

            sqlStr = sqlStr + item + " = " + item + addOrSubtraction + str(optionNumber[index]) + ","
        sqlStr = sqlStr[0:-1]

        sqlStr = sqlStr + " where goodsid = '%s'" % goodsid

        cursor = connection.cursor()
        cursor.execute(sqlStr)

        return HttpResponse(json.dumps({'message':'更新成功', 'status':'ok'}), content_type="application/json")


    except Exception as e:    
        return HttpResponse(json.dumps({'message':'修改商品一些参数的操作异常,请联系服务器管理人员', 'status':'error'}), content_type="application/json");


# 给商品添加运单号接口
def addTransportId(request):
    try:
        orderTableId = request.POST.get("orderTableId" , "")
        goodsId = request.POST.get("goodsId" , "")
        transportId = request.POST.get("transportId" , "")

        if orderTableId == "" or goodsId == "" or transportId == "":
            return HttpResponse(json.dumps({'message':'参数出错', 'status':'error'}), content_type="application/json");

        nowTime = datetime.datetime.now();
        nowTime = nowTime + datetime.timedelta(hours = 8)
        nowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")

        sqlStr = "update order_goods_table set transportId='%s' , status = 2 , \
        fahuotime = '%s' where orderTableId='%s' and goodsid='%s'" % (transportId , nowTime , orderTableId , goodsId)
        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        cursor.close()
        
        if result >= 1:
            return HttpResponse(json.dumps({'message':'更新成功', 'status':'ok' , 'data':{'fahuoTime': nowTime} }), content_type="application/json");
        else :
            return HttpResponse(json.dumps({'message':'更新失败', 'status':'error'}), content_type="application/json");


    except Exception as e:    
        raise e
        return HttpResponse(json.dumps({'message':'修改商品一些参数的操作异常,请联系服务器管理人员', 'status':'error'}), content_type="application/json");



# 订单添加接口 已完成
def ordertableManageJsonAdd(request):
    try:
        cursor = connection.cursor()
        resultData = {}

        orderid = randomString()
        wxid = request.POST.get("wxid" , "")

        goodsIdArr = request.POST.get("goodsIdArr" , [])
        transportMethod = request.POST.get("transportMethod" , "微信支付")
        invoiceType = request.POST.get("invoiceType" , "")
        invoiceContent = request.POST.get("invoiceContent" , "")
        deliveryTime = request.POST.get("deliveryTime" , "")  # 配送时间
        noGoodsMethod = request.POST.get("noGoodsMethod" , "")  # 缺货处理
        sendCompany = request.POST.get("sendCompany" , "申通")
        addressId = request.POST.get("addressId" , 1)
        status = request.POST.get("status" , 0)

        

        resultData["orderId"] = orderid
        resultData["userInfo"] = {}
        resultData["status"] = 0
        resultData["goodsInfo"] = [] 

        nowTime = datetime.datetime.now();
        nowTime = nowTime + datetime.timedelta(hours = 8)
        nowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")

        resultData['createTime'] = nowTime
        
        resultData['payTime'] = ""
        resultData['wxOrderId'] = ""
        resultData["transportMethod"] = transportMethod
        resultData["invoiceType"] = invoiceType
        resultData["invoiceContent"] = invoiceContent
        resultData["deliveryTime"] = deliveryTime
        resultData["noGoodsMethod"] = noGoodsMethod
        resultData["sendCompany"] = sendCompany
        
        resultData["userAddress"] = getAddressByAddressid(addressId)


        goodsIdArr = json.loads(goodsIdArr)

        # 查看用户是否是首单
        oneUserInfo = getUserDetailByWxid(wxid)
        isShouDan = False
        if len(oneUserInfo) > 0:
            
            resultData["userInfo"] = oneUserInfo
            isFirstBuy = oneUserInfo["isFirstBuy"]
            if int(isFirstBuy) == 0:
                cursor.execute("update user set isFirstBuy=1 where wxid='%s'" % wxid)
                isShouDan = True
        else:
            tempDic = json.dumps({'status':'error','message':'对不起,没有改用户'})
            return HttpResponse(tempDic, content_type="application/json")


        # 判断用户有没有这个地址
        isHaveThisAddress = False
        addressArr = getAddressListByWxid(wxid)
        for item in addressArr:
            if item.get("addid" , "") == addressId:
                isHaveThisAddress = True
                break
        if isHaveThisAddress == False:
            tempDic = json.dumps({'status':'error','message':'对不起,该用户没有这个地址编号'})
            return HttpResponse(tempDic, content_type="application/json")

        originFreightPrice = 0
        freightRiskPrice = 0
        freightPrice = 0
        comment = ""
        totalMoney = 0
        totalNum = 0
        for oneGoodsInfo in goodsIdArr:
            oneGoodsId = oneGoodsInfo.get("goodsId" , "")
            oneGoodsNum = oneGoodsInfo.get("goodsNum" , 1)
            oneGoodsParams = oneGoodsInfo.get("goodsParams" , "")

            oneGoodsMoney = oneGoodsInfo.get("goodsMonery" , 0)
            oneGoodsFreightPrice = oneGoodsInfo.get("freightPrice" , 0)
            oneGoodsFreightRiskPrice = oneGoodsInfo.get("freightRiskPrice" , 0)

            order_goods_table_sqlStr = "insert into order_goods_table (orderTableId , goodsid , goodsNumber , params , status) values ('%s' , '%s' , '%s' , '%s' , %d)" % (orderid , oneGoodsId , oneGoodsNum , oneGoodsParams , int(status))
            cursor.execute(order_goods_table_sqlStr)
            
            oneGoods = getGoodsDetailByGoodsid(oneGoodsId)
            oneGoodsDic = {
                "goods":oneGoods , 
                "buyNumber":oneGoodsNum , 
                "params":oneGoodsParams,
                "is_pingjia": 0,
                'orderTableId': orderid,
                'status': status,
                'transportId': ''
            }
            resultData["goodsInfo"].append(oneGoodsDic)

            # totalNum计算
            totalNum = totalNum + int(oneGoodsNum)
            # totalMoney计算
            totalMoney = totalMoney + float(oneGoods['shop_price']) * int(oneGoodsNum)
            # 运费计算
            originFreightPrice = originFreightPrice + float(oneGoods['transportmoney']) * int(oneGoodsNum)
            # 运费险计算
            freightRiskPrice = freightRiskPrice + float(oneGoodsFreightRiskPrice) * int(oneGoodsNum)

        freightPrice = originFreightPrice
        if originFreightPrice >= 20:
            freightPrice = 0
            comment = "满20元,免运费"
        if isShouDan == True:
            freightPrice = 0
            comment = "收单免运费"


        wxRes = getWxPayidFn({
            'body': '嘉福祥-在线商城' , 
            'orderid': orderid , 
            'totalMoney': totalMoney , 
            'wxid': wxid , 
            'nonce_str': orderid + 'abc'
        })
        if wxRes['xml']['return_code']['$'] == 'SUCCESS':
            order_table_sqlStr = "insert into ordertable \
            (wxid , orderId , freightPrice , freightRiskPrice , \
            payTime , addressId , wxOrderId , transportMethod , \
            invoiceType , invoiceContent , deliveryTime , noGoodsMethod , \
            sendCompany , fahuoTime , originFreightPrice , comment , \
            status) \
            values ('%s' , '%s' , '%s' , '%s' , \
            '%s' , '%s' , '%s' , '%s' , \
            '%s' , '%s' , '%s' , '%s' , \
            '%s' , '%s' , '%s' , '%s' , \
            %d)" % (wxid , orderid , freightPrice , freightRiskPrice , "" , addressId , wxRes['xml']['prepay_id']['$'] , transportMethod , invoiceType , invoiceContent , deliveryTime , noGoodsMethod , sendCompany , "" , originFreightPrice , comment , int(status))
            cursor.execute(order_table_sqlStr)
            cursor.close()

            resultData['originFreightPrice'] = originFreightPrice
            resultData["freightRiskPrice"] = freightRiskPrice
            resultData["freightPrice"] = freightPrice
            resultData["comment"] = comment
            resultData["totalMoney"] = totalMoney
            resultData["totalNum"] = totalNum
            resultData['wxOrderId'] = wxRes['xml']['prepay_id']['$']
            return HttpResponse(json.dumps({'status':"ok" , 'data':resultData}), content_type="application/json")
        else :
            return HttpResponse(json.dumps({'status':"error" , 'message':'下订单失败' , 'data': wxRes}), content_type="application/json")

        
    except Exception as e:
        raise e
        tempDic = json.dumps({'status':'error','message':'订单添加接口异常,请联系服务器人员'})
        return HttpResponse(tempDic, content_type="application/json")

# 根据订单id查询订单信息
def getDingdanByDingdanid (request):
    
    orderId = request.POST.get("orderId" , "")
    if orderId == "":
        return HttpResponse(json.dumps({'status':'error','message':'参数有误'}), content_type="application/json")

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ordertable where orderId = '%s'" % orderId)
    dingdanList = orderRows_to_orderData(cursor.fetchall())
    return HttpResponse(json.dumps({'status':'ok','data':dingdanList}), content_type="application/json")
    
def getCommimgFn(commImgId):
    cursor = connection.cursor()
    cursor.execute("select * from commImg where commId = '%s'" % commImgId)
    rows = cursor.fetchall()
    cursor.close()
    img_arr = []
    for row in rows:
        temp_dic = {
            'comImgId': row[0],
            'commId': row[1],
            'img': row[2],
        }
        img_arr.append(temp_dic)
    return img_arr

# 订单查询列表接口 已完成 移动端
def ordertableListJson(request):
    try:
        wxid = request.POST.get("wxid" , "")

        fromType = request.POST.get("from" , "phone")

        commonName = request.POST.get("commonName" , "")

        orderStatus = request.POST.get("orderStatus" , "")

        transportId = request.POST.get("transportId" , "")

        page = request.POST.get("page" , 1)
        if int(page) <= 1:
            page = 1
        start = (int(page) - 1) * 10

        sortType = request.POST.get("sortType" , "createTime")
        sortDirection = request.POST.get("sortDirection" , "desc")

        sqlStr = "select * from ordertable where wxid = '%s' order by %s %s limit %d , 10" % (wxid , sortType , sortDirection , start)
        if fromType == "server":
            sqlStr = "select ordertable.wxid , ordertable.orderId , ordertable.createTime , ordertable.status , ordertable.freightPrice , ordertable.freightRiskPrice , ordertable.payTime , ordertable.addressId , ordertable.wxOrderId , ordertable.transportMethod , ordertable.invoiceType , ordertable.invoiceContent , ordertable.deliveryTime , ordertable.noGoodsMethod , ordertable.sendCompany from ordertable inner join user on ordertable.wxid=user.wxid and user.username like '%%%%%s%%%%' and ordertable.status like '%%%%%s%%%%' order by %s %s limit %d , 10" % (commonName , orderStatus , sortType , sortDirection , start)
            if transportId != "":
                sqlStr = "select ordertable.wxid , ordertable.orderId , ordertable.createTime , ordertable.status , ordertable.freightPrice , ordertable.freightRiskPrice , ordertable.payTime , ordertable.addressId , ordertable.wxOrderId , ordertable.transportMethod , ordertable.invoiceType , ordertable.invoiceContent , ordertable.deliveryTime , ordertable.noGoodsMethod , ordertable.sendCompany from ordertable inner join order_goods_table on ordertable.orderId=order_goods_table.orderTableId and order_goods_table.orderTableId='%s'" % (transportId)
        allOrdertables = [];
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        for row in cursor.fetchall():
            ordertable = {
                'orderId':row[1],
                'userInfo':{} , # row[0]
                'status':row[3],
                'goodsInfo':[] , 
                'createTime':MyTool.none_or_strftime(row[2]),
                'freightPrice':row[4],
                'freightRiskPrice':row[5],
                'payTime':row[6],
                'userAddress':{} , #  row[8], 
                'wxOrderId':row[8],
                'transportMethod':row[9],
                'invoiceType':row[10],
                'invoiceContent':row[11],
                'deliveryTime':row[12],
                'noGoodsMethod':row[13],
                'sendCompany':row[14]
            }
            goodsInfoArrResult = getGoodsInfoArrByOrderId(row[1])
            ordertable["goodsInfo"] = goodsInfoArrResult.get("goodsArr" , [])
            ordertable["userInfo"] = getUserDetailByWxid(row[0])
            ordertable["userAddress"] = getAddressByAddressid(row[7])
            ordertable["totalMoney"] = goodsInfoArrResult.get("totalMoney" , 0)
            ordertable["totalFreightMoney"] = goodsInfoArrResult.get("totalFreightMoney" , 0)
            ordertable["totalNum"] = goodsInfoArrResult.get("totalNum" , 0)
            


            
            allOrdertables.append(ordertable)
        

        if fromType == "server":
            cursor.execute("SELECT COUNT(*) FROM ordertable inner join user on ordertable.wxid=user.wxid and user.username like '%%%%%s%%%%' and ordertable.status like '%%%%%s%%%%'" % (commonName , orderStatus))
        else:
            cursor.execute("SELECT COUNT(*) FROM ordertable where wxid='%s'" % wxid)
        goodscount  = cursor.fetchall();
        cursor.close()
        goodscount = goodscount[0][0]
        
        return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok' , 'count':goodscount}), content_type="application/json")
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({'message':"订单查询接口异常,请联系服务器管理人员", 'status':'error'}), content_type="application/json")
# 订单删除接口 已完成
def ordertableDelete(request):
    try:
        orderId = request.POST["orderId"]
        cursor=connection.cursor();
        result = cursor.execute("DELETE FROM ordertable WHERE orderid ='%s'" % orderId)
        cursor.close();
        if result == 1:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
        else:
            return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");
    except Exception as e:
        return HttpResponse(json.dumps({'message':"订单表删除异常,请联系服务器人员", 'status':'error'}), content_type="application/json")
# 修改订单状态
def modify_order_status(request):
    try:
        orderTableId = request.POST.get("orderTableId" , "")
        sta = request.POST.get("status" , 0)
        sta = int(sta)

        if orderTableId == "" or sta == "":
            return HttpResponse(json.dumps({'message':'参数错误', 'status':'error'}), content_type="application/json");

        sqlStr = "update ordertable set status=%d where orderId='%s'" % (sta , orderTableId)

        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        cursor.close()

        if result == 1:
            # if sta == "待收货":
            #     cursor = connection.cursor()
            #     nowTime = datetime.datetime.now();
            #     nowTime = nowTime + datetime.timedelta(hours = 8)
            #     nowTime = nowTime.strftime("%Y-%m-%d %H:%M:%S")
            #     cursor.execute("update ordertable set fahuoTime = '%s' where orderId = '%s'" % (nowTime , orderTableId))
            #     cursor.close()
            return HttpResponse(json.dumps({'message':'操作成功', 'status':'ok'}), content_type="application/json");
        else :
            return HttpResponse(json.dumps({'message':'操作失败', 'status':'error'}), content_type="application/json");
    except Exception as e:
        raise e;
        return HttpResponse(json.dumps({'message':'订单取消接口异常，请联系服务器管理人员', 'status':'error'}), content_type="application/json");

#图片上传并返回拼接地址   韩乐天
def imgUpload(request):
    uf = UserForm(request.POST,request.FILES)
    test = imagesupload();
    imgpath = test.upload(request)
    return render_to_response('test.html',{'uf':uf})


# 上传图片到服务器接口
def uploadImage(request):
    resultData = {"errno":0 , "data":[]}
    for key in request.FILES:

        imgs = request.FILES[key];
        imgName = randomString()

        imgName = imgName + ".jpg"; 
        filepath = "./shopApp/static/myfile/uploadImage/";
        filepath = filepath + imgName

        
        fileHandle = open(filepath , "wb");
        fileHandle.write(imgs.__dict__["file"].read());
        fileHandle.close();
        resultData["data"].append("http://" + my_global_host_url + "/static/myfile/uploadImage/" + imgName)

    return HttpResponse(json.dumps(resultData),content_type="application/json")


# 活动删除接口 有待测试 刘斌 已完成
def activetableManageJsonDelete(request):
    cursor=connection.cursor()
    active_id = request.GET["dataId"];
    try:
        cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % active_id)
        data = cursor.fetchall();
        if data[0][0]:
            tempimg = data[0][0];
            if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
            else:
                pass;
        cursor.execute("DELETE FROM activetable WHERE activeid='%s'"% (active_id))
        cursor.close()
        return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
    except expression as identifier:
        return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
def redpack(request):
    
    return render(request,"redpack.html")
# 活动批量删除接口 胡亚洲
def activesManageJsonDelete(request):
    activeidsDict =  request.POST
    activeids = activeidsDict.getlist("activeids")
    cursor=connection.cursor();
    result = 0
    try:
        for activeid in activeids:
            cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % activeid)
            data = cursor.fetchall();
            if data[0][0]:
                tempimg = data[0][0];
                if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                    os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
                else:
                    pass;
            result += cursor.execute("DELETE FROM activetable where activeid = '%s'"%(activeid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");

    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
# 活动查询接口  有待测试
def activeManageJsonSelect(request):
    
    try:
        myData=[]
        cursor=connection.cursor()

        cursor.execute("SELECT * FROM activetable")
        for data in cursor.fetchall():
            tempDic={
                "activeid":data[0],
                "activedetail":data[1],
                "starttime":MyTool.none_or_strftime(data[2]),
                "imgs":data[3],
                "stoptime":MyTool.none_or_strftime(data[4]),
                "activeAddress":data[5], 
                "activeName":data[6],
                "activePosition":data[7]
            }
            myData.append(tempDic);
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:   
        # raise e
        return HttpResponse(json.dumps({"data":myData , "status":"error"}) , content_type="application/json");
# 活动添加接口 刘斌
def activetableManageJsonAdd(request):
    datas = request.POST
    imagesName = "None"
    #前台传过来的图片
    if request.FILES.get('imgs',False):
        images = request.FILES["imgs"];
        #随机字符串存取图片名字
        imagesName = randomString() + ".jpg";
        #判断是否存在
        if os.path.exists("../shopServer/shopApp/static/myfile/"+imagesName)==True:
            os.remove("../shopServer/shopApp/static/myfile/"+imagesName);
        else:
            pass;
        filepath = "./shopApp/static/myfile/";
        #路径组合
        filepath = os.path.join(filepath,imagesName)
        #在路径中创建图片名字
        fileobj = open(filepath , "wb");
        #并把前端传过来的数据写到文件中
        fileobj.write(images.__dict__["file"].read());

        activeid = randomString()
        sql = "INSERT INTO activetable ("
        for item in datas:
            sql = sql + item + ","
        sql = sql[0:-1]    
        sql = sql +',activeid,imgs' ") values (";
        for key in datas:
            oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        sql = sql[0:-1]
        sql = sql +','+"'"+activeid+"','" + imagesName +"'" ")"

    else:
        activeid = randomString()
        sql = "INSERT INTO activetable ("
        for item in datas:
            sql = sql + item + ","
        sql = sql[0:-1]    
        sql = sql +',activeid' ") values (";
        for key in datas:
            oneValue = datas[key]
            sql = sql + "'" + oneValue + "',"
        sql = sql[0:-1]
        sql = sql +','+"'"+activeid+"'" ")"
          
    cursor=connection.cursor()
    try:
        cursor.execute(sql)
        cursor.execute("SELECT * FROM activetable WHERE activeid='%s'" %activeid)
        data = cursor.fetchall()[0]
        activeid=data[0]
        activedetail=data[1]
        starttime=MyTool.none_or_strftime(data[2])
        imgs = data[3]
        stoptime = MyTool.none_or_strftime(data[4])
        activetitle = data[5]
        activeName = data[6]
        activePosition = data[7]
        tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
        # cursor.execute("INSERT INTO order (activeid,activetime,activedetail) VALUES (%d,%s,%s)"% (activeid,str(activetime),activedetail))
        statusDic={"status":"ok","message":"添加成功","addactive":tempDic};
        
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except Exception as e :
        raise e
       
        statusDic=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");


#收藏 浏览记录 添加接口 已完成
def favoriteAndLookTableManageJsonAdd(request):
    try:
        wxid = request.POST["wxid"];
        goodsid = request.POST["goodsid"];
        tablename = request.POST["tablename"]  
        favoriteid = randomString()

        number = "" 
        idstring = ""
        sqlStr = ""
        if tablename == "favorite":
            idstring = "favoriteid"
        if tablename == "lookhistory":
            idstring = "lookid"  

        cursor=connection.cursor() 
        result = cursor.execute("select goodsid from " + tablename + " where goodsid='%s' and wxid='%s'" % (goodsid , wxid))

        if int(result) > 0:
            statusDic=MyTool.resultError("该商品已经存在")
            cursor.close()
            return HttpResponse(json.dumps(statusDic), content_type = "application/json");
        else :
            cursor.execute("insert into %s (wxid , %s , goodsid) values ('%s' , '%s' , '%s')" % (tablename , idstring , wxid , favoriteid , goodsid))
            cursor.close()
            return HttpResponse(json.dumps({"status":"ok" , "message":"添加成功" , "id":favoriteid}), content_type = "application/json");
    
    
    except Exception as e :
        raise e
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDic), content_type = "application/json");

def favoriteAndLookTableManageJsonSelectFn(wxid , tablename):
    myData=[]
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM %s where wxid='%s'"%(tablename , wxid))
    for data in cursor.fetchall():
        tempDic = {
            'wxid':data[0] , 
            'id':data[1] , 
            'goods':{} , 
            'addtime':MyTool.none_or_strftime(data[3])
        }
        
        tempDic['goods'] = getGoodsDetailByGoodsid(data[2])

        myData.append(tempDic);
    cursor.close()
    return myData

# 收藏 浏览记录 查询 接口 已完成
def favoriteAndLookTableManageJsonSelect(request):
    try:
        wxid = request.POST["wxid"];  
        tablename = request.POST["tablename"] 
        current_list = favoriteAndLookTableManageJsonSelectFn(wxid , tablename)
        return HttpResponse(json.dumps({'data':current_list, 'status':'ok'}),  content_type = "application/json");      
    except Exception as e:   
        return HttpResponse(json.dumps({"data":current_list , "status":"error"}) , content_type = "application/json");

# 购物车添加接口  已完成
def cartstableManageJsonAdd(request):   
    try: 
        cursor = connection.cursor()
        wxid = request.POST.get("wxid" , "");
        number = request.POST.get("number" , 0);
        goodsid = request.POST.get("goodsid" , "")
        params = request.POST.get("goodsparams" , "")
        cartsid = randomString()

        sqlStr = "select wxid from carts where wxid='%s'" % wxid
        result = cursor.execute(sqlStr)
        if result == 0:
            result = cursor.execute("INSERT INTO carts (wxid , cartsid , number , goodsid , params) VALUES ('%s' , '%s' , '%s' , '%s' , '%s')" % (wxid,cartsid , number , goodsid , params))   
            cursor.close()
            if result == 1:
                statusDic=MyTool.resultOk("添加成功")
                return HttpResponse(json.dumps(statusDic),content_type="application/json");
            else :
                statusDic=MyTool.resultError("添加失败")
                return HttpResponse(json.dumps(statusDic),content_type="application/json");
        else:

            result = cursor.execute("select number from carts where goodsid='%s' and wxid='%s'" % (goodsid , wxid))

            if result == 0:
                result = cursor.execute("INSERT INTO carts (wxid , cartsid , number , goodsid , params) VALUES ('%s' , '%s' , '%s' , '%s' , '%s')" % (wxid,cartsid , number , goodsid , params))   
                cursor.close()
                if result == 1:
                    statusDic=MyTool.resultOk("添加成功")
                    return HttpResponse(json.dumps(statusDic),content_type="application/json");
                else :
                    statusDic=MyTool.resultError("添加失败")
                    return HttpResponse(json.dumps(statusDic),content_type="application/json");
            else :
                
                cursor.execute("update carts set number = number + %d where goodsid = '%s' " % (int(number) , goodsid))
                cursor.close()
                statusDic=MyTool.resultOk("累加成功")
                return HttpResponse(json.dumps(statusDic),content_type="application/json");  
            
        
       
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":"购物车添加操作失败，请联系服务器人员","status":"error"}),content_type="application/json")
#购物车 浏览记录 收藏表 批量删除接口 已完成
def cartstableManageJsonDelete(request):
    try:
        cartsids = request.POST["ids"]
        tablename = request.POST["tablename"]
        idstring = ""
        if tablename == "carts":
            idstring = "cartsid"
        if tablename == "favorite":
            idstring = "favoriteid"
        if tablename == "lookhistory":
            idstring = "lookid"


        cartsids = json.loads(cartsids)
        cursor=connection.cursor()
        sqlStr = "delete from " + tablename + " where " + idstring + " in ("
        for item in cartsids:
            sqlStr = sqlStr + "'" + item + "',"
        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"
        result = cursor.execute(sqlStr)
        if result >= 1:
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
        else :
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")

    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")
#购物车修改数量接口   已完成
def cartstableManageJsonUpdate(request):
    try:
        cursor = connection.cursor();
        cartsid = request.POST["cartsid"];   
        number = request.POST["number"]
        result = cursor.execute("update carts set number='%s' where cartsid='%s'"%(number , cartsid))
        cursor.close();
        if result == 1:
            return HttpResponse(json.dumps({"message":"修改成功","status":"ok"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":"购物车查询操作失败，请联系服务器人员","status":"error"}),content_type="application/json")
#购物车查询接口  已完成
def cartstableManageJsonSelect(request):  
    wxid = request.POST["wxid"]
    if wxid == "":
        return HttpResponse(json.dumps({"message":"获取用户信息失败","status":"error"}),content_type="application/json")
    try:
        cursor = connection.cursor()
        myData = []
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM carts WHERE wxid='%s'" % wxid)
        datas = cursor.fetchall()
        cursor.close()
        for data in datas:
            tempDic = {
                'wxid':data[0] , 
                'cartsid':data[1] , 
                'number':data[2] , 
                'params':data[4] , 
                'goods':{}
            }
            tempDic['goods'] = getGoodsDetailByGoodsid(data[3])
            myData.append(tempDic)
        return HttpResponse(json.dumps(myData) , content_type="application/json");
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":"购物车查询操作失败，请联系服务器人员","status":"error"}),content_type="application/json")



#添加抽奖余额接口
def drawJsonAdd(request):  
    cursor = connection.cursor() 
    wxid = request.POST["wxid"];
    drawmoney = request.POST["drawmoney"];
    drawdetail = request.POST["drawdetail"];
    username = "11111"
    drawid = randomString();
    try:
        cursor.execute("INSERT INTO draw (wxid , drawmoney , username , drawdetail , drawid) VALUES ('%s' , '%s' , '%s' , '%s' , '%s')" % (wxid , drawmoney , username , drawdetail , drawid))
        statusDic=MyTool.resultOk("添加成功")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加失败");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#删除抽奖余额接口
def drawJsonDel(request):
    cursor = connection.cursor()
    wxid = request.POST["wxid"];
    drawid = request.POST["drawid"];   
    try:
        cursor.execute("DELETE FROM draw WHERE drawid=\"%s\""%drawid)
        statusDic=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#更新抽奖接口
def drawJsonUpdate(request):
    cursor = connection.cursor()
    datas = request.POST
    try:
        for key in list(datas):
            cursor.execute("update draw set %s='%s' where wxid='%s'"%(key , datas[key] , datas["wxid"]))
            statusDic=MyTool.resultOk("修改成功")
        return HttpResponse(json.dumps(statusDic) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
# 查询抽奖余额接口
def drawJsonQuery(request):
    cursor = connection.cursor()
    wxid = request.POST["wxid"]
    myData = []
    try:
        cursor.execute('SELECT * FROM draw WHERE wxid=\"%s\"' % wxid)
        datas = cursor.fetchall()
        for data in datas:
            wxid = data[0];
            drawmoney = data[1];
            drawtime = MyTool.none_or_strftime(data[2])
            username = data[3];
            drawid = data[4];
            drawdetail = data[5];
            tempDic = {"wxid":wxid , "drawmoney":drawmoney , "drawtime":drawtime ,"username":username , "drawid":drawid , "drawdetail":drawdetail}
            myData.append(tempDic)

        return HttpResponse(json.dumps(myData) , content_type="application/json");
    except:
        statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    pass



# 福袋管理页面 胡亚洲
def luckyManage(request):
    return render(request , "luckyManage.html");
# 随机获取一个福袋的接口  已完成
def getOneRandomFudai(request):
    try:
        sqlStr = "select * from lucky"
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        allcount = 0
        data = []
        for row in rows:
            allcount = allcount + int(row[2])
            oneRow = {
                "luckyId":row[0] , 
                "goodsInfo":row[1] , 
                "counts":row[2] 
            }
            oneRow["goodsInfo"] = getGoodsDetailByGoodsid(row[1])
            data.append(oneRow)

        randomNumber = random.randint(0 , allcount - 1)
        randomIndex = 0
        for index , oneData in enumerate(data):
            if randomNumber < int(oneData["counts"]):
                randomIndex = index
                break
            else:
                randomNumber = randomNumber - int(oneData["counts"])

        randomGoods = data[randomIndex]

        return HttpResponse(json.dumps({"status":"ok" , "data":randomGoods}),content_type="application/json");

    except Exception as e:
        raise e  
        return HttpResponse(json.dumps({'message':'随机获取福袋接口异常，请联系服务器管理人员', 'status':'error'}), content_type="application/json");
# 福袋模查询接口
def luckyManageJsonQuery(request):
    myData = []
    timeUP = request.GET.get("timeUp" , "0")
    commName = request.GET.get("commName" , "")
    cursor = connection.cursor()

    timeStatus = "desc"
    if timeUP == '1':
        timeStatus = "asc"

    sqlStr = ""
    
    if commName == "":
        sqlStr = "SELECT lucky.luckyid, lucky.goodsid, goods.goodsname, lucky.counts, goods.shop_price, lucky.uptime FROM goods,lucky where lucky.goodsid=goods.goodsid order by lucky.uptime %s" % timeStatus
    else :
        sqlStr = "SELECT lucky.luckyid, lucky.goodsid, goods.goodsname, lucky.counts, goods.shop_price, lucky.uptime FROM goods,lucky where lucky.goodsid=goods.goodsid and goods.goodsname like '%%%%%s%%%%' order by lucky.uptime %s"%(commName, timeStatus)
    
    cursor.execute(sqlStr);
    datas = cursor.fetchall()
    try:
        for row in datas:
            try:
                uptime = MyTool.none_or_strftime(row[5])
            except:
                uptime = "未知"
            lucky = {
                'luckyid':row[0],
                'goodsid':row[1],
                'goodsname':row[2],
                'counts':row[3],
                'price':row[4],
                'uptime':uptime,
            }
            myData.append(lucky);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:  
        raise e
        return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");
# 福袋列表删除接口 胡亚洲
def luckyManageJsonDelete(request):
    luckyidsDict =  request.POST
    luckyids = luckyidsDict.getlist("luckyids")
    goodsids = luckyidsDict.getlist("goodsids")
    cursor=connection.cursor();
    result = 0
    try:
        for (myindex , luckyid) in enumerate(luckyids):
            result += cursor.execute("DELETE FROM lucky where luckyid = '%s'"%(luckyid))
            cursor.execute("UPDATE goods SET isinfudai = 'false' WHERE goodsid = '%s'" % goodsids[myindex])
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    except Exception as e:   
        raise e
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
# 福袋修改列表修改接口 胡亚洲
def luckyManageJsonUpdata(request):
    num=request.POST["num"];
    luckyid=request.POST["luckyid"]
    try:
        cursor = connection.cursor()
        cursor.execute("update lucky set counts='%s' where luckyid='%s'"%(num , luckyid))
        data = {'data':'success', 'status':'ok'}
        return HttpResponse(json.dumps(data) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'修改失败' , "status":"error"}) , content_type="application/json");
# 福袋添加接口 胡亚洲
def luckyManageJsonAdd(request):
    try:
        goodsName = request.POST["goodsName"]
        goodsId = request.POST["goodsId"]
        counts = request.POST["counts"]
        luckyid = randomString()
        cursor = connection.cursor()
        sql = "INSERT INTO lucky (luckyid , counts , goodsid) VALUES('%s','%s','%s')" % (luckyid, counts , goodsId)
        result = cursor.execute(sql)
        
        if result == 1 :
            # 将商品的状态改变了 (isinfudai)
            cursor.execute("UPDATE goods SET isinfudai = 'true' WHERE goodsid = '%s'" % goodsId)
            cursor.close()

            statusDic = {"status" : "ok" , "message" : "添加成功"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
        else:
            cursor.close()
            statusDic = {"status" : "error" , "message" : "添加失败"};
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");
#通过商品号查询福袋数
def selectLuckyJsonByGoodsId(request):
    myData = []
    goodsidsDict =  request.POST
    goodsids = goodsidsDict.getlist("goodsids")
    try:
        for goodsid in goodsids:
            oneData = []
            cursor = connection.cursor();
            luckycount = cursor.execute("SELECT lucky.luckyid, lucky.goodsid, goods.goodsname, lucky.counts, goods.shop_price, lucky.uptime FROM goods,lucky where lucky.goodsid=goods.goodsid and goods.goodsid = '%s'" % (goodsid))
            datas = cursor.fetchall();
            for row in datas:
                try:
                    uptime = MyTool.none_or_strftime(row[5])
                except:
                    uptime = "未知"
                lucky = {
                    'luckyid':row[0],
                    'goodsid':row[1],
                    'goodsname':row[2],
                    'counts':row[3],
                    'price':row[4],
                    'uptime':uptime,
                }
                oneData = {
                    'luckyData':lucky,
                    'luckyCount':luckycount,
                }
            cursor.close();
            if luckycount > 0:
                myData.append(oneData)
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'luckycount':str(len(myData)) }), content_type="application/json")
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'goodscount':'0'}), content_type="application/json");

def commentJsonQueryFn(wxid , goodsid):
    myData = []
    sqlStr = ""
    # 查询所有评论
    if wxid == "" and goodsid == "":
        sqlStr = "select * from comment"

    # 按照商品id查询评论
    if wxid == "" and goodsid != "":
        sqlStr = "select * from comment where goodsid = '%s'" % goodsid
    
    # 按照用户id查询评论
    if wxid != "" and goodsid == "":
        sqlStr = "select * from comment where wxid = '%s'" % wxid

    # 按照用户id和商品id来查找评论
    if wxid != "" and goodsid != "":
        sqlStr = "select * from comment where wxid = '%s' and goodsid = '%s'" % (wxid , goodsid)

    cursor = connection.cursor()
    luckycount = cursor.execute(sqlStr);
    datas = cursor.fetchall()
    for row in datas:
            
        getGoodsId = row[1]
        getWxid = row[2] 

        # 根据id 获取商品详情
        goodsDetail = getGoodsDetailByGoodsid(getGoodsId)

        # 根据 wxid 获取用户详情
        userDetail = getUserDetailByWxid(getWxid)

        try:
            uptime = MyTool.none_or_strftime(row[4])
        except:
            uptime = "未知"
        comment = {
            'commentid':row[0],
            'goodsInfo':{
                'goods': goodsDetail , 
                'buyNumber': row[12],
                'fahuotime': row[13],
                'is_pingjia': row[14],
                'orderTableId': row[15],
                'params': row[11],
                'status': row[16],
                'transportId': row[17],
            },
            'user':userDetail,
            'comment_text':row[3],
            'uptime':uptime,
            'happing': row[5],
            'niming': row[6] , 
            'shiwu': row[7] , 
            'wuliu': row[8] , 
            'fuwu': row[9] ,   
        }
        comment['commImg'] = getCommimgFn(row[0])
        myData.append(comment);
    cursor.close();
    return {"myData": myData , 'luckycount': luckycount}

# 评论查询(通过用户id和商品id) 胡亚洲  已完成
def commentJsonQuery(request):
    wxid = request.POST.get("wxid" , "")
    goodsid = request.POST.get("goodsid" , "")
    try:
        current_data = commentJsonQueryFn(wxid , goodsid)
        return HttpResponse(json.dumps({'data':current_data['myData'], 'status':'ok' , 'commentCount':str(current_data['luckycount']) }), content_type="application/json")
    
    except Exception as e: 
        raise e  
        return HttpResponse(json.dumps({'data':current_list, 'status':'error', 'goodscount':'0'}), content_type="application/json");
# 评论删除接口 胡亚洲 已完成
def commentJsonDelete(request):
    commentidsDict =  request.POST
    commentids = luckyidsDict.getlist("commentids")
    cursor=connection.cursor();
    result = 0
    try:
        for commentid in commentids:
            result += cursor.execute("DELETE FROM comment where commentid = '%s'"%(commentid))
        cursor.close();
        if result != 0:
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok', 'deleteCount':result}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    except Exception as e:   
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
# 评论添加接口 胡亚洲 已完成
def commentJsonAdd(request):
    try:
        commentid = randomString()
        goodsid = request.POST.get("goodsid" , "")
        wxid = request.POST.get("wxid" , "")
        comment_text = request.POST.get("comment_text" , "")
        orderid = request.POST.get("orderid" , "")
        checkerValue = request.POST.get("checkerValue" , "")
        shiwu = request.POST.get("shiwu" , "")
        wuliu = request.POST.get("wuliu" , "")
        fuwu = request.POST.get("fuwu" , "")
        niming = request.POST.get("niming" , "")
        commImg = request.POST.get("commImg" , "")

        params = request.POST.get("params" , "")
        buyNumber = request.POST.get("buyNumber" , "")
        fahuotime = request.POST.get("fahuotime" , "")
        is_pingjia = request.POST.get("is_pingjia" , "")
        orderTableId = request.POST.get("orderTableId" , "")
        status = request.POST.get("status" , "")
        transportId = request.POST.get("transportId" , "")

        cursor = connection.cursor()
        sql = "INSERT INTO comment \
        (commentid , goodsid , wxid , comment_text , haoping , niming , shiwu , wuliu , fuwu , commImg , \
        params , buyNumber , fahuotime , is_pingjia , orderTableId , status , transportId) \
        VALUES \
        ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s') \
        " % (commentid, goodsid, wxid, comment_text , checkerValue , niming , shiwu , wuliu , fuwu , commImg , params , buyNumber , fahuotime , is_pingjia , orderTableId , status , transportId)
        result = cursor.execute(sql)
        if result == 1 :
            addOneCommentNumberByGoodsid(goodsid)
            add_number_sql = "update goods set %s=%s+ 1 where goodsid = '%s'" % (checkerValue , checkerValue , goodsid)
            cursor.execute(add_number_sql)

            add_number_sql = "update order_goods_table set is_pingjia='true' , status = 4 \
            where goodsid = '%s' and orderTableId = '%s'\
            " % (goodsid , orderid)
            cursor.execute(add_number_sql)

            cursor.close()
            # statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps({'status': 'ok' , 'message': '添加成功' , 'data': {'commentid': commentid}}) , content_type = "application/json");
        else:
            cursor.close()
            statusDic=MyTool.resultError("添加失败");
            return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
    except Exception as e:   
        # raise e 
        return HttpResponse(json.dumps({'message':"添加失败", 'status':'error'}), content_type="application/json");


# 将某一个地址设置为默认地址,其他地址修改为非默认地址
def change_one_add_to_moren(request):
    try:
        
        wxid = request.POST.get("wxid" , "")
        addid = request.POST.get("addid" , "")
        if wxid == "" or addid == "":
            return HttpResponse(json.dumps({"status":"error" , "message":"参数错误"}),content_type="application/json");

        cursor = connection.cursor()
        sqlStr = "update address set flag = 'false' where wxid = '%s'" % wxid
        cursor.execute(sqlStr)

        sqlStr = "update address set flag = 'true' where addid = '%s'" % addid
        cursor.execute(sqlStr)

        cursor.close();
        return HttpResponse(json.dumps({"status":"ok" , "message":"修改成功"}),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加地址操作异常，请联系服务器人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");

#添加地址接口
def addAddress(request):
    try:
        cursor = connection.cursor()
        addid = randomString()
        wxid = request.POST.get("wxid" , "")
        username = request.POST.get("username" , "")
        tel = request.POST.get("tel" , "")
        address = request.POST.get("address" , "")
        mailcode = request.POST.get("mailcode" , "")
        flag = request.POST.get("flag" , "")
        if wxid == "" or username == "" or address == "":
            return HttpResponse(json.dumps({"status":"error" , "message":"参数错误"}),content_type="application/json");

        if flag == "true":
            sqlStr = "update address set flag = 'false' where wxid = '%s'" % wxid
            cursor.execute(sqlStr)
        
        result = cursor.execute("INSERT INTO address (addid , wxid , username , tel , address , mailcode , flag) VALUES ('%s' , '%s' , '%s' , '%s' , '%s' , '%s' , '%s' )" % (addid , wxid , username , tel , address , mailcode , flag))

        

        cursor.close();
        if result == 1:
            statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
        else :
            statusDic=MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except:
        statusDic=MyTool.resultError("添加地址操作异常，请联系服务器人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#删除地址接口
def delAddress(request):

    addid = request.POST.get("addid" , "")
    if addid == "":
        return HttpResponse(json.dumps({"status":"error" , "message":"参数错误"}),content_type="application/json");
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM address WHERE addid='%s'" % addid)
        cursor.close()
        statusDic=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除失败");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#更新地址接口
def updateAddress(request):
    cursor = connection.cursor()
    datas = request.POST

    try:
        for key in list(datas):
            cursor.execute("update address set %s='%s' where addid='%s'"%(key , datas[key] , datas["addid"]))
            statusDic=MyTool.resultOk("修改成功")
        return HttpResponse(json.dumps(statusDic) , content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改失败","status":"error"}),content_type="application/json")
#查找地址接口
def findAddress(request):
    
    try:
        wxid = request.POST.get("wxid" , "")

        myData = getAddressListByWxid(wxid)

        return HttpResponse(json.dumps(myData) , content_type="application/json");

    except Exception as e :
        raise e 
        statusDic=MyTool.resultError("查找失败");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
def message_row_to_dic(row):
    return {
        'msgId': row[0],
        'senderId': row[1],
        'receiveId': row[2],
        'time': row[3].strftime("%Y-%m-%d %H:%M:%S"),
        'status': row[4],
        'content': row[5],
    }

#留言接口
def leavingMessage(request):
    return render(request , "leavingMessage.html");

#根据wxid 标记已读消息
def read_all_msg_by_wxid(request):
    wxid = request.POST.get('wxid' , '')
    is_client = request.POST.get('client', '')

    if wxid == "":
        statusDic=MyTool.resultError("参数错误");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json")


    cursor = connection.cursor()
    sql_str = ""
    if is_client == 'client':
        sql_str = "update message set status = 2 where receiveId = '%s' and status = 1" % wxid
    else:
        sql_str = "update message set status = 2 where senderId = '%s' and status = 0" % wxid
    cursor.execute(sql_str)
    
    rows = cursor.fetchall()
    cursor.close()
    
    statusDic=MyTool.resultOk("标记已读成功")
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json")


#增加用户留言接口
def addLeaveMessage(request):
    content = request.POST.get('content' , '')
    senderId = request.POST.get('senderId' , '')
    receiveId = request.POST.get('receiveId' , '')
    if content == "" or senderId == "" or receiveId == "":
        statusDic=MyTool.resultError("参数错误");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json")

    msgId = randomString()
    cursor = connection.cursor()
    cur_status = 0
    if senderId == MyTool.server_str():
        cur_status = 1
    result = cursor.execute("INSERT INTO message(msgId , content , senderId , receiveId , status)VALUES('%s' , '%s' , '%s' , '%s' , %d)"%(msgId , content , senderId , receiveId , cur_status))
    cursor.close()
    if result == 1:
         statusDic=MyTool.resultOk("留言添加成功")
    else :
        statusDic=MyTool.resultError("留言添加失败");
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json")

     


#查询用户留言接口
def leaveMessage(request):
    wxid = request.POST.get('wxid' , '')

    if wxid == "":
        statusDic=MyTool.resultError("参数错误");
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json")


    cursor = connection.cursor()
    cursor.execute("SELECT * FROM message where senderId = '%s' or receiveId = '%s'" % (wxid , wxid))
    
    rows = cursor.fetchall()
    cursor.close()
    msg_arr = get_liuyan_list(rows)
    return HttpResponse(json.dumps(msg_arr) , content_type = "application/json")

#删除用户留言接口
def deleLeaveMessage(request):
    msgId = request.POST.get('msgId' , "")
    if msgId == "":
        statusDic=MyTool.resultError("参数错误");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    
    cursor = connection.cursor()
    sql = "delete from message where msgId = '%s'" % msgId
    result = cursor.execute(sql)
    cursor.close() 
    statusDic=MyTool.resultOk("留言删除成功")
    return HttpResponse(json.dumps(statusDic) , content_type = "application/json")
#添加分享接口 已完成
def addShare(request):
    try:
        goodsid = request.POST.get("goodsid" , "")
        wxid = request.POST.get("wxid" , "")
        sharepath = request.POST.get("sharepath" , "")

        shareid = randomString()

        cursor = connection.cursor()
        result = cursor.execute("INSERT INTO share (shareid , goodsid , wxid , sharepath) VALUES ('%s' , '%s' , '%s' , '%s')" % (shareid , goodsid , wxid , sharepath))
        cursor.close()
        if result == 1:
            statusDic=MyTool.resultOk("添加成功")
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
        else :
            statusDic=MyTool.resultError("添加失败")
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except Exception as e:
        raise e
        statusDic=MyTool.resultError("分享添加异常,请联系服务器人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#删除分享接口 已完成
def delShare(request):
    try:
        cursor = connection.cursor()
        shareid = request.POST.get("shareid" , "")
        cursor.execute("DELETE FROM share WHERE shareid='%s'" % shareid)
        cursor.close()
        statusDic=MyTool.resultOk("删除成功")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except Exception as e:
        raise e
        statusDic=MyTool.resultError("分享删除异常,请联系服务器人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
# 分享列表接口 已完成
def findShare(request):
    try:
        cursor = connection.cursor()
        wxid = request.POST.get("wxid" , "")
        myData = []
        cursor.execute("SELECT * FROM share WHERE wxid='%s'" % wxid)
        datas = cursor.fetchall()
        cursor.close()
        for data in datas:
            tempDic = {
                "shareid":data[0] , 
                "wxid":data[2] , 
                "sharepath":data[3] , 
                'sharetime':MyTool.none_or_strftime(data[4])
            }
            tempDic["goods"] = getGoodsDetailByGoodsid(data[1])
            myData.append(tempDic)

        return HttpResponse(json.dumps({"data":myData , "status":"ok"}) , content_type="application/json");

    except Exception as e:
        raise e
        statusDic=MyTool.resultError("分享查询异常,请联系服务器人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");


# 购买历史添加接口 已完成
def buyhistoryAdd(request):
    try:
        
        buyid = randomString()
        wxid = request.POST["wxid"]
        goodsid = request.POST["goodsid"]
        number = request.POST["number"]
        goodsparams1 = request.POST["goodsparams1"]
        goodsparams2 = request.POST["goodsparams2"]
        
        cursor = connection.cursor()
        sqlStr = "INSERT INTO buyhistory(wxid , buyid , goodsid , number , goodsparams1 , goodsparams2) VALUES ('%s' , '%s' , '%s' ,'%s' ,'%s' , '%s')" % (wxid , buyid , goodsid , number , goodsparams1 , goodsparams2)

        result = cursor.execute(sqlStr)
        cursor.close()
        if result == 1:
            statusDic=MyTool.resultOk("消费记录添加成功");
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
        else: 
            statusDic=MyTool.resultError("消费记录添加失败");
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except Exception as e:
        raise e
        statusDic=MyTool.resultError("添加消费记录操作异常,请联系服务器管理人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#购买记录删除接口 已完成
def buyhistoryDelete(request):
    
    try:
        buyid = request.POST["buyid"]
        cursor = connection.cursor()
        result = cursor.execute("DELETE FROM buyhistory WHERE buyid = '%s'" % buyid)
        cursor.close()
        if result >= 1:
            statusDic=MyTool.resultOk("删除成功");
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
        else :
            statusDic=MyTool.resultError("删除失败");
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except:
        statusDic=MyTool.resultError("删除购买记录操作异常,请联系服务器管理人员");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#购买记录查询接口 已完成
def buyhistorySelect(request):
    wxid = request.POST.get('wxid' , '')
    if wxid == '':
       return HttpResponse(json.dumps({"message":'请获取用户信息' , "status":"error"}) , content_type="application/json"); 
    try:
        cursor=connection.cursor()
        myData=[]
        cursor.execute("SELECT * FROM buyhistory WHERE wxid = '%s'" % wxid)
        for data in cursor.fetchall():
            tempDic = {
                'wxid':data[0] , 
                'buyid':data[1] , 
                'number':data[3] , 
                'buytime':MyTool.none_or_strftime(data[4]),
                'params':data[5] , 
                'goods':{}
            }
            tempDic["goods"] = getGoodsDetailByGoodsid(data[2])
            myData.append(tempDic)
        cursor.close()
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    except Exception as e:  
        raise e 
        return HttpResponse(json.dumps({"message":'购买记录接口查询操作异常,请联系服务器管理人员' , "status":"error"}) , content_type="application/json");

#好友列表查询功能
def friendslistManageJsonSelect(request):
    # friendslistid = request.friendsList["friendslistid"]
    friendslistid = "11"
   
    myData = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM friendsList WHERE friendslistid='%s'" % (friendslistid))
    for data in cursor.fetchall():
        friendslistid = data[0];
        wxid = data[1];
        friendid = data[2];
        setuptime = MyTool.none_or_strftime(data[3])
    
        tempDic = {"friendslistid":friendslistid , "wxid":wxid , "friendid":friendid , "setuptime":setuptime}
        myData.append(tempDic)
    cursor.close()
    return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")


def settings(request):
    return render(request,"setting.html")
def settingsApi(request):
    sql="";
    if request.POST and (request.POST["settingid"]!=""):
        settingid=request.POST["settingid"];     
        sql="update settingtable redmoney='%s',rebatepercent='%s',rebatevalue='%s' WHERE settingid='%s'"%(redmoney,rebatepercent,rebatevalue,settingid);
     
    else:
        sql = "SELECT * FROM settingtable";   
    allOrdertables = [];
    cursor = connection.cursor()
    cursor.execute(sql)
    for row in cursor.fetchall():
        ordertable = {
            'settingid':row[0],
            'redmoney':row[1],
            'rebatepercent':row[2],
            'rebatevalue':row[3],
        }
        allOrdertables.append(ordertable)
    cursor.close()
    return HttpResponse(json.dumps({'data':allOrdertables, 'status':'ok'}), content_type="application/json")

def settingsAdd(request):
    settingid=request.POST["settingid"];
    redmoney=request.POST["redmoney"];
    rebatepercent=request.POST["rebatepercent"];
    rebatevalue=request.POST["rebatevalue"];
    try:
        cursor=connection.cursor();
        cursor.execute("INSERT INTO settingtable(settingid,redmoney,rebatepercent,rebatevalue) VALUES (%s,%s,%s,%s)"% (settingid,redmoney,rebatepercent,rebatevalue))
        statusDic=MyTool.resultOk("添加成功");
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except Exception as e :
        statusDic=MyTool.resultError("添加失败")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
def settingsUpdate(request):   
    cursor = connection.cursor()
    
    datas = request.POST
    settingid= request.POST["settingid"]
    settingid = str(settingid)
    for key in datas:
        if key != 'settingid' and datas[key] != "":
            cursor.execute("update settingtable set %s='%s' where settingid=%s"%(key , datas[key] , datas["settingid"]))
    cursor.close();                   
    return HttpResponse(json.dumps({"message":"更新成功" , "status":"ok"}) , content_type="application/json");

def get_message_by_wxid(request):
    wxid = request.POST.get('wxid' , '')
    if wxid == '':
       return HttpResponse(json.dumps({"message":'参数错误' , "status":"error"}) , content_type="application/json"); 

    # cursor = connection.cursor()
    # sql_str = "select * from message where senderId = '%s' or receiveId = '%s'" % (wxid , wxid)

    # cursor.execute(sql_str)
    # rows = cursor.fetchall()
    # cursor.close()

    msg_list = []
    # for row in rows:
    #      msg_list.append(message_row_to_dic(row))

    return HttpResponse(json.dumps({"data":msg_list , "status":"ok" , "message":"查询成功"}) , content_type="application/json");


#base页面留言列表和订单列表
def liuyan_and_dingdan(request):  
    cursor = connection.cursor()
    
    dataArr = {
        "liuyan_list":[] , 
        "dingdan_list":[]
    }

    # 查询留言列表
    cursor.execute("SELECT * FROM message")
    rows = cursor.fetchall()

    # return {
    #     'msgId': row[0],
    #     'senderId': row[1],
    #     'receiveId': row[2],
    #     'time': row[3].strftime("%Y-%m-%d %H:%M:%S"),
    #     'status': row[4],
    #     'content': row[5],
    # }

    msg_arr = []
    temp_arr = []
    for row in rows:
        temp_str = row[1]
        if temp_str == MyTool.server_str():
            temp_str = row[2]
        if temp_str in temp_arr:
            temp_data_index = temp_arr.index(temp_str)
            msg_arr[temp_data_index]['msg_list'].append(message_row_to_dic(row))
        else:
            temp_arr.append(temp_str)
            sqlStr = "select * from user where wxid = '%s'" % temp_str
            cursor = connection.cursor()
            cursor.execute(sqlStr)
            user_rows = cursor.fetchall()
            oneData = user_row_to_dic_one(user_rows)
            msg_arr.append({
                'user_info':oneData,
                'msg_list':[message_row_to_dic(row)]
            })

    dataArr["liuyan_list"] = msg_arr

    # 订单列表查询
    cursor.execute("SELECT * FROM ordertable order by createTime")
    dataArr["dingdan_list"] = orderRows_to_orderData(cursor.fetchall())
    cursor.close();

    # 留言查询
                     
    return HttpResponse(json.dumps({"data":dataArr , "status":"ok" , "message":"查询成功"}) , content_type="application/json");

def get_liuyan_list(rows):
    msg_arr = []
    for row in rows:
        msg_arr.append(message_row_to_dic(row))
    return msg_arr 

#获取session接口
def getSession(request):
    is_login = request.session.get('IS_LOGIN',False)
    return HttpResponse(json.dumps({"data":is_login , "status":"ok"}) , content_type="application/json");
#设置session接口
def setSession(request):
    request.session['IS_LOGIN'] = False
    is_login = request.session.get('IS_LOGIN')
    return HttpResponse(json.dumps({"status":"ok"}) , content_type="application/json");
#获取当前时间
def getdatatime(request):
    return HttpResponse(json.dumps({"status":"ok" , "message":'服务器的返回时间'}) , content_type="application/json");



#秒杀添加接口 已完成
def secondkillManageJsonAdd(request):
    try:
        
        killid = randomString();
        goodsid = request.POST.get("goodsid" , "");
        starttime = request.POST.get("starttime" , "");
        stoptime = request.POST.get("stoptime" , "")
        miaoShaCount = request.POST.get("miaoShaCount" , "")
        if goodsid == "" or starttime == "" or stoptime == "" or miaoShaCount == "":
            return HttpResponse(json.dumps({"status":"error" , "message":'参数有误'}) , content_type="application/json");

        cursor = connection.cursor();
        result = cursor.execute("INSERT INTO secondkill(killid , goodsid ,starttime, stoptime , miaoShaCount) VALUES ('%s' , '%s' ,'%s' , '%s' , '%s')" % (killid , goodsid , starttime ,stoptime , miaoShaCount))

        if result == 1:
            statusDic=MyTool.resultOk("添加成功");
            cursor.execute("UPDATE goods SET isinmiaosha = 'true' WHERE goodsid = '%s'" % goodsid)
            cursor.close()
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
        else :
            statusDic=MyTool.resultError("添加失败");
            return HttpResponse(json.dumps(statusDic),content_type="application/json");
        
            
    except Exception as e:
        statusDic=MyTool.resultError("秒杀添加异常,请联系服务器人员")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");

# 增加商品的已秒杀数量
def addAlreadyMiaoShaNumber(request):
    goodsid = request.POST.get("goodsid" , "")
    if goodsid == "":
        return HttpResponse(json.dumps({'status':"error" , 'message':'参数传入失败'}) , content_type="application/json")

    sqlStr = "UPDATE secondkill SET alreadyMiaoShaNumber = alreadyMiaoShaNumber + 1 WHERE goodsid = '%s'" % goodsid
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    if result >= 1:
        return HttpResponse(json.dumps({'status':"ok" , 'message':'操作成功'}) , content_type="application/json")
    else:
        return HttpResponse(json.dumps({'status':"error" , 'message':'操作失败'}) , content_type="application/json")



# 秒杀查询接口 已完成
def secondkillManageJsonSelect(request):
    try:
        page = request.POST.get("page" , 1)
        if int(page) <= 1:
            page = 1
        start = (int(page) - 1) * 10

        cursor=connection.cursor()
        myData=[]
        cursor.execute("SELECT killid , goodsid ,starttime , stoptime , miaoShaCount , alreadyMiaoShaNumber FROM secondkill limit %d , 10" % start)
    
        for data in cursor.fetchall():
            tempDic = {
                'killid':data[0] , 
                'goods':{} , 
                'startTime':MyTool.none_or_strftime(data[2]),
                'stopTime':MyTool.none_or_strftime(data[3]),
                'miaoShaCount':data[4] , 
                'alreadyMiaoShaNumber':data[5]
            }

            goods = getGoodsDetailByGoodsid(data[1])

            tempDic["goods"] = goods
            
            myData.append(tempDic)
        cursor.execute("SELECT COUNT(*) FROM secondkill")
        goodscount  = cursor.fetchall();
        cursor.close()
        goodscount = goodscount[0][0]
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'count':goodscount}), content_type="application/json")
    except Exception as e:   
        return HttpResponse(json.dumps({"message":"秒杀接口查询异常,请联系服务器人员" , "status":"error"}) , content_type="application/json");
def secondkillManageJsonDelete(request):
    killid = request.POST["killid"];
    goodsid = request.POST["goodsid"];
    
    cursor=connection.cursor()
    try:
        cursor.execute("DELETE FROM secondkill where killid = %s" %killid)
        cursor.execute("UPDATE goods SET isinmiaosha = 'false' WHERE goodsid = '%s'" % goodsid)
        statusDic=MyTool.resultOk("删除成功");
        cursor.close()
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
    except:
        
        statusDic=MyTool.resultError("秒杀删除异常操作....")
        return HttpResponse(json.dumps(statusDic),content_type="application/json");
#秒杀分页 韩乐天
def secondkillcommodityQuery(request):
    try:
        myData=[];
        mypage = (int(request.POST["page"]) - 1) * 8
        cursor = connection.cursor();
        #以八条数据为一页返回第mypage页,并且按时间排序
        cursor.execute("SELECT * FROM secondkill  LIMIT %d , 8"%mypage);
        #取出数据
        datas=cursor.fetchall();
        for data in datas:
            killid = data[0];
            goodsid = data[1];
            goodstatus = data[2];
            starttime = MyTool.none_or_strftime(data[3])
            stoptime = MyTool.none_or_strftime(data[4])
            goodsname = data[5];
            tempDic = {"killid":killid, "goodsid":goodsid , "goodstatus":goodstatus , "starttime":starttime , "stoptime":stoptime ,"goodsname":goodsname}
            myData.append(tempDic)
        #查出总共有多少条数据
        cursor.execute("SELECT COUNT(*) FROM secondkill")
        adcounts  = cursor.fetchall();
        adcounts = adcounts[0][0];
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok' , 'adcounts':str(adcounts)}) , content_type="application/json");
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error', 'adcounts':'0'}), content_type="application/json");

# 秒杀 修改商品的秒杀信息 已完成
def secondkillManageJsonUpdata(request):
    try:

        miaoshaId = request.POST.get("killid" , "")
        miaoshaCount = request.POST.get("miaoShaCount" , "")
        startTime = request.POST.get("starttime" , "")
        stoptime = request.POST.get("stoptime" , "")

        sqlStr = ""

        if miaoshaId == "" or miaoshaCount == "":
            return HttpResponse(json.dumps({'status':'error' , 'message':'参数传入错误'}) , content_type="application/json")

        if startTime == "" and stoptime == "":
            sqlStr = "update secondkill set miaoShaCount='%s' where killid='%s'" % (miaoshaCount , miaoshaId)
        
        if startTime != "" and stoptime != "":
            sqlStr = "update secondkill set miaoShaCount='%s' , starttime='%s' , stoptime='%s' where killid='%s'" % (miaoshaCount , startTime , stoptime , miaoshaId)
        

        if startTime == "" and stoptime != "":
            sqlStr = "update secondkill set miaoShaCount='%s' , stoptime='%s' where killid='%s'" % (miaoshaCount , stoptime , miaoshaId)
        
        if startTime != "" and stoptime == "":
            sqlStr = "update secondkill set miaoShaCount='%s' , starttime='%s' where killid='%s'" % (miaoshaCount , startTime , miaoshaId)
        
        cursor = connection.cursor()
        result = cursor.execute(sqlStr)
        if result >= 1:
            return HttpResponse(json.dumps({'status':'ok' , 'message':'操作成功'}) , content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status':'error' , 'message':'操作失败'}) , content_type="application/json")


    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"修改秒杀商品操作异常，请联系服务器管理人员","status":"error"}),content_type="application/json")

    
    
def secondkillManageJsonstock(request):
    killid = request.POST["killid"];
    cursor = connection.cursor();
    try:
        cursor.execute("select stock from goods where goodsid = (select goodsid from secondkill where killid = '%s')"%killid);
        data = cursor.fetchall();
        stock = data[0][0];
        cursor.close();
        return HttpResponse(json.dumps({'data':stock, 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"message":"没有该商品", 'status':'error'} , content_type="application/json"))
def secondkillAddgoodsidintogoods(request):
    goodsid = request.POST['goodsid'];
    cursor = connection.cursor();
    killid = randomString();
    try:
        sql = "INSERT INTO secondkill(killid,goodsid) VALUES ('%s','%s')" %  (killid,goodsid) ;
        cursor.execute(sql);
        cursor.close();
        return HttpResponse(json.dumps({'message':'添加成功', 'status':'ok'}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({"message":"添加失败", 'status':'error'}) , content_type="application/json")


# 快递查询接口  测试版   （陈云飞）
def express(request):
    NO = request.POST["NO"];
    company = request.POST["company"];
    appkey = '6a5e822ae9dacf265266ea02bd27b5ba';
    url = "http://v.juhe.cn/exp/index"
    params = {
        "com" : company, #需要查询的快递公司编号
        "no" : NO, #需要查询的订单号
        "key" : appkey, #应用APPKEY(应用详细页查询)
        "dtype" : "json", #返回数据的格式,xml或json，默认json
    
    }
    params = urlencode(params)   
    f = urllib.request.urlopen("%s?%s" % (url, params))
    content = f.read()
    res = json.loads(content)
    error_code = res["error_code"]    
    if error_code == 0:
        #成功请求
        resultDic = (res['result'])
        return HttpResponse(json.dumps(resultDic) , content_type="application/json");
    else:
        return HttpResponse(json.dumps({"error_code":res["error_code"] , "reason":res["reason"]}) , content_type="application/json");
#查询快递公司编号接口  测试用 （陈云飞）
def expressCompany(request):
    appkey = '6a5e822ae9dacf265266ea02bd27b5ba';
    url = "http://v.juhe.cn/exp/com";
    params = {
        "key":appkey
    }
    params = urlencode(params)
    f = urllib.request.urlopen("%s?%s" % (url, params))

    content = f.read()
    res = json.loads(content)
    if res:
        error_code = res["error_code"]
        if error_code == 0:
            #成功请求
            return HttpResponse(res["result"])
        else:
            return HttpResponse("%s:%s" % (res["error_code"],res["reason"]))
    else:
        return HttpResponse("request api error")
#发送短信接口  测试用  （陈云飞）
def shortMsgFromName(request):
    username = request.POST["username"];
    cursor = connection.cursor();
    cursor.execute('SELECT * FROM manager WHERE username = "%s"' % username)
    datas = cursor.fetchall();
    for i in datas:
        phone = i[2];
        p=re.compile('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$')
        match = p.match(phone)
        if match:  

            sendurl = 'http://v.juhe.cn/sms/send' #短信发送的URL,无需修改 
            appkey = '0f2f46d95cfe854988012bf5a1da65cf';
            mobile = phone;
            tpl_id = "56951";
            code = str(random.randint(0,999999));
            tpl_value = '#code#='+code;
            params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
                    (appkey, mobile, tpl_id, urllib.request.quote(tpl_value)) #组合参数
        
            wp =urllib.request.urlopen(sendurl+"?"+params)
            content = wp.read() #获取接口返回内容
        
            result = json.loads(content)
            error_code = result['error_code']
            if error_code == 0:
                #发送成功
                smsid = result['result']['sid']
                statusDic = {"status":"ok" , "smsid":smsid}
                return HttpResponse(json.dumps(statusDic) , content_type="application/json");
            else: 
                #发送失败
                statusDic = {"status":"error" , "reason":result['reason']}
                return HttpResponse(json.dumps(statusDic) , content_type="application/json");
        else:
            
            statusDic=MyTool.resultError("手机号码格式出错")
            return HttpResponse(json.dumps(statusDic) , content_type="application/json")
#发送短信接口  测试用  （陈云飞）
def shortMsgFromPhone(request):
    phone = request.POST["phone"]
    p=re.compile('^((13[0-9])|(14[5|7])|(15([0-3]|[5-9]))|(18[0,5-9]))\\d{8}$')
    match = p.match(phone)
    if match:
        sendurl = 'http://v.juhe.cn/sms/send' #短信发送的URL,无需修改 
        appkey = '0f2f46d95cfe854988012bf5a1da65cf';
        mobile = phone;
        tpl_id = "56951";
        code = str(random.randint(0,999999));
        tpl_value = '#code#='+code;
        params = 'key=%s&mobile=%s&tpl_id=%s&tpl_value=%s' % \
        (appkey, mobile, tpl_id, urllib.request.quote(tpl_value)) #组合参数
            
        wp =urllib.request.urlopen(sendurl+"?"+params)
        content = wp.read() #获取接口返回内容
            
        result = json.loads(content)
        error_code = result['error_code']
        if error_code == 0:
            #发送成功
            smsid = result['result']['sid']
            statusDic = {"status":"ok" , "smsid":smsid}
            return HttpResponse(json.dumps(statusDic) , content_type="application/json");
        else: 
            #发送失败
            statusDic = {"status":"error" , "reason":result['reason']}
            return HttpResponse(json.dumps(statusDic) , content_type="application/json");
    else:
        
        statusDic=MyTool.resultError("手机号码格式出错")
        return HttpResponse(json.dumps(statusDic) , content_type="application/json")


#活动修改接口
def activetableManageJsonchange(request):
    try:
        datas = request.POST
        cursor=connection.cursor();
        if request.FILES:
            #前台传过来的图片
            Imgs = request.FILES["imgs"];
            #随机字符串存取图片名字
            ImgsName = randomString() + ".jpg";
            #当上传头像的时候必然会传过来用户的Id,方法根据前台来决定
            
            cursor.execute("SELECT imgs FROM activetable WHERE activeid='%s'" % datas["activeid"])
            data = cursor.fetchall();
            if data[0][0]:
                tempimg = data[0][0];
                if os.path.exists("../shopServer/shopApp/static/myfile/"+tempimg)==True:
                    os.remove("../shopServer/shopApp/static/myfile/"+tempimg);
                else:
                    pass;
            filepath = "./shopApp/static/myfile/";
            #路径组合
            filepath = os.path.join(filepath,ImgsName)
            #在路径中创建图片名字
            fileobj = open(filepath , "wb");
            #并把前端传过来的数据写到文件中
            fileobj.write(Imgs.__dict__["file"].read());
            cursor.execute("update activetable set imgs='%s' where activeid=%s"%(ImgsName , datas["activeid"]))
        for key in list(datas):
            if key != "imgs":
                cursor.execute("update activetable set %s='%s' where activeid='%s'"%(key , datas[key] , datas["activeid"]))
        cursor.execute("SELECT * FROM activetable WHERE activeid='%s'" % datas["activeid"])
        data = cursor.fetchall()[0]
        activeid=data[0]
        activedetail=data[1]
        starttime=MyTool.none_or_strftime(data[2])
        imgs = data[3]
        stoptime = MyTool.none_or_strftime(data[4])
        activetitle = data[5]
        activeName = data[6]
        activePosition = data[7]
        tempDic={"activeid":activeid,"activedetail":activedetail,"starttime":starttime,"imgs":imgs,"stoptime":stoptime,"activetitle":activetitle, "activeName":activeName,"activePosition":activePosition}
        data = {'data':'success', 'status':'ok','addactive':tempDic}
        cursor.close();
        return HttpResponse(json.dumps(data) , content_type="application/json");
    except Exception as e :
        cursor.close();
        raise e
        statusDic={'data':'error', 'status':'error'};
        return HttpResponse(json.dumps(statusDic),content_type="application/json");


def audioToStr(request):
     return render(request , "audiotostr.html");


# def audioToStrApi(request):
#     statusDic = {};
#     if request.POST["audio"]:
#         mydata = request.POST["audio"];
#         mydata = mydata.split(",")
#         mydata = mydata[1];
#         mybyte = base64.b64decode(mydata);
#         filepath ="./shopApp/static/myfile/audio.wav";
#         myfile = open(filepath , "wb");
#         myfile.write(mybyte);
#         myfile.close();
#         allPath = os.path.abspath(filepath);
#         tmpAllPath = allPath.replace("audio","Str")
#         if os.path.exists(allPath):
#             cmd = "ffmpeg -i %s -ar 16000 -ac 1 %s" % (allPath ,tmpAllPath);
#             ret = subprocess.run(cmd);
#             if os.path.exists(tmpAllPath):
#                 myfile = open(tmpAllPath , "rb");
#                 audiobyte = myfile.read();
#                 myfile.close();
#                 APP_ID = '10573104'
#                 API_KEY = 'iGPGdtRjwadhpRdsG89iSIrp'
#                 SECRET_KEY = '1c169dc662f8bfdf88f73fe3e8a1940d'
#                 aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
#                 result = aipSpeech.asr(audiobyte, 'wav', 16000, {'lan': 'zh',});
#                 os.remove(tmpAllPath);
#                 if result["err_no"] == 0:
#                     result = result["result"][0];
#                     statusDic = {"status":"ok" , "result":result};
#                 else:
#                     statusDic = {"status":"error" , "result":"请说普通话"};
#             else:
#                 statusDic = {"status":"error" , "result":"数据转换失败"};
#         else:
#             statusDic = {"status":"error" , "result":"数据写入失败"};
#     else:
#         statusDic = {"status":"error" , "result":"没有接受到数据"};
#     return HttpResponse(json.dumps(statusDic) , content_type = "application/json");




#根据商品名模糊查询
def goodsNameSelect(request):
    myData = []
    cursor = connection.cursor()
    goodsName = request.POST["goodsName"]
    cursor.execute("SELECT * FROM goods where goodsname like '%%%%%s%%%%'"%(goodsName));
    datas = cursor.fetchall()
    try:
        for row in datas:
            goods = goodsDataRowToDic(row)
            myData.append(goods);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");

#根据商品名准确查询
def goodsNameOneSelect(request):
    myData = []
    cursor = connection.cursor()
    goodsName = request.POST["goodsName"]
    cursor.execute("SELECT * FROM goods where goodsname='%s'"%(goodsName));
    datas = cursor.fetchall()
    try:
        for row in datas:
            goods = goodsDataRowToDic(row)
            myData.append(goods);
        cursor.close();
        return HttpResponse(json.dumps({'data':myData, 'status':'ok'}), content_type="application/json")
    
    except Exception as e: 
        raise e   
        return HttpResponse(json.dumps({'data':myData, 'status':'error'}), content_type="application/json");

#购物车删除接口
def cartstableManageJsonOneDelete(request):
    cursor=connection.cursor()
    cartsid = request.GET["id"];

    try:
        result = cursor.execute("DELETE FROM liu_carts WHERE cartsid='%s'" % (cartsid))
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")

# 根据小分类id查询所有的商品
def getGoodsByMinfenleiId(request):
    
    try:
        minFenleiId = request.POST.get("minFenleiId" , "")
        remoteType = request.POST.get("type" , "phone")
        if minFenleiId == "":
            return HttpResponse(json.dumps({"message":"参数错误","status":"error"}),content_type="application/json")
        page = request.POST.get("page" , 1)
        if int(page) <= 1:
            page = 1
        start = (int(page) - 1) * 10

        if remoteType == "phone":
            sqlStr = "select *from goods where status='1' and xiaoClassiData='%s' limit %d , 10" % (minFenleiId , start)

        else:
            sqlStr = "select *from goods where xiaoClassiData='%s' limit %d , 10" % (minFenleiId , start)
        
        cursor = connection.cursor()
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        
        data = []
        for row in rows:
            oneData = goodsDataRowToDic(row)
            data.append(oneData)

        cursor.execute("SELECT COUNT(*) FROM goods where xiaoClassiData='%s'" % minFenleiId)
        goodscount  = cursor.fetchall();
        cursor.close()
        goodscount = goodscount[0][0]

        return HttpResponse(json.dumps({'data':data, 'status':'ok' , 'count':goodscount}), content_type="application/json");

    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":"分类查询商品异常,请联系服务器管理人员","status":"error"}),content_type="application/json")


#商品大分类获取接口
def getBigClassify(request):
    myData=[];
    try:
        cursor = connection.cursor();
        cursor.execute("SELECT * FROM bigclassify")
        datas=cursor.fetchall();
        cursor.close()
        for data in datas:
            bigClassifyId=data[0];
            name=data[1];
            tempDic = {"bigClassifyId":bigClassifyId , "name":name}
            myData.append(tempDic)
        return HttpResponse(json.dumps({"message":"查询成功","status":"ok" , "data":myData}),content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"sql语句拼写出错","status":"error"}),content_type="application/json") 
# 商品大分类添加接口
def addBigClassify(request):
    cursor=connection.cursor()
    bigName = request.POST["bigName"];
    bigclassifyid = randomString()

    try:
        result = cursor.execute("INSERT INTO bigclassify (bigclassifyid , name)VALUES('%s' , '%s')" % (bigclassifyid , bigName) )
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"添加成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"添加失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")
# 商品大分类删除接口
def deleteBigClassify(request):
    cursor=connection.cursor()
    deleteName = request.POST["deleteName"];

    try:
        result = cursor.execute("DELETE FROM bigclassify WHERE name='%s'" % (deleteName))
        if result == 1:
            result = cursor.execute("DELETE FROM minClassify WHERE bigName='%s'" % (deleteName))
            cursor.close()
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
            
        else : 
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")
# 商品小分类获取接口
def getMinClassify(request):
    myData=[];
    try:
        sqlStr = "SELECT * FROM minClassify order by CONVERT(bigName USING gbk) , CONVERT(minName USING gbk)"
        queryValue = ""
        if "queryValue" in request.POST:
            queryValue = request.POST["queryValue"]

        if queryValue != "":
            sqlStr = "SELECT * FROM minClassify where bigName like '%%%%%s%%%%' or minName like '%%%%%s%%%%' order by CONVERT(bigName USING gbk) , CONVERT(minName USING gbk)" % (queryValue , queryValue)
        cursor = connection.cursor();
        cursor.execute(sqlStr)
        datas=cursor.fetchall();
        cursor.close()

        for data in datas:
            minClassifyId=data[1];
            bigName=data[2];
            minName = data[3]
            showImage = data[4]
            tempDic = {"minClassifyId":minClassifyId , "bigName":bigName , "minName":minName , "showImage":showImage}
            myData.append(tempDic)
        return HttpResponse(json.dumps({"message":"查询成功","status":"ok" , "data":myData}),content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"sql语句拼写出错","status":"error"}),content_type="application/json")
# 商品小分类添加图片接口
def uploadMinCllasifyImg(request):
    # request.FILES.getlist("imgsFile")

    sqlImgPath = ""

    try: 
        imgs = request.FILES["imgFile"];
        imgName = randomString()

        imgName = imgName + ".jpg"; 
        filepath = "./shopApp/static/myfile/classifyImgs/";
        filepath = filepath + imgName

        sqlImgPath = "/static/myfile/classifyImgs/" + imgName
        
        fileHandle = open(filepath , "wb");
        fileHandle.write(imgs.__dict__["file"].read());
        fileHandle.close();
    except Exception as e: 
        statusDic = MyTool.resultError("小分类图片保存失败，请联系服务器人员.....")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");


    # 将消费类图片路径保存到数据库中
    minClassifyId = request.POST["minClassifyIdInput"]
    sqlStr = "update minClassify set showImage='%s' where minClassifyId='%s'" % (sqlImgPath , minClassifyId)
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)

    if result >= 1:
        return HttpResponse(json.dumps({"message":"图片上传成功","status":"ok"}),content_type="application/json")
    else: 
        return HttpResponse(json.dumps({"message":"图片上传失败","status":"error"}),content_type="application/json")


# 商品小分类添加接口
def addMinClassify(request):
    cursor=connection.cursor()
    bigName = request.POST["bigName"];
    minName = request.POST["minName"];
    minClassifyId = randomString()

    try:
        result = cursor.execute("INSERT INTO minClassify (minClassifyId , bigName , minName)VALUES('%s' , '%s' , '%s')" % (minClassifyId , bigName , minName))
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"添加成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"添加失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")
# 商品小分类删除接口
def deleteMinClassify(request):
    cursor=connection.cursor()
    deleteBigName = request.POST["deleteBigName"];
    deleteMinName = request.POST["deleteMinName"];

    cursor.execute("select showImage from minClassify where bigName='%s' and minName='%s'" % (deleteBigName , deleteMinName))
    deleteImage = ""
    # if len(cursor.fetchall()) > 0 and len(cursor.fetchall()[0]) > 0:
    deleteImage = cursor.fetchall()[0][0]
    if deleteImage != None:
        deleteImage = deleteImage.replace(" " , "")


    if deleteImage == None or len(deleteImage) <= 0 or deleteImage == "null" or deleteImage == "":
        pass
    else:
        deleteImage = "../shopServer/shopApp" + deleteImage
        os.remove(deleteImage);

    try:
        result = cursor.execute("DELETE FROM minClassify WHERE bigName='%s' and minName='%s'" % (deleteBigName , deleteMinName))
        cursor.close()
        if result == 1:
            return HttpResponse(json.dumps({"message":"删除成功","status":"ok"}),content_type="application/json")
        else : 
            return HttpResponse(json.dumps({"message":"删除失败","status":"error"}),content_type="application/json")
    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"删除语句执行失败","status":"error"}),content_type="application/json")


# 不在推荐表中的所有商品
def notInRecommendGoods(request):
    try:
        commonName = request.POST.get("commonName" , " ")
        if commonName!= " ":
            commonName = " goodsname like '%%%%%s%%%%' and " % commonName
        sqlStr = "select * from goods where" + commonName + "goodsid not in (select goodsid from recommendGoods)"

        cursor = connection.cursor()
        cursor.execute(sqlStr);
        rows = cursor.fetchall()
        cursor.close()

        myData = []
        for row in rows:
            goods = goodsDataRowToDic(row)
            myData.append(goods);

        return HttpResponse(json.dumps({"data":myData,"status":"ok"}),content_type="application/json")

    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":"非推荐商品查询失败，请联系服务器管理人员","status":"error"}),content_type="application/json")

def recommendGoodsRow_to_dic(datas):
    myData=[];
    for data in datas:
        recommendId=data[1];
        recommendImg=data[2];
        recommendName = data[3]
        recommendTime = MyTool.none_or_strftime(data[4])
        goodsid = data[5]
        goodsInfo = getGoodsDetailByGoodsid(goodsid)
        tempDic = {"recommendId":recommendId , "recommendImg":recommendImg , "recommendName":recommendName , "recommendTime":recommendTime , "goods":goodsInfo}
        myData.append(tempDic)
    return myData

def getRecommendGoodsFn ():
    
    cursor = connection.cursor();
    cursor.execute("SELECT * FROM recommendGoods")
    datas=cursor.fetchall();
    cursor.close()
    myData = recommendGoodsRow_to_dic(datas)
    return myData

# 推荐商品获取接口
def getRecommendGoods (request):
    try:
        myData = getRecommendGoodsFn()
        return HttpResponse(json.dumps({"message":"查询成功","status":"ok" , "data":myData}),content_type="application/json")

    except Exception as identifier:
        return HttpResponse(json.dumps({"message":"商品推荐表查询操作失败","status":"error"}),content_type="application/json")   
# 推荐商品添加接口
def addRecommendGoods (request) :
    names = request.POST.getlist("recommendName")
    goodsIdList = request.POST.getlist("goodsid")
    imgs = request.FILES.getlist("imgsFile")

    try: 
        for itemIndex , item in enumerate(imgs):
            
            filepath = "./shopApp/static/myfile/recommendGoods";
            imgName = randomString() + ".jpg";
            filename = filepath + "/" + imgName
            
            filename = open(filename , "wb");
            filename.write(item.__dict__["file"].read());
            filename.close();

        
            recommendId = randomString()
            cursor=connection.cursor()
            sqlstr = "INSERT INTO recommendGoods (recommendId , recomendImg , recommendName , goodsid) VALUES ('%s' , '%s' , '%s' , '%s')" % (recommendId , "/static/myfile/recommendGoods/" + imgName , names[itemIndex] , goodsIdList[itemIndex]);
            cursor.execute(sqlstr)
            cursor.close()
        statusDic = MyTool.resultOk("插入数据成功")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
            
    
    except Exception as e: 
        statusDic = MyTool.resultError("插入数据失败")
        return HttpResponse(json.dumps(statusDic) , content_type = "application/json");
# 推荐商品删除接口 已完成
def delRecommendGoods(request):
    recommendIds = []
    imgs = []

    for key in request.POST:
        if "deleteId" in key:
            recommendIds.append(request.POST[key])
        if "deleteImg" in key:
            imgs.append(request.POST[key])

    cursor=connection.cursor();

    if len(recommendIds) <= 0:
        return HttpResponse(json.dumps({"message":'要删除0个数据吗？' , "status":"error"}) , content_type="application/json");

    try:
        sqlStr = "delete FROM recommendGoods WHERE recommendId in ("
        for deleteId in recommendIds:
            sqlStr = sqlStr + "'" + deleteId + "' ,"

        sqlStr = sqlStr[0:-1]
        sqlStr = sqlStr + ")"
        
        deleteCount = cursor.execute(sqlStr);
        cursor.close()

        if deleteCount == len(recommendIds):
            try:
                for imgPath in imgs:
                    imgPath = imgPath.split("/")
                    imgPath = imgPath[len(imgPath) - 1]
                    removePath = "../shopServer/shopApp/static/myfile/recommendGoods/" + imgPath
                    os.remove(removePath);
                        
            except Exception as e:
                
                return HttpResponse(json.dumps({'message': '删除图片失败......','status':'ok'}), content_type="application/json");
            
            return HttpResponse(json.dumps({'message': '删除成功','status':'ok'}), content_type="application/json");
        else: 
            return HttpResponse(json.dumps({'message': '删除失败','status':'error'}), content_type="application/json");
     
        
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":'数据库操作失败' , "status":"error"}) , content_type="application/json");


# 用户的搜索记录
def searchList(request):
    try:
        cursor = connection.cursor()
        sqlStr = "select * from search_history"
        cursor.execute(sqlStr)
        rows = cursor.fetchall()
        data = []
        cursor.close()
        for row in rows:
            tempDic = {
                'search_id':row[0] , 
                'wxid':row[1] , 
                'content':row[2] , 
                'search_type':row[3]
            }
            data.append(tempDic)

        return HttpResponse(json.dumps({'data': data,'status':'ok'}), content_type="application/json");
            

    except Exception as e:
        raise e
        return HttpResponse(json.dumps({"message":'搜索记录查询失败，请联系服务器管理人员' , "status":"error"}) , content_type="application/json");

def xunichongzhi(request):
    totalMoney = request.POST.get('totalMoney' , "")
    wxid = request.POST.get('wxid' , "")

    orderid = randomString()
    nonce_str = randomString() + 'abc'
    body = '嘉福祥-在线商城'


    res = getWxPayidFn({
        'body': body , 
        'orderid': orderid , 
        'totalMoney': totalMoney , 
        'wxid': wxid , 
        'nonce_str': nonce_str
    })
    if res['xml']['return_code']['$'] == 'SUCCESS':
        
        return HttpResponse(json.dumps({"message":'生成订单成功' , "status":"ok" , 'data':res}) , content_type="application/json");
    else :
        return HttpResponse(json.dumps({"message":'生成订单失败' , "status":"error" , 'data':res}) , content_type="application/json");

def getWxPayidFn(pass_data):
    url = "https://api.mch.weixin.qq.com/pay/unifiedorder"

    # 自己的appid和secret
    # appid = "wx619c085e365678c4"
    # secret = "12abb748fd981b90aa22f165817d231f"

    # 刘润东的appid和secret
    # appid = "wxe0df1aa623047849"
    # secret = "cd3f7ae6c5cb67e73a9317acaf8d0658"

    # 明川的appid和secret
    appid = "wxd789a73b4cea944d"
    # secret = "c920a96414e839d4509c19d6d1741882"


    # 刘润东的商户id
    # mch_id = '1275304201'

    # 明川的商户id
    mch_id = '1546074401'


    # 刘润东的 公网ip
    # spbill_create_ip = '39.98.74.72'

    # 教学部服务器的公网ip
    spbill_create_ip = '118.24.210.103'


    body = pass_data['body']
    body = body.encode('utf-8')
    nonce_str = pass_data['nonce_str']
    notify_url = 'http://' + my_global_host_url + '/weixinNotify_url/'
    openid = pass_data['wxid']
    out_trade_no = pass_data['orderid']
    sign_type = 'MD5'
    
    total_fee = str(int(float(pass_data['totalMoney']) * 100))
    trade_type = 'JSAPI'
    key = 'c920a96414e839d4509c19d6d1741882'

    device_info = 'WEB'
    # body : 商家名称-销售商品类目
    # detail : 商品详情
    # time_start : 
    # time_expire : 
    # product_id : 商品id
    
    pinjieString = 'appid=%s&body=%s&mch_id=%s&nonce_str=%s&notify_url=%s&openid=%s&out_trade_no=%s&sign_type=%s&spbill_create_ip=%s&total_fee=%s&trade_type=%s&key=%s'%(appid , body , mch_id , nonce_str , notify_url , openid , out_trade_no , sign_type , spbill_create_ip , total_fee , trade_type , key)
    hash = hashlib.md5()
    hash.update(pinjieString.encode())
    signature = hash.hexdigest()
    signature = signature.upper()

    params = """
        <xml>
	<appid><![CDATA[%s]]></appid>
	<body><![CDATA[%s]]></body>
	<mch_id><![CDATA[%s]]></mch_id>
	<nonce_str><![CDATA[%s]]></nonce_str>
	<notify_url><![CDATA[%s]]></notify_url>
	<openid><![CDATA[%s]]></openid>
	<out_trade_no><![CDATA[%s]]></out_trade_no>
	<sign_type><![CDATA[%s]]></sign_type>
	<spbill_create_ip><![CDATA[%s]]></spbill_create_ip>
	<total_fee><![CDATA[%s]]></total_fee>
	<trade_type><![CDATA[%s]]></trade_type>
	<sign>%s</sign>
</xml>
    """%(appid , body , mch_id , nonce_str , notify_url , openid , out_trade_no , sign_type , spbill_create_ip , total_fee , trade_type , signature)
    f = requests.post(url , data = params)
    res = f.content.decode()
    res = json.dumps(bf.data(fromstring(res)))
    res = json.loads(res)
    return res
# 服务器向微信下订单的接口
def getWxPayid(request):
    res = {"message":'测试,请调用getWxPayidFn(data)方法'}
    return HttpResponse(json.dumps({"data": res , "message":'向微信下单成功' , "status":"ok"}) , content_type="application/json");

# 微信支付结果的通知地址
def weixinNotify_url (request):
    return HttpResponse("收到微信支付结果的通知....")

# 微信网页授权文件获取的接口
def getTxt(request):
    return render(request , "MP_verify_OEMcT0UWO4grSYBg.txt")

# 创建随机字符串的方法
def createRandomString() :
    ran_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    return ran_str

# 获取当前时间戳的方法
def getTimeCuo():
    return str(int(time.time()))

# httpGet请求  获取 json 数据
def httpGetFn (urlStr):
    res = requests.get(urlStr)
    data = json.loads(res.text)
    return data

# 微信JS-SDK文件获取的接口
def getJSSDKTxt(request):
    return render(request , "MP_verify_gxBhgLWOaaVeJ6fr.txt")

# 润东网页授权txt
def rundongWangyeTxt(request):
    return render(request , "MP_verify_X8Xygw0Hvfgy0UZq.txt")

# 明川网页守缺网页授权txt
def mingchuanWangyeTxt(request):
    return render(request , "MP_verify_XkZ6EA7ucXFAwE0P.txt")


# 支付接口
def weixinPayFn(request):
    orderId = request.POST.get("orderid" , "")
    wxid = request.POST.get("wxid" , "")

    if orderId == "" or wxid == "":
        return HttpResponse(json.dumps({"message": "参数错误" , "status":"error"}) , content_type="application/json");

    cursor = connection.cursor()

    nowTime=datetime.datetime.now().strftime("%Y%m%d%H%M%S"); 
    
    sqlStr = "update ordertable set status=1 , payTime='%s' where orderId='%s'" % (nowTime , orderId)
    cursor.execute(sqlStr)

    # 用户
    order_info = getGoodsInfoArrByOrderId(orderId)
    rebeat_money = float(order_info["totalRebateMoney"])
    totalMoney = float(order_info["totalMoney"])
    
    sqlStr = "update user set rebate=rebate+%d , buyMoney=buyMoney+%d where wxid='%s'" % (float(rebeat_money) , float(totalMoney) , wxid)
    cursor.execute(sqlStr)
  
    # 返利列表
    for item in order_info["goodsArr"]:
        one_goods = item["goods"]
        one_goods_id = one_goods["goodsid"]
        rebate_money = float(one_goods["shop_price"]) * float(one_goods["rebate"]) * float(item["buyNumber"])
        rebate_id = randomString()
        rebate_str = "insert into rebatetable (rebateid , wxid , goodsid , rebateMoney) values ('%s' , '%s' , '%s' , '%s')" % (rebate_id , wxid , one_goods_id , rebate_money)
        cursor.execute(rebate_str)
        # 增加到 购买记录 列表中
        buyid = randomString()
        buy_number = item["buyNumber"]
        one_params = item["params"]

        buy_his_str = "insert into buyhistory (wxid , buyid , goodsid , number , params) values ('%s' , '%s' , '%s' , %d , '%s')" % (wxid , buyid , one_goods_id , int(buy_number) , one_params)
        cursor.execute(buy_his_str)

        # 减少库存量
        lose_kucun = "update goods set counts=counts-%d where goodsid = '%s'" % (int(buy_number) , one_goods_id)
        cursor.execute(lose_kucun)

        # 修改订单中商品的状态
        new_sql_str = "update order_goods_table set status = 1 where goodsid = '%s' and orderTableId = '%s'" % (one_goods_id , orderId)
        cursor.execute(new_sql_str)

    sqlStr = "select rebate , buyMoney from user where wxid='%s'" % wxid
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    data = {}
    for item in rows:
        data = {
            "rebeat_money":item[0] , 
            "total_money": item[1]
        }

    
    
    cursor.close()

    return HttpResponse(json.dumps({"message": "支付成功" , "data":data , "status":"ok"}) , content_type="application/json");



# 确认收货某一件商品
def querenshouhuoApi(request):
    goodsid = request.POST.get("goodsid" , "")
    orderid = request.POST.get("orderid" , "")

    if goodsid == "" or orderid == "":
        return HttpResponse(json.dumps({"message": "参数错误" , "status":"error"}) , content_type="application/json");


    sqlStr = "update order_goods_table set status = 3 where orderTableId = '%s' and goodsid = '%s'" % (orderid , goodsid)
    
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    cursor.close()

    if result == 1:
        return HttpResponse(json.dumps({"message":'收货成功' , "status":"ok"}) , content_type="application/json");
    else: 
        return HttpResponse(json.dumps({"message":'收货失败' , "status":"error"}) , content_type="application/json");


# 三级分类添加接口
def addSanjiFenlei(request):
    name = request.POST.get("name" , "")
    bigName = request.POST.get("bigName" , "")
    midName = request.POST.get("midName" , "")
    fatherId = request.POST.get("fatherid" , "")
    twoFenleiId = randomString()

    sqlStr = "insert into minfenlei (id , fatherid , name , bigName , midName) values ('%s' , '%s' , '%s' , '%s' , '%s')" % (twoFenleiId , fatherId , name , bigName , midName)
    
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    cursor.close()

    data = {
        "id":twoFenleiId , 
        "name":name
    }
    if result == 1:
        return HttpResponse(json.dumps({"message":'添加三级分类成功' , 'data':data , "status":"ok"}) , content_type="application/json");
    else: 
        return HttpResponse(json.dumps({"message":'添加三级分类失败' , "status":"error"}) , content_type="application/json");



    # return HttpResponse(json.dumps({"message":'数据库操作失败' , "status":"error"}) , content_type="application/json");

# 三级分类上传图片接口
def sanjiFenleiAddImage(request):
    headImgs = request.FILES.get("myfile" , "");
    sanjifenleiid = request.POST.get("sanjifenleiid" , "")
    if headImgs == "":
        return HttpResponse(json.dumps({"message":'请选择图片再提交' , "status":"error"}) , content_type="application/json");

    imgsName = randomString() + ".jpg"; 

    filepath = "./shopApp/static/myfile/classifyImgs";
    fullPath = filepath + "/" + imgsName
    
    fileHandle = open(fullPath , "wb");
    fileHandle.write(headImgs.__dict__["file"].read());
    fileHandle.close();

    sqlImagePath = "static/myfile/classifyImgs/" + imgsName
    sqlStr = "update minfenlei set image='%s' where id='%s'" % (sqlImagePath , sanjifenleiid)
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    cursor.close()
    
    if result >= 1:
        return HttpResponse(json.dumps({"message":'上传图片成功' , "data":{"imagePath":sqlImagePath} , "status":"ok"}) , content_type="application/json");
    else :
        return HttpResponse(json.dumps({"message":'上传图片失败' , "status":"error"}) , content_type="application/json");
    



# 三级分类删除接口
def deleteSanjiFenlie (request):
    deleteId = request.POST.get("deleteId" , "")
    if deleteId == "":
        return HttpResponse(json.dumps({"message":'请输入删除的id' , "status":"error"}) , content_type="application/json");

    deleteImage = request.POST.get("deleteImage" , "")
    deleteImageArr = deleteImage.split("/")
    if len(deleteImageArr) > 0:
        deleteImageName = deleteImageArr[len(deleteImageArr) - 1]
        if os.path.exists("../shopServer/shopApp/static/myfile/classifyImgs/" + deleteImageName)==True:
            os.remove("../shopServer/shopApp/static/myfile/classifyImgs/" + deleteImageName);

    sqlStr = "delete from minfenlei where id='%s'" % deleteId
    

    cursor = connection.cursor()
    result = cursor.execute(sqlStr)

    if result >= 1:
        return HttpResponse(json.dumps({"message":'删除成功' , "status":"ok"}) , content_type="application/json");
    else :
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    

# 三级分类数据接口
def getSanjifenleiData(request):
    fatherId = request.POST.get("fatherid" , "")

    sqlStr = "select * from minfenlei where fatherid='%s'" % fatherId

    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    allData = []
    for row in rows:
        tempDic = {
            'id': row[0] , 
            'fatherid':row[1] , 
            'name':row[2] , 
            'addtime':MyTool.none_or_strftime(row[3]),
            'image':row[4]
        }
        allData.append(tempDic)
    cursor.close()

    return HttpResponse(json.dumps({"data":allData , "status":"ok"}) , content_type="application/json");
    

# 添加二级分类的接口
def addTwoFenlei (request) :
    name = request.POST.get("name" , "")
    fatherId = request.POST.get("fatherId" , "")
    twoFenleiId = randomString()

    sqlStr = "insert into midfenlei (id , fatherid , name) values ('%s' , '%s' , '%s')" % (twoFenleiId , fatherId , name)
    
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    cursor.close()

    data = {
        "id":twoFenleiId , 
        "name":name
    }

    if result == 1:
        return HttpResponse(json.dumps({"message":'添加二级分类成功' , "data":data , "status":"ok"}) , content_type="application/json");
    else: 
        return HttpResponse(json.dumps({"message":'添加二级分类失败' , "status":"error"}) , content_type="application/json");

    # except Exception as e:
    #     return HttpResponse(json.dumps({"message":'数据库操作失败' , "status":"error"}) , content_type="application/json");

# 根据大分类 获取 二级分类的接口 
def getMinFenleiByBigFenlei(request):
    fatherId = request.POST.get("fatherid" , "")

    sqlStr = "select * from midfenlei where fatherid='%s'" % fatherId

    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    allData = []
    for row in rows:
        tempDic = {
            'id': row[0] , 
            'fatherid':row[1] , 
            'name':row[2] , 
            'addtime':MyTool.none_or_strftime(row[3])
        }
        allData.append(tempDic)
    cursor.close()

    return HttpResponse(json.dumps({"data":allData , "status":"ok"}) , content_type="application/json");
    

# 删除二级分类接口
def deleteErjiFenlei(request):
    deleteId = request.POST.get("deleteId" , "")
    if deleteId == "":
        return HttpResponse(json.dumps({"message":'请输入删除的id' , "status":"error"}) , content_type="application/json");

    cursor = connection.cursor()
    selectFromSanjifenleiStr = "select image from minfenlei where fatherid='%s'" % deleteId
    cursor.execute(selectFromSanjifenleiStr)
    allImage = cursor.fetchall()
    for item in allImage:
        imagePath = item[0]
        if os.path.exists("../shopServer/shopApp/" + imagePath)==True:
            os.remove("../shopServer/shopApp/" + imagePath);



    sqlStr = "delete from midfenlei where id='%s'" % deleteId

    
    result = cursor.execute(sqlStr)

    if result >= 1:
        return HttpResponse(json.dumps({"message":'删除成功' , "status":"ok"}) , content_type="application/json");
    else :
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    
    
# 添加大分类接口
def addBigFenlei(request):

    name = request.POST.get("name" , "")
    fenleiId = randomString()

    sqlStr = "insert into bigfenlei (id , name) values ('%s' , '%s')" % (fenleiId , name)
    
    cursor = connection.cursor()
    result = cursor.execute(sqlStr)
    cursor.close()

    if result == 1:
        return HttpResponse(json.dumps({"data":{"name":name , "id":fenleiId} , "status":"ok"}) , content_type="application/json");
    else: 
        return HttpResponse(json.dumps({"message":'添加大分类失败' , "status":"error"}) , content_type="application/json");



    # except Exception as e:
    #     return HttpResponse(json.dumps({"message":'数据库操作失败' , "status":"error"}) , content_type="application/json");


# 大分类删除接口
def deleteBigFenlei(request):
    deleteId = request.POST.get("deleteId" , "")
    if deleteId == "":
        return HttpResponse(json.dumps({"message":'请输入删除的id' , "status":"error"}) , content_type="application/json");



    cursor = connection.cursor()
    erjifenleiStr = "select id from midfenlei where fatherid='%s'" % deleteId
    cursor.execute(erjifenleiStr)
    allIds = cursor.fetchall()
    for item in allIds:

        sanjifenleiImageStr = "select image from minfenlei where fatherid='%s'" % item[0]
        cursor.execute(sanjifenleiImageStr)
        allImage = cursor.fetchall()
        for oneImage in allImage:
            if os.path.exists("../shopServer/shopApp/" + oneImage[0])==True:
                os.remove("../shopServer/shopApp/" + oneImage[0]);


    sqlStr = "delete from bigfenlei where id='%s'" % deleteId
    result = cursor.execute(sqlStr)

    if result >= 1:
        return HttpResponse(json.dumps({"message":'删除成功' , "status":"ok"}) , content_type="application/json");
    else :
        return HttpResponse(json.dumps({"message":'删除失败' , "status":"error"}) , content_type="application/json");
    

# 根据大分类获取下面的所有分类数据 供移动端使用
def getAllFenleiByDafenleiId(request):
    dafenleiId = request.POST.get("dafenleiId" , "")
    if dafenleiId == "":
        return HttpResponse(json.dumps({"message":'请传入一级分类的id' , "status":"error"}) , content_type="application/json");

    allData = []
    erjiSqlStr = "select * from midfenlei where fatherid='%s'" % dafenleiId
    cursor = connection.cursor()
    cursor.execute(erjiSqlStr)
    erjiRows = cursor.fetchall()
    for erjiRow in erjiRows:
        erjiTempDic = {
            "id":erjiRow[0] , 
            "fatherid":erjiRow[1] , 
            "name":erjiRow[2] , 
            "addtime":MyTool.none_or_strftime(erjiRow[3]),
            "data":[]
        }
        sanjiSqlStr = "select * from minfenlei where fatherid='%s'" % erjiRow[0]
        cursor.execute(sanjiSqlStr)
        sanjiRows = cursor.fetchall()
        for sanjiRow in sanjiRows:
            sanjiTempDic = {
                "id":sanjiRow[0] , 
                "fatherid":sanjiRow[1] , 
                "name":sanjiRow[2] , 
                "addtime":MyTool.none_or_strftime(sanjiRow[3]),
                "image":sanjiRow[4]
            }

            erjiTempDic["data"].append(sanjiTempDic)

        allData.append(erjiTempDic)

    return HttpResponse(json.dumps({"data":allData , "status":"ok"}) , content_type="application/json");


# 大分类接口列表
def allBigFenlei(request):

    sqlStr = "select * from bigfenlei"
    cursor = connection.cursor()
    cursor.execute(sqlStr)
    rows = cursor.fetchall()
    cursor.close()

    allData = []

    for row in rows:
        tempDic = {
            'id':row[0] , 
            'name':row[1] , 
            'addtime':MyTool.none_or_strftime(row[2])
        }

        allData.append(tempDic)
    


    return HttpResponse(json.dumps({"data":allData , "status":"ok"}) , content_type="application/json");



import csv
# csv上传文件接口
def uploadCSVFile(request):
    try:
        minFenleiName = request.POST.get("minFenleiName" , "")
        if minFenleiName == "":
            return HttpResponse(json.dumps({"message":'参数出错' , "status":"error"}) , content_type="application/json");

        minFenleiId = ""
        minFenleiStr = "select id from minfenlei where name='%s'" % minFenleiName

        cursor = connection.cursor()

        cursor.execute(minFenleiStr)

        minFenleiRows = cursor.fetchall()
        for minFenleiRow in minFenleiRows:
            minFenleiId = minFenleiRow[0]

        myfile = request.FILES["myfiles"].__dict__["file"]

        xxx = request.FILES["myfiles"]

        xxx = xxx.read()
        myArr = []
        try:
            myArr = xxx.decode("utf-8").split("\r\n")
        except Exception as e:    
            myArr = xxx.decode("gbk").split("\r\n")
        

        firstLength = 0

        

        sqlStr1 = "insert into goods ("
        sqlStr2 = ""
        for i , item in enumerate(myArr):
            if len(item) <= 0:
                break
            minArr = item.split(",")
                
            if i == 0:
                firstLength = len(minArr)
                for minItem in minArr:
                    minItem = minItem.replace("\ufeff" , "")
                    sqlStr1 = sqlStr1 + minItem + ","
                sqlStr1 = sqlStr1[0:-1]
                sqlStr1 = sqlStr1 + ",goodsid,xiaoClassiData) values ('"
            else:
                currentLength = len(minArr)
                if currentLength - 1 == firstLength:
                    minArr.pop()
                for minItem in minArr:
                    sqlStr2 = sqlStr2 + minItem + "','"
                
                sqlStr2 = sqlStr2 + randomString() + "','" + minFenleiId + "')"

                allString = sqlStr1 + sqlStr2
                allString = allString.replace('"' , '')
                result = cursor.execute(allString)

                if result >= 1:
                    sqlStr2 = ""
                else:
                    return HttpResponse(json.dumps({"data":'第' + str(i) + "条数据插入失败" , "status":"error"}) , content_type="application/json");

        

        return HttpResponse(json.dumps({"message":'上传成功' , "status":"ok"}) , content_type="application/json");

    except Exception as e:    
        raise e
        return HttpResponse(json.dumps({'status':'error' , 'message':'上传操作失败，请联系服务器管理人员'}) , content_type="application/json")



def lihangjiekou(request):
    echostr = request.GET.get('echostr' , "")
    if echostr == "":
        return HttpResponse(json.dumps({'status':'ok' , 'message':'开始进行业务逻辑算法'}) , content_type="application/json")
    else :
        return HttpResponse(echostr)

def tianxiaopengjiekou(request):
    echostr = request.GET.get('echostr' , "")
    if echostr == "":
        return HttpResponse(json.dumps({'status':'ok' , 'message':'开始进行业务逻辑算法'}) , content_type="application/json")
    else :
        return HttpResponse(echostr)

def fcyjiekou(request):
    echostr = request.GET.get('echostr' , "")
    if echostr == "":
        return HttpResponse(json.dumps({'status':'ok' , 'message':'开始进行业务逻辑算法'}) , content_type="application/json")
    else :
        return HttpResponse(echostr)

def yanjiushengjiekou(request):
    echostr = request.GET.get('echostr' , "")
    if echostr == "":
        return HttpResponse(json.dumps({'status':'ok' , 'message':'开始进行业务逻辑算法'}) , content_type="application/json")
    else :
        return HttpResponse(echostr)

def xiongdajiekou(request):
    echostr = request.GET.get('echostr' , "")
    if echostr == "":
        return HttpResponse(json.dumps({'status':'ok' , 'message':'开始进行业务逻辑算法'}) , content_type="application/json")
    else :
        return HttpResponse(echostr)

def lianxiyangjiekou(request):
    echostr = request.GET.get('echostr' , "")
    if echostr == "":
        return HttpResponse(json.dumps({'status':'ok' , 'message':'开始进行业务逻辑算法'}) , content_type="application/json")
    else :
        return HttpResponse(echostr)

def lxyjiekou(request):
    echostr = request.GET.get('echostr' , "")
    if echostr == "":
        return HttpResponse('jklasd')
    else :
        return HttpResponse(echostr)



def getcodeDemo(request):
    temp_code = request.GET.get("code" , "")

    get_acstk_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=wx619c085e365678c4&secret=12abb748fd981b90aa22f165817d231f&code=" + temp_code + "&grant_type=authorization_code"

    my_result = requests.get(get_acstk_url)
    my_result = my_result.text
    my_result = json.loads(my_result)


    my_openid = my_result["openid"]
    my_accstk = my_result["access_token"]


    user_info_url = "https://api.weixin.qq.com/sns/userinfo?access_token=" + my_accstk + "&openid=" + my_openid + "&lang=zh_CN"
    my_result1 = requests.get(user_info_url)
    my_result1 = my_result1.text
    my_result1 = json.loads(my_result1)




    return HttpResponse("xxxxx")


def lihanghtml(request):
    return render(request , "lihang.html");
def chenhaijiaohtml(request):
    return render(request , "chenhaijiao.html");
def fcyhtml(request):
    return render(request , "fcy.html");
def tianxiaopenghtml(request):
    return render(request , "tianxiaopeng.html");
def songchenfeihtml(request):
    return render(request , "songchenfei.html");
def xiongdahtml(request):
    return render(request , "xiongda.html");
def lianxiyanghtml(request):
    return render(request , "lianxiyang.html");


