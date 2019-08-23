收集数据,CSV写入



class CpuinfoTest:

# CPU性能测试
	def __init__(self, count):
		self.counter = count
		self.data = [('testtime', 'cpuinfo')]
		
	def get_cpuinfo(self, packageName):
	# 监控cpu信息
		result = os.popen(f'adb shell dumpsys cpuinfo | findstr {packageName}')
		cpuinfo = result.readlines()[0].split('%')[0].strip() + '%'
		testtime = time.strftime('%H:%M:%S')
		self.data.append([testtime, cpuinfo])
		return self.data
		
	def test_monitor(self):
	# 计时器
		while self.counter > 0 :
			self.get_cpuinfo()
			self.counter = self.counter - 1
			time.sleep(2)
			
	def data_save(self):
	# 写入数据表
		with open('cpu_report.csv', 'w', newline='') as f:
		# newline去掉空行
			writer = csv.writer(f, dialect = 'excel')
			writer.writerows(self.data)
			
			
if __name__ == '__main__':
	CT = CpuinfoTest(10)
	CT.test_monitor()
	CT.get_cpuinfo()
	CT.data_save()