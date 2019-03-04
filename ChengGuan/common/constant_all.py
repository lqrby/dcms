#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-07-09 14:00
# constant/constant_1.py
# 常量部分（固定不变使用频繁的参数维护在此处）

from PIL import Image
import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from com.aliyun.api.gateway.sdk import client
# from com.aliyun.api.gateway.sdk.http import request
# from com.aliyun.api.gateway.sdk.common import constant
import base64
import json
import requests
import os.path
import urllib
import time
import urllib, sys
from PIL import Image
from selenium import webdriver
import time
from PIL import ImageGrab
class getConstant():
    # IP = "http://219.149.226.180"
    IP = "http://122.137.242.91"
    # IP = "http://122.137.242.15"
    # IP_WEB_180 = "http://219.149.226.180:7897"
    # IP_APP_180 = "http://219.149.226.180:7880"
    PORT_7897 = ":7897" #180服务城管>接口
    PORT_7880 = ":7880" #180服务爱吉林>接口
    PORT_7884 = ":7884" #180服务爱吉林>上传文件图片
    PORT_7890 = ":7890" #180服务执法局apk>巡检抽查
    # IP_WEB_91 = "http://122.137.242.91"
    PROJECT_PATH = "E:/test/dcms/ChengGuan"

    

    #是否需要核实(核实1，无需核实0)
    NEEDCONFIRM_YES	= "1"
    NEEDCONFIRM_NO = "0"


    #核实有效:402880822f3eca29012f3ed0218c0002   核实无效:402880822f3eca29012f3ecf72020001
    HSYX = '402880822f3eca29012f3ed0218c0002'
    HSWX = '402880822f3eca29012f3ecf72020001'

    #处理方式(复核1，回访0)
    ISFH_YES = "1"
    ISFH_NO = "0"

    #案卷类型(事件/部件)
    EORCID_SJ = "402880822f4dbfd8012f4df791c70010"
    EORCID_BJ = "402880822f4dbfd8012f4df7d20c0011"
    
    #======================================================#
    #************************事件类型***********************#
    #======================================================#
    #事件大类
    SJ_SRHJ = "402880ea2f53fedc012f5400964d000d" #市容环境
    SJ_XCGG = "402880822f2d8d88012f2d9013f70001" #宣传广告
    SJ_SGGL = "402880822f2d8d88012f2d9052480002" #施工管理
    SJ_JMZX = "402880822f2f6d61012f2f74123f0001" #街面秩序

    #事件小类

    #市容环境》小类
    SJ_SRHJ_DLBJ = "402881795961e05b015961f1fb01000e" #道路不洁
    SJ_SRHJ_SDLJ = "4028838358b04eb70158b2df134e525e" #私搭乱建
    SJ_SRHJ_LDZL = "4028838358b04eb70158b2dfb4a95262" #绿地脏乱、小片荒
    SJ_SRHJ_JZLJ = "4028838358b04eb70158b2df69d95260" #建筑垃圾、渣土管理
    SJ_SRHJ_DLYS = "4028838358b04eb70158b2e0296c5264" #道路遗撒
    SJ_SRHJ_YYWR = "4028838358b04eb70158b2e071ce5266" #油烟污染
    SJ_SRHJ_SZSY = "4028838358b04eb70158b2e0c5f15268" #擅自饲养家禽家畜
    SJ_SRHJ_DLPS = "402881795961e05b015961f28cc00011" #道路破损
    
    #宣传广告》小类
    SJ_XCGG_FFXGG = "4028838358b04eb70158b301a4a85273" #非法小广告
    SJ_XCGG_GGPPS = "4028838358b04eb70158b304c2e4527b" #广告招牌破损
    SJ_XCGG_JTFGG = "4028838358b04eb70158b304973b5279" #街头散发广告
    SJ_XCGG_WZPB = "4028838358b04eb70158b303dc465275" #违章张贴悬挂广告牌匾
    SJ_XCGG_ZDGGP = "4028838358b04eb70158b30421535277" #占道广告牌
    
    #施工管理》小类
    SJ_SGGL_WZJL = "4028838358b04eb70158b30591ce527f" #无证掘路
    SJ_SGGL_SGZD = "4028838358b04eb70158b30562b0527d" #施工占道
    SJ_SGGL_GDYC = "402881795961e05b015961efccca0009" #工地扬尘
    SJ_SGGL_GDYC = "402881795961e05b015961ef86490007" #施工扰民

    #街面秩序》小类
    SJ_JMZX_SYZY = "402881795961e05b015961ee3d780004" #商业噪音
    SJ_JMZX_LDJY = "4028838358b04eb70158b305e27e5281" #流动经营
    SJ_JMZX_LTSK = "4028838358b04eb70158b3068ac75289" #露天烧烤
    SJ_JMZX_JDCLTF = "4028838358b04eb70158b30639825285" #机动车乱停放
    SJ_JMZX_LDLF = "4028838358b04eb70158b30664bb5287" #乱堆乱放
    SJ_JMZX_DWJY = "4028838358b04eb70158b3060f4e5283" #店外经营


    #====================================================#
    #***********************部件类型**********************#
    #====================================================#
    #部件件大类
    BJ_JTSS = "402881795961e05b015961e8c6660002" #交通设施
    BJ_GGSS = "402880923338d4ff013339bb523e0d1d" #公共设施
    BJ_SRHJ = "402880923338d4ff013339158e0606b5" #市容环境
    BJ_YLLH = "402880923338d4ff013339a131470a1a" #园林绿化设施

    #部件小类
    #交通设施>小类
    BJ_JTSS_DXTD = "402881795961e05b015961f61fd4001e" #地下通道
    BJ_JTSS_KHQ = "402881795961e05b015961f6715d0022" #跨河桥
    BJ_JTSS_GJLJQ = "402881795961e05b015961f649530020" #高架立交桥
    BJ_JTSS_GJTQ = "402881795961e05b015961f5c890001c" #过街天桥

    #公共设施>小类
    BJ_GGSS_RLJG = "4028838358b04eb70158b2bf57ce5238" #热力井盖
    BJ_GGSS_WSJG = "4028838358b04eb70158b2b6b3395228" #污水井盖
    BJ_GGSS_SSJG = "4028838358b04eb70158b2b62fe95226" #上水井盖
    BJ_GGSS_DSJG = "4028838358b04eb70158b2be02ee5236" #电视井盖
    BJ_GGSS_RQJG = "4028838358b04eb70158b2bff760524d" #燃气井盖
    BJ_GGSS_DLJG = "4028838358b04eb70158b2bc16da522c" #电力井盖
    BJ_GGSS_TXJG = "4028838358b04eb70158b2bcf50b5231" #通讯井盖
    BJ_GGSS_YSBZ = "4028838358b04eb70158b2b727ec522a" #雨水箅子
    BJ_GGSS_XFJG = "4028838358b04eb70158b2c04e785250" #消防井盖
    BJ_GGSS_LD = "402881795961e05b015961f75e690024" #路灯

    #市容环境>小类
    BJ_SRHJ_LJX = "4028838358b04eb70158b2c116945252" #垃圾箱
    BJ_SRHJ_GGPB = "4028838358b04eb70158b2c181d45254" #广告牌匾
    BJ_SRHJ_GGCS = "402881795961e05b015961f494e40018" #公共厕所
    BJ_SRHJ_LJJ = "402881795961e05b015961f4c7b6001a" #垃圾间

    #园林绿化设施>小类
    BJ_YLLH_LD = "4028838358b04eb70158b2c27d4f5258" #绿地
    BJ_YLLH_DS = "8a8a84835c3dcaea015c48f712ae047d" #雕塑
    BJ_YLLH_PQ = "8a8a84835c3dcaea015c48f7dab1047f" #喷泉
    
    BJ_YLLH_HDS = "8a8a84835c3dcaea015c48f5f4ab0479" #行道树
    BJ_YLLH_DLS = "8a8a84825c3dc7cb015c48f633f404e3" #独立树
    BJ_YLLH_GSMM = "4028838358b04eb70158b2c22d265256" #古树名木
    BJ_YLLH_LDHL = "4028838358b04eb70158b2c2cea7525a" #绿地护栏
    BJ_YLLH_HSSS = "8a8a84835c3dcaea015c48f693f8047b" #护树设施
    BJ_YLLH_HJHB = "8a8a84825c3dc7cb015c48f6ce8e04e5" #花架花钵
    BJ_YLLH_JTZY = "8a8a84825c3dc7cb015c48f7537d04e7" #街头坐椅
    BJ_YLLH_LDWHSS = "8a8a84825c3dc7cb015c48f7a39104e9" #绿地维护设施
    BJ_YLLH_QTYLSS = "8a8a84825c3dc7cb015c48f80f9904eb" #其他园林绿化设施






    #待派发列表url
    dpf_ListUrl = '/dcms/cwsCase/Case-dispatchlist.action?casestate=20&menuId=4028338158a414bd0158a484daae000e&keywords=402880ea2f6bd924012f6c521e8c0034'
    #待调整列表url
    dtz_ListUrl = '/dcms/cwsCase/Case-adjustlist.action?casestate=40&menuId=402880822f9490ad012f949b98b4004c&keywords=402880eb2f90e905012f9138a5fb00a4'
    #派发/调整/挂起
    pf_url = '/dcms/cwsCase/Case-dispatch.action'
    
    #申请非正常结案url
    sqfzcja_url = '/dcms/cwsCase/Case-applyabnormal.action'



    #构建维护系统>>用户权限配置
    authority_XJCC = "402883845f295831015f296be837003d"        #巡检抽查
    authority_YYWR = "8a8a848260e4cad20160e80d173a1a61"        #油烟污染
    authority_DCKH = "8a8a848261464b200161543976571a61"        #督查考核
    authority_JTJT = "8a8a8482645fd43301645fd8461c0020"        #静态交通
    authority_DBZD = "402883835baa13f2015bad850b66000c"        #督办指导
    authority_WFJJ = "8a8a84835f9608f8015fa4f582f61c5d"        #违法建筑
    authority_LT = "8a8a848361464faa01615438e5051c37"          #论坛
    authority_LD = "8a8a84835adcc7b3015ba3ec8296345f"          #领导

    



