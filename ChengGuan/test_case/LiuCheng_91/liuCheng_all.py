
# # -*- coding: utf-8 -*-

# import json,os,sys
# from selenium import webdriver
# from test_login import allLogin
# from test_jobEntry import test_submitOrder
# from test_liAn import test_detailsAndFiling
# from test_paiFa import test_sendDetailsAndSendOut
# from test_chuLi import fileFandling
# from test_fuHeAndHuiFang import test_reviewAndReturnVisit

# class liuCheng():
#     # web坐席工单录入(无需核实需要复核)》web立案》web派发》权属单位处理》apk网格管理员复核》结束
#     def test_liucheng_1(self):
#         # #移动端登录
#         # appLogin = allLogin().test_app_allLogin()
#         # #web端登录
#         # driver = webdriver.Chrome("D:/python/chromeDriverSever/chromedriver.exe")
#         # webLogin = allLogin().test_web_login(driver)
#         # while appLogin == False:
#         #     appLogin = allLogin().test_app_allLogin()
#         # while webLogin==False:
#         #     webLogin = allLogin().test_web_login(driver)
#         # 工单录入
#         webgdlr_res = test_submitOrder().test_web_submitOrder()
#         if webgdlr_res:
#             #立案
#             lian_result = test_detailsAndFiling()
#             if lian_result:
#                 #派发
#                 paifa_result = test_sendDetailsAndSendOut()
#                 if paifa_result:
#                     # 处理 移动端权属单位apk处理
#                     qsdw_result = fileFandling().test_app_qsdw_handlingDetailsAndHandling()
#                     if qsdw_result:
#                         #网格管理员apk复核
#                         test_reviewAndReturnVisit().test_app_wggly_returnDetailsAndVisit()
            

# # if __name__=="__main__":
# #     liuCheng().test_liucheng_1()