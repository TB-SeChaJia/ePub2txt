#encoding=utf8

import os,sys
import re
import shutil
import zipfile
from bs4 import BeautifulSoup as BS



class GetContent():
    def __init__(self,path):
        html = open(path)
        self.objs = BS(html)
        self.title = self.objs.title.string
        print("title is ",self.title)

    def gettext(self):
        text = ""
        for string in self.objs.strings:
            if re.search("[\u0F00-\u0FFF]+",string):
                text += string
        return text

def embedded_numbers(url):
    pieces = re.findall(r"([0-9]+\.x?html$)",url)[-1]
    pieces = re.findall("[0-9]+",pieces)[0]
    return int(pieces)

def sort_with_embedded_numbers(urls):
    aux = [(embedded_numbers(url), url) for url in urls]
    aux.sort()
    return [url for _,url in aux]
    
def get_urls(path):
    global URLS
    listdirs = os.listdir(path)
    htmls  = [os.path.join(path,dir) for dir in listdirs if re.search(r"[0-9]\.(x)?html$",dir)]
    others = [path+"/"+dir for dir in listdirs if os.path.isdir(path+"/"+dir)]
    URLS.extend(htmls)
    for dir in others:
        get_urls(dir)
    aa = URLS
    #print("Old urls == >",len(aa))
    return aa
        
        
def rename_urls(path,urls):
    name = 1
    newurls = []
    for url in urls:
        newname = os.path.join(path,str(name)+re.findall("\.x?html$",url)[-1])
        os.rename(url,newname)
        newurls.append(newname)
    return newurls
        

    

if __name__ == "__main__":

    DIR1 = "./EPUB/"	
    DIR2 = "./TXT/"
    
	
    if not os.path.exists(DIR1):
        os.mkdir(DIR1)
    if not os.path.exists(DIR2):
        os.mkdir(DIR2)
	    
    if len(sys.argv) == 1:
    	print("epub change to txt all!")
    	dirlist = os.listdir()
    	dirlist = [dl for dl in dirlist if re.search(".epub$",dl)]
    elif len(sys.argv) == 2:
        print("epub2txt.py sample.epub")
        dirlist = [sys.argv[1]]
    else:
        print("python3 epub2txt.py sample.epub -OR- python3 epub2txt.py")
        sys.exit()
	
    Error = []
    for dl in dirlist:
        try:
            fn = os.path.basename(dl)
            fn1 = fn.split(".")[0]
            path = DIR1+fn1
            if not os.path.exists(path):
                os.mkdir(path)

            command = "unzip -n -d {0} {1}".format(path,dl)
            print("command ==>> ",command)
            os.system(command)
            
            URLS = []
            urls = get_urls(os.path.join(os.getcwd(),path))
            html_list = sort_with_embedded_numbers(urls)
            print("Old urls == >",len(html_list))
            newurls = rename_urls(path,html_list)
            print("New urls ===============> :",len(newurls))
            write_file = DIR2+fn1+".txt"
            write_file = re.sub("\s+","",write_file)
            text = ""
            for html in newurls:
                content_obj = GetContent(html)
                t = content_obj.gettext()
                text += t
            if re.search("[\u0F00-\u0FFF]{20,}",text):
                with open(write_file,"w",encoding="utf8") as wf:
                    wf.write(text+"\n")
            print("<  The writed to ==  {0}  >".format(write_file))
        except IOError:
            Error.append(dl)
    shutil.rmtree(DIR1)
    print("The error file is ",Error)
    print("The error file is ",len(Error))
    print("The all finish!")
            
            
        #os.remove(path)

	
