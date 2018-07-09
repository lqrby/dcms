# -*- coding: UTF-8 -*-  
from bs4 import BeautifulSoup 
from selenium import webdriver
from time import *
import os,sys
import re
import linecache
def tiqu(): 
#     f = open('1234.txt', 'r')
#     a=(f.read())
#     f.close() 
#     f = open('1235.txt', 'r')   
#     f.read()
    count=(linecache.getline(r'1235.txt',57))
    fw=open('data.txt','w')
    fw.write(count)
    fw.close() 
    f = open('data.txt', 'r')
    a=(f.read())
    print(a)
    b=a[80]+a[81]+a[82]+a[83]+a[84]+a[85]+a[86]+a[87]+a[88]+a[89]+a[90]+a[91]+a[92]+a[93]+a[94]+a[95]+a[96]+a[97]+a[98]+a[99]+a[100]+a[101]+a[102]+a[103]+a[104]+a[105]+a[106]+a[107]+a[108]+a[109]+a[110]+a[111]
    print(b)
if __name__ == '__main__':
    tiqu()
