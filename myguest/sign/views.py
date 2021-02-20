from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from  django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import render,get_object_or_404
import json
import os
import string
import re
# Create your views here.
def index(request):
    return render(request,"index.html")

def login_action(request):#登录
    if request.method=="POST":
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)#登录(不加此句，登录成功不跳转)
            response=HttpResponseRedirect('/event_manage/')
            request.session["user"]=username#设置session
            return response
        else:
            return render(request,'index.html',{'error':'username or password error!'})

@login_required
def event_manage(request):#发布会管理
    #username=request.COOKIES.get("user","")#读取浏览器cookie
    username=request.session.get("user","")#读取浏览器session
    event_list=Event.objects.all()
    return render(request,"event_manage.html",{"user":username,"events":event_list})

@login_required
def search_name(request):#通过名称、地址搜索
    username = request.session.get("user", "")  # 读取浏览器session
    search_name=request.GET.get("name","")
    event_list = Event.objects.filter(Q(name1__contains=search_name) | Q(address1__contains=search_name))
    return render(request,"event_manage.html",{"user":username,"events":event_list})


@login_required
def guest_manage(request):#嘉宾管理
    username=request.session.get("user","")
    guest_list=Guest.objects.all()
    paginator=Paginator(guest_list,10)#每页显示10条数据
    page=request.GET.get("page")
    try:
        contacts=paginator.page(page)
    except PageNotAnInteger:
        contacts=paginator.page(1)
    except EmptyPage:
        contacts=paginator.page(paginator.num_pages)
    return render(request,"guest_manage.html",{"user":username,"guests":contacts})

@login_required
def sign_index(request):#签到页面
    event_id=request.GET.get("eid")
    return render(request,'sign_index.html',{"event_id":event_id})

@login_required
def sign_index_action(request):
    if request.method == "GET":
        event_id = request.GET.get("eid")
        print(event_id)
        event =str(get_object_or_404(Event, id=event_id))
        phone=request.GET.get("phone")
        result=Guest.objects.filter(phone=phone).first()
        if not result:
           return HttpResponse(json.dumps({'msg': '手机号输入有误，请重新输入'}))
        result = Guest.objects.filter(phone=phone, event_id=event_id)
        if not result:
           return HttpResponse(json.dumps({'msg': '手机号或者发布会有误，请重新输入'}))
        if result.sign:
                return HttpResponse(json.dumps({'msg': '已签到'}))
        else:
                Guest.objects.filter(phone=phone, event_id=event_id).update(sign="1")
                return HttpResponse(json.dumps({"event":event,'msg': '签到成功'}))

def code_manage(request):
    return render(request,"code_manage.html")

def totalcodeline(filepath,codetype):
    space_line=0
    comment_line=0
    valid_line=0
    flag = False
    dic={}
    for root,dirs,files in os.walk(filepath):
        for file in files:
            if "py" in codetype:
                if file.endswith(".py"):
                    with open(os.path.join(root,file),"r",encoding="utf-8") as fp:
                         datalines=fp.readlines()
                         for line in datalines:
                             if line.strip() in string.whitespace:
                                 space_line+=1
                             elif line.strip()[0]=="#":
                                 comment_line+=1
                             elif re.findall(r"^\'\'\'", line) and flag == False:
                                 comment_line += 1
                                 flag = True
                             elif re.findall(r"^\'\'\'", line) and flag == True:
                                 comment_line += 1
                                 flag = False
                             elif flag:
                                 comment_line += 1
                             else:
                                 valid_line += 1
    dic["space"]=space_line
    dic["comment"]=comment_line
    dic["valid"]=valid_line
    dic["all"]=space_line+comment_line+valid_line
    return dic

def search_manage(request):
    if request.method=="GET":
        filepath=request.GET.get("path")
        codetype=request.GET.get("codetype")
        if filepath.strip()!=" " and codetype.strip()!=" ":
           dic=totalcodeline(filepath,codetype)
           newdic=json.dumps(dic,ensure_ascii=False)
           return HttpResponse(newdic)










