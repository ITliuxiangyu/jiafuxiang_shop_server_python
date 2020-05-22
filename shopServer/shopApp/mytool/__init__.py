import os
import time
from django import forms
from django.shortcuts import render_to_response
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import render
from django.http import HttpResponse
import json, urllib
#用django自带的forms将图片下载到本地并返回地址

class MyTool():
    def resultOk(msg="操作成功" , data={}):
        return {"status" : "ok" , "message" : msg , "data":data};

    def resultError(msg="操作失败" , data={}):
        return {"status" : "error" , "message" : msg , "data":data};

    def returnJson(dic):
        return HttpResponse(json.dumps(dic) , content_type="application/json")

    def none_or_strftime(aaa):
        if aaa is None or isinstance(aaa,str):
            return ''
        else :
            return aaa.strftime('%Y-%m-%d %H:%M:%S')

    def server_str():
        return 'jiafuxiang_server'

    def global_domain():
        return 'gongzhong.huidianit.com'
    

class UserForm(forms.Form):
    headImg = forms.FileField()
class imagesupload(object):
    def upload(self , request):
        uf = UserForm(request.POST,request.FILES)
        if uf.is_valid():
            headImg = uf.cleaned_data['headImg']
            headImg.__dict__["_name"] = str(int(time.time()*1000))+'.jpg'
            filepath = "./shopApp/static/myfile/";
            filename = os.path.join(filepath,headImg.__dict__["_name"])
            filename = open(filename , "wb");
            filename.write(headImg.__dict__["file"].read());
            sqlfilename = filepath+headImg.__dict__["_name"]
            return sqlfilename
           
            