import appium

import os
import re
import socket
import threading

import time
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction


class Appiumcloud:
	def __init__(self):
		pass

	# self.port = 5000
	# self.

	def get_device(self):
		port = 5000
		bport = 9000
		devices = output.strip().split('\n')

		dlist = []
		for i in range(1, len(devices)):
			udid = devices[i].split('\t')[0]

			port = self.get_port()
			bport = self.get_port()

			dlist.append(udid, port, bport)
		return dlist

	def get_port(self, port):

		s = socket.socket()
		while True:
			try:
				s.connect(('127.0.0.1', port))
				port += 1

			except:
				break

			return port

	def get_pack(self):
		os.system(f'aapt dump badging {path} >log.txt')

		with open('log.txt', 'r', encoding='utf-8') as f:
			pattern = "package: name='(.+?)' versionCode"
			results = re.finditer(pattern=pattern, string=f.readline())
			for i in results:
				packname = i.group(1)
			# return packname

			pattern2 = "launchable-activity: name='(.*)' label"
			string = f.readlines()
			# print(string)
			result1 = re.findall(pattern=pattern2, string=str(string))

			return (packname, result1[0])

	def get_version(self, udid):
		version = os.popen(f'adb -s {udid} shell getprop ro.build.version.release').read().strip()

		# os.system进程阻塞
		# version = os.system('adb shell getprop ro.build.version.release').strip()
		return version

	def app_test(self, udid, port, bport, version, packname):
		os.system('taskkill /F /IM node.exe')

		logfile = '/.logs/' + str(udid).replace(':', '_') + '.log'

		# 启动appium服务
		cmd = f'appium -p {port} -bp {bport} --log {logfile} --log-timestamp'
		os.system(f'start /b {cmd}')
		time.sleep(10)

		# 准备字典参数
		# desired_caps = {}
		# desired_caps['platformName'] = 'Android'
		# desired_caps['platformVersion'] = '7'
		# desired_caps['deviceName'] = 'Appiumcloud'
		# desired_caps['appPackage'] = 'com.knivlk.kvmlphb'
		# desired_caps['appActivity'] = 'com.kingkr.webapp.activity.MainActivity'
		# desired_caps['unicodeKeyboard'] = True
		# desired_caps['udid'] = '20a0c8420504'

		# wd = webdriver.Remote(f'http://127.0.0.1:{port}/wd/hub', desired_caps)
		time.sleep(10)

	# wd.find_


if __name__ == '__main__':
	ac = Appiumcloud()
	# path = r'.apk'
	#
	# devices = ac.get_device()

	# for i in range(len(devices)):
	#	udid = devices[i]

	desired_caps = {}
	desired_caps['platformName'] = 'Android'
	desired_caps['platformVersion'] = '7'
	desired_caps['deviceName'] = 'Appiumcloud'
	desired_caps['appPackage'] = 'com.blogspot.aeioulabs.barcode'
	desired_caps['appActivity'] = 'com.blogspot.aeioulabs.barcode.ui.list.CodeListActivity_'
	desired_caps['unicodeKeyboard'] = True
	desired_caps['noReset'] = True
	desired_caps['udid'] = '20a0c8420504'
	# print(desired_caps)
	
	os.system('taskkill /F /IM node.exe')
	# cmd = "appium -p 4723 -bp 4724"
	os.system("start /b appium -a 127.0.0.1 -p 4723 -bp 4724")
	time.sleep(8)
	driver = webdriver.Remote(f'http://127.0.0.1:4723/wd/hub', desired_caps)
	time.sleep(3)
	el1 = driver.find_element_by_id("com.blogspot.aeioulabs.barcode:id/code_list_floating_buttons__add_button")
	el1.click()
	# driver.implicitly_wait(1)
	el2 = driver.find_element_by_id("com.blogspot.aeioulabs.barcode:id/code_list_floating_buttons__add_edit_label")
	el2.click()
	
	el3 = driver.find_elements_by_android_uiautomator("text()")
	el3[0].click()
	#TouchAction(driver).tap([(500, 300)], 10).perform()
	# driver.tap([(500, 300)],1)
	# driver.implicitly_wait(1)

	el6 = driver.find_elements_by_class_name("android.widget.TextView")
	# el6 = driver.find_elements_by_xpath(
	#     "//*[@=resource-id='com.blogspot.aeioulabs.barcode:id/code_list_item__text' and @text='文字')]")
	el6[0].click()
	#TouchAction(driver).tap([(500, 300)],10).perform()
	# driver.tap([(500, 300)],1)

	el7 = driver.find_element_by_id("com.blogspot.aeioulabs.barcode:id/code_edit_simple__text1")
	el7.send_keys("项目友人帐")

	# el8 = driver.find_element_by_id("com.blogspot.aeioulabs.barcode:id/code_edit_simple__text1")
	# el8.send_keys("ABC")

	el9 = driver.find_element_by_accessibility_id("保存")
	el9.click()

# threading.Thread(target=ac.app_test, args=())


