import re
import threading
import uiautomator2 as u2
import os
import time

# os.system('python -m uiautomator2 init')


class u2cloud:


	def get_devices(self):
		lists = (os.popen('adb devices').read())
		# print(lists)
		devices = lists.strip().split('\n')
		# print(devices)

		dlist = []
		for i in range(1, len(devices)):
			udid = devices[i].split('\t')[0]
			dlist.append(udid)
		return dlist

	def get_pack(self, path):
		results = os.system(f'aapt dump badging {path} >log.txt')
		with open('log.txt', 'r', encoding='utf-8') as f:
			# print(f.readline())   # 不能打印
			# 正则表达式提取包名
			pattern = "package: name='(.+?)' versionCode"
			results = re.finditer(pattern=pattern, string=f.readline())
			for result in results:
				# print(result.group(1))  # 0全部,1匹配值
				packname = result.group(1)
				return packname

	def app_test(self, udid, path, packname):
		# 连接设备
		self.d = u2.connect(udid)
		# 安装
		os.system(f'adb -s {udid} install -r {path}')
		time.sleep(2)
		self.d.app_start(pkg_name=packname)
		# 操作核心模块
		d(text=u"我").click()
		d(text=u"登录/注册").click()
		d(text=u"账号密码登录").click()
		d(resourceId="account").click()
		d(resourceId="account").set_text("17629074323")
		d(resourceId="password").click()
		d(resourceId="password").set_text("123456")
		d(resourceId="btn").click()
		d(resourceId="plus").click()
		d(resourceId="2m").click()
		d(text=u"立即借款").click()
		d(text=u"确认借款").click()

		# 卸载
		os.system('adb -s {udid} uninstall {packname}')


if __name__ == '__main__':
	uc = u2cloud()

	devices = uc.get_devices()
	print(devices)

	# packname = 'com.knivlk.kvmlphb'
	# avtivityname = '.com.kingkr.webapp.activity.MainActivity'

	apkpath = r"H:\xindai.apk"
	packname = uc.get_pack(apkpath)
	print(packname)

	# 多线程
	# threading.Thread(target=uc.app_test, args=(device, path, packname)).start()
