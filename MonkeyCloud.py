#基于云测试平台的Monkey测试
#设备列表+测试脚本+日志错误
class MonkeyCloud:

	def build_device(self):
	# 通过list对象构建设备列表
		dlist = []
		devices = subprocess.check_output('adb devices').decode().strip().split('\r\n')
		for i in range(1, len(devices)):
			udid = devices[i].split('\t')[0]
			if udid != '':
				dlist.append(udid)
		return dlist
		
	def star_monkey(self, udid, package, count):
	# 调用monkey命令进行测试
		cmd = f'adb -s {udid} shell monkey -p {package} {count}'
		monkey_log = subprocess.check_output(cmd)
		log_file = os.path.abspath('.') + '\\report\\monkey_' + udid.replace(':', '.') + '.log'
		# 将日志信息写入文件
		report = open(log_file, mode='w', encoding='utf8')
		monkey_list = srt(monkey_log).split('\\r\\r\\r')
		# 将日志按照 \r\r\n 拆分成列表,按行写入文件
		for line in monkey_list;
			report.writelines(line + '\r\n')
		report.close()
		time.sleep(5)
		os.system(f'adb -s {udid} shell am force-stop {package}')
		# 关闭应用程序并打印结果
		self.print_result(udid)
		
	def print_result(self, udid):
		log_path = os.path.abspath('.') + '\\report\\monkey_' + udid.replace(':', '.') + '.log'
		log_file = open(log_path, mode='r', encoding='utf8')
		# 读取日志
		content = log_file.read()
		if 'crash' in content or 'Crash' in content:
		# 异常情况判断
			print(f'设备 {udid}: 出现Crashed异常 - Failed')
			print(f'设备 {udid}: 未出现Crashed异常 - Passed')
		if 'ANR' in content:
			print(f'设备 {udid}: 出现ANR异常 - Failed')
			print(f'设备 {udid}: 未出现ANR异常 - Passed')
		log_file.close()
		
		
if __name__ == '__main__':
	threads = []
	for udid in devices:
		threads.append(threading.Thread(target=mc.start_monkey, args=(udid, package, count)))
	for t in threads:
		t.setDaemon(True)
		t.start()
	t.join()