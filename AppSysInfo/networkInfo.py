#coding=gbk
#流量测试
import os,time,csv

from app_performance.get_name import Get_Name


class Tra_Tst:

    def __init__(self,count,path):
        self.count1=count
        self.count2=count
        self.count3=count
        #获取包名、类名
        name=Get_Name().get_p_a_name(path)
        self.pkname=name[0]
        self.acname=name[1]
        print(self.pkname)
        app=path.split('top50apk\\')[1].strip('.apk')
        self.app=app

    def get_tra(self,data):
        #获取pid
        r=os.popen(f'adb shell ps |findstr {self.pkname}')
        pid = r.readlines()[0].split('  ')[2]
        #获取uid
        r1 = os.popen(f"adb shell cat proc/{pid}/status")
        uid = r1.readlines()[12].split('\t')[1]
        #获取下行流量，夜神Andriod5以下版本才可进行
        r2 = os.popen(f"adb shell cat /proc/uid_stat/{uid}/tcp_rcv ")
        tcp_rcv = r2.readlines()[0].strip()
        #获取上行流量，夜神Andriod5以下版本才可进行
        re3 = os.popen(f"adb shell cat /proc/uid_stat/{uid}/tcp_snd")
        tcp_snd = re3.readlines()[0].strip()
        testtime=time.strftime('%H:%M:%S')
        data.append([testtime,tcp_rcv,tcp_snd])
        print(data)

    def get_start_app(self):
        #打开APP
        os.popen(f'adb shell am start -n {self.pkname}/{self.acname}')
        print('start')
        time.sleep(20)

    def get_stop_app(self):
        #关闭APP
        os.popen(f'adb shell pm clear {self.pkname}')
        print('stop')
        time.sleep(5)

    def do_monk_play(self):
        #猴子操作
        os.popen(f'adb shell monkey --throttle 200 -p {self.pkname} 100')
        time.sleep(20)

    def do_usua_play(self):
        #常规操作
        pass

    def get_data(self,do):
        rcv = self.app + '_' + do + '_rcv_info'
        snd = self.app + '_' + do + '_snd_info'
        return [['testtime',rcv,snd]]

    def do_null_tst(self):
        self.get_start_app()
        do = 'null'
        data=self.get_data(do)
        #通过传入参数控制监控次数
        while self.count1>0:
            self.get_tra(data)
            self.count1-=1
            time.sleep(5)
        self.get_stop_app()
        self.save_data(data)

    def do_usua_tst(self):
        self.get_start_app()
        do = 'usua'
        data = self.get_data(do)
        while self.count2>0:
            self.do_usua_play()
            self.get_tra(data)
            self.count2-=1
            time.sleep(5)
        self.get_stop_app()
        self.save_data(data)

    def do_monk_tst(self):
        self.get_start_app()
        do = 'monk'
        data = self.get_data(do)
        while self.count3>0:
            self.do_monk_play()
            self.get_tra(data)
            self.count3-=1
            time.sleep(5)
        self.get_stop_app()
        self.save_data(data)


    def save_data(self,data):
        #记录数据存入csv文件
        with open(f"mem_info.csv",'a',newline='')as f:
            writer=csv.writer(f,dialect='excel')
            writer.writerows(data)

    def just_do_it(self):
        self.do_null_tst()
        self.do_usua_tst()
        self.do_monk_tst()

if __name__ == '__main__':
    path=r'D:\apps\top50apk\996.apk'
    TT=Tra_Tst(3,path)
    TT.just_do_it()
