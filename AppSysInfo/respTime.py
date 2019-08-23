import csv
import os
import time

from app_performance.get_name import Get_Name


class Resp_Time:

    def __init__(self,count,path,app):
        self.count1=count
        self.count2=count
        self.data = [["test_time", ""]]
        name=Get_Name().get_p_a_name(path)
        self.pkname=name[0]
        self.acname=name[1]
        self.app=app+'_start_time'

    def get_start(self):
        r=os.popen(f'adb shell am start -W {self.pkname}/{self.acname}')
        st_time=r.readlines()
        print(st_time)
        st=st_time[8].split('\n')[0].split(':')[1].strip()
        testtime=time.strftime("%H:%M:%S")
        self.data.append([testtime,st])
        print(self.data)

    def get_quit(self):
        os.popen(f"adb shell pm clear {self.pkname}")
        time.sleep(3)

    def get_home(self):
        os.popen("adb shell input keyevent 3")
        time.sleep(3)

    def do_cold_tst(self):
        while self.count1>0:
            self.get_start()
            time.sleep(10)
            self.get_quit()
            self.count1-=1
            time.sleep(5)
        name="cold_start_time"
        self.get_data(name)
        self.data = [["test_time", ""]]

    def do_hot_tst(self):
        os.popen(f'adb shell am start -n {self.pkname}/{self.acname}')
        time.sleep(10)
        self.get_home()
        while self.count2>0:
            data=self.get_start()
            time.sleep(5)
            self.count2 -= 1
            if self.count2>0:
                self.get_home()
            else:
                self.get_quit()
            time.sleep(5)
        name="hot_start_time"
        self.get_data(name)
        self.data = [["test_time", ""]]

    def get_data(self,name):
        self.data[0][1]=self.app
        print(self.data)
        with open(f"{name}.csv",'a',newline='')as f:
            writer=csv.writer(f,dialect='excel')
            writer.writerows(self.data)

if __name__ == '__main__':
    pp=[r'D:\apps\top50apk\996.apk',r'D:\apps\top50apk\xiaoxiaole.apk',r'D:\apps\top50apk\2048.apk']
    for path in pp:
        app=path.split('top50apk\\')[1].strip('.apk')
        print(app)
        RT=Resp_Time(10,path,app)
        RT.do_cold_tst()
        RT.do_hot_tst()