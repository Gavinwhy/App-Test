import os
import re
import threading
import time


class Monkey_top50:

    def do_install(self,path):
        os.system(f"adb install -r {path}")


    def do_uninatall(self,pkname):
        os.system(f"adb uninstall {pkname}")


    def get_path(self):
        li=os.listdir(r'd:\apps\top50apk')
        path=[]
        for i in li:
            p='d:\\apps\\top50apk\\'+i
            path.append(p)
        print(path)
        return path

    def get_pkname(self):
        p=self.get_path()
        pkname=[]
        for path in p:
            os.system(f'aapt dump badging {path}>log.txt')
            with open('log.txt','rb') as f:
                li1=str(f.readline())
                pattern="package: name='(.*?)' versionCode"
                r=re.findall(pattern=pattern,string=li1)[0]
                pkname.append(r)
        return pkname

    def do_mktst(self):
        path=self.get_path()
        pkname = self.get_pkname()
        for i in range(len(path)):
            self.do_install(path[i])
            time.sleep(30)
            os.system(f"adb shell monkey --throttle 500 -v-v -p {pkname[i]} 100>./log/mk_{pkname[i]}.log")
            time.sleep(5)
            self.do_uninatall(pkname[i])

    def do_judge(self):
        path = self.get_path()
        pkname = self.get_pkname()
        for i in range(len(path)):
            with open(f"./log/mk_{pkname[i]}.log",'r') as f:
                li=f.readlines()
                x=str(li)
                if ('crash' in x) or ('anr' in x):
                    print('fail')
                else:
                    print('pass')

if __name__ == '__main__':
    MK=Monkey_top50()
    MK.do_mktst()


