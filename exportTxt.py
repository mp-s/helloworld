#coding=utf-8

import os,sys,codecs

def getFileList(path, fl):  #return a list
    try:
        files = os.listdir(path)
        for f in files:
            subPath = path + '\\' + f
            if (os.path.isdir(subPath)):
                getFileList(subPath, fl)
            else:
                if(os.path.splitext(subPath)[1] == '.txt'):
                    fl.append(subPath)
    except: #permission denied
        pass

def readExportTBL(tblPath):
    #if os.path.isfile(tblPath):
    tbl = {}
    tblFile = open(tblPath)
    for line in tblFile.readlines():
        if (line != '\n'):
            d = line.split('=')
            tblHex, tblWord = d[0], d[1][:-1].decode('utf-8')
            tbl[tblHex] = tblWord  # reverse Dict work for export tool
            #line = line.decode('utf-8')
    return tbl

def readFile(filePath, targetPath, tbl):
    #fobj = open(filePath, 'r')
    fInput = codecs.open(filePath, 'r', encoding='shiftjis')  #read with shift-jis encode
    #fOutput = codecs.open(targetPth, 'w', 
    fout = open(targetPath, 'w')

    for line in fInput.readlines():
        lineBuff = ''
        for word in line:    # sjis -> syscode
        # 如果直接转hex会导致不会按字符分割，只会按字节分割
            exportHex = word.encode('shiftjis').encode('hex')
            if exportHex == '0a':
                lineBuff += u'\n'
            elif exportHex == '0d':
                pass
            else:
                lineBuff += tbl[exportHex.upper()]
        fout.write(lineBuff.encode('utf-8'))

def main(input, tblPath='.\\tableData.tbl'):
    '''
    文件夹时候，out不存在，使用默认的输出目录
    out存在时 使用outputList
    文件时候， out不存在，使用默认输出文件名
    out存在时，直接给输出文件名为export.txt
    '''
    #file
    tbl = readExportTBL(tblPath)
    if os.path.isfile(input) and os.path.splitext(input)[1] == '.txt':
        readFile(input, '.\\export.txt', tbl)
    elif os.path.isdir(input):
        fileList = []
        getFileList(input, fileList)
        for path in fileList:
            targetPath = '.\\target' + path.lstrip(input)
            targetPathdir = os.path.dirname(targetPath)
            if not os.path.exists(targetPathdir):
                os.makedirs(targetPathdir)
            print 'Converting : ' + targetPath
            
            readFile(path, targetPath, tbl)
    else: pass

if __name__ == "__main__":
    '''
    tbl = readExportTBL('.\\tableData.tbl')
    readFile('.\\sjisFile.txt', '', tbl)
    '''
    main(sys.argv[1])