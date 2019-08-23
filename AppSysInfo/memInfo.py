import os,time,csv

from app_performance.get_name import Get_Name


class Mem_Tst:

    def __init__(self,count,path):
        self.count1=count
        self.count2=count
        self.count3=count
        name=Get_Name().get_p_a_name(path)
        self.pkname=name[0]
        self.acname=name[1]
        print(self.pkname)
        app=path.split('top50apk\\')[1].strip('.apk')
        self.app=app

    def get_mem(self,data):
        r=os.popen(f'adb shell dumpsys meminfo {self.pkname}')
        li=r.readlines()
        print(li)
        jin=li[14].split('    ')[-2].split('    ')[-1]
        java=li[16].split('    ')[-2].split('    ')[-1]
        tot=li[40].split('TOTAL   ')[1].split(' ')[0]
        print(li[14])
        print(li[16])
        print(li[40])
        print(jin,java,tot)
        testtime=time.strftime('%H:%M:%S')
        data.append([testtime,jin,java,tot])
        print(data)

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

    def get_data(self,do):
        jin = self.app + '_' + do + '_jin_info'
        java = self.app + '_' + do + '_java_info'
        tot = self.app + '_' + do + '_tot_info'
        return [['testtime',jin,tot,java]]

    def do_null_tst(self):
        self.get_start_app()
        do = 'null'
        data=self.get_data(do)
        while self.count1>0:
            self.get_mem(data)
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
            self.get_mem(data)
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
            self.get_mem(data)
            self.count3-=1
            time.sleep(5)
        self.get_stop_app()
        self.save_data(data)


    def save_data(self,data):
        with open(f"mem_info.csv",'a',newline='')as f:
            writer=csv.writer(f,dialect='excel')
            writer.writerows(data)

    def just_do_it(self):
        self.do_null_tst()
        self.do_usua_tst()
        self.do_monk_tst()

if __name__ == '__main__':
    path=r'D:\apps\top50apk\996.apk'
    MT=Mem_Tst(3,path)
    MT.just_do_it()
