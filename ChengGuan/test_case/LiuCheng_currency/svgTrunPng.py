#coding = utf-8
import os,json
import cairosvg
from bs4 import BeautifulSoup
import chardet

def export(fromDir,colers, targetDir, exportType):
        print("开始执行转换命令...")
        # files = os.listdir(fromDir)
        num = 0
        newPathArr = []
        i = 1
        for (filePath,coler) in zip (fromDir,colers):
            # path = os.path.join(fromDir,fileName)
            if os.path.isfile(filePath) and filePath[-3:] == "svg":
                num += 1
                fileHandle = open(filePath)  #<_io.TextIOWrapper name='E:/test/tubiao1/010105.svg' mode='r' encoding='cp936'> <class '_io.TextIOWrapper'>
                svg = fileHandle.read()
                svg = svg.replace('path','path fill='+coler)
                svg = svg.replace('polygon','polygon fill='+coler)
                fileHandle.close()
                # print("svg类型为：",type(svg),svg)    #str类型
                exportPath = os.path.join("", filePath[:-4]+str(i)+"."+ exportType)
                i+=1
                exportFileHandle = open(exportPath,'w')
                if exportType == "png":
                    cairosvg.svg2png(bytestring=svg, write_to=exportPath)
                    newPathArr.append(exportPath)
                exportFileHandle.close()
                print("Success Export ", exportType, " -> " , exportPath)
            else:
                print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX图标不是svg格式XXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                return fromDir
        print("已导出 ", num, "个文件")
        print("路径是",newPathArr)
        return newPathArr
        
        
        


if __name__ == '__main__':
    oneAndTwe = "E:/test/tubiao1/010103.svg"
    threeAndFour = "E:/test/tubiao1/010105.svg"
    locn_red = '"#3d99fc"'
    locn_blue = '"#ff0000"'
    hs_picpath1 = oneAndTwe
    hs_picpath2 = oneAndTwe
    hs_picpath3 = threeAndFour
    hs_picpath4 = threeAndFour

    # itemData['labelcolor'] = locn_red
    # itemData['labelredcolor'] = locn_blue
    # itemData['localcolor'] = locn_red
    # itemData['localredcolor'] = locn_blue
    colers = [locn_red,locn_blue,locn_red,locn_blue]
    fromDir = [hs_picpath1,hs_picpath2,hs_picpath3,hs_picpath4]
    targetDir = 'E:/test/tubiao'
    exportType = 'png'
    export(fromDir,colers, targetDir, exportType)