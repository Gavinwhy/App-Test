# coding=gbk
import os,re


class Get_Name:

    def get_p_a_name(self,path):
        # 命令从镜像到log.txt
        os.system(f'aapt dump badging {path}>log.txt')
        with open('log.txt', 'r', encoding='utf-8') as f:
            st = f.readlines()
            ss = str(st)
            # 正则表达式取出包名和类名
            pattern1 = "package: name='(.*?)' versionCode"
            pattern2 = "activity: name='(.*?)'  label"
            packname = re.findall(pattern=pattern1, string=ss)[0]
            activityname = re.findall(pattern=pattern2, string=ss)[0]
            return (packname, activityname)

if __name__ == '__main__':
    GN=Get_Name().get_p_a_name(r'd:\app\5742942.apk')
    print(GN)
