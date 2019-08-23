import os,time,csv

from app_performance.get_name import Get_Name


class Cpu_Tst:

    def __init__(self,count,path):
        self.count1=count
        self.count2=count
        self.count3=count
        name=Get_Name().get_p_a_name(path)
        self.pkname=name[0]
        self.acname=name[1]
        print(self.pkname)
        self.data=[['testtime','']]
        app=path.split('top50apk\\')[1].strip('.apk')
        self.app=app

    def get_cpu(self):
        r=os.popen(f'adb shell dumpsys cpuinfo | findstr {self.pkname}')
        li=r.readlines()
        print(li)
        cpu=li[0].split('%')[0].strip()+'%'
        testtime=time.strftime('%H:%M:%S')
        self.data.append([testtime,cpu])
        print(self.data)

    def get_start_app(self):
        os.popen(f'adb shell am start -n {self.pkname}/{self.acname}')
        print('start')
        time.sleep(20)

    def get_stop_app(self):
        os.popen(f'adb shell pm clear {self.pkname}')
        print('stop')
        time.sleep(5)

    def do_monk_play(self):
        os.popen(f'adb shell monkey --throttle 200 -p {self.pkname} 100')
        time.sleep(20)

    def do_usua_play(self):
        pass


    def do_null_tst(self):
        self.get_start_app()
        do = 'null'
        name = self.app + '_' + do + '_cpu_info'
        self.data=[['testtime',name]]
        while self.count1>0:
            self.get_cpu()
            self.count1-=1
            time.sleep(5)
        self.get_stop_app()
        self.get_data()
        self.data=[['testtime','']]

    def do_usua_tst(self):
        self.get_start_app()
        do = 'usua'
        name = self.app + '_' + do + '_cpu_info'
        self.data = [['testtime',name]]
        while self.count2>0:
            self.do_usua_play()
            self.get_cpu()
            self.count2-=1
            time.sleep(5)
        self.get_stop_app()
        self.get_data()
        self.data = [['testtime','']]

    def do_monk_tst(self):
        self.get_start_app()
        do = 'monk'
        name = self.app + '_' + do + '_cpu_info'
        self.data = [['testtime',name]]
        while self.count3>0:
            self.do_monk_play()
            self.get_cpu()
            self.count3-=1
            time.sleep(5)
        self.get_stop_app()
        self.get_data()
        self.data = [['testtime','']]

    def get_data(self):
        with open(f"cpu_info.csv",'a',newline='')as f:
            writer=csv.writer(f,dialect='excel')
            writer.writerows(self.data)

    def just_do_it(self):
        self.do_null_tst()
        self.do_usua_tst()
        self.do_monk_tst()

if __name__ == '__main__':
    path=r'D:\apps\top50apk\996.apk'
    CT=Cpu_Tst(3,path)
    CT.just_do_it()
