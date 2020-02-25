import re
import shutil
import random

r_date = "Logging started at ([\w\-:\.]*)"
r_nick = "\) (.*) \*\*LOCAL\*\*"

r_adapter = "Detected Adapter '(.*)\n"
r_process = 'Parent process: (.*)\n'
r_locale = '-Locale=([^"]*)"'
r_rr3d = "rr3dRenderLayer::InitDevice\(([^\)]*)\)"
r_build = "Build Version: (.*)\n"
r_os = "CFG\| OS Version:(.*)\n"
fps_a = "FPS Average (.*)\n"
fps_m = "FPS Average Minimum (.*)\n"
fps_mx = "FPS Average Maximum (.*)\n"
fps_v = "FPS Variance (.*)\n"

groups = [
	r_adapter, r_process, r_locale,
	r_rr3d, r_build, r_os,
	fps_a, fps_m, fps_mx, fps_v
]

config = []
target = []
def find(regex, txt):
	return re.search(regex, txt, re.IGNORECASE).group(1)

def openLogs(player, configuration):
	with open(configuration, "r", encoding="UTF-8") as f:
		fc = f.read()

	for g in groups:
		config.append(find(g, fc))

	with open(player, "r", encoding="UTF-8") as f:
		fc = f.read()

	for g in groups:
		target.append(find(g, fc))

	for i in range(4):
		val = float(config[-(i+1)][2:])
		delta_max = val*0.03
		delta_min = -val*0.03
		delta = random.uniform(delta_min, delta_max)
		val += delta
		config[-(i+1)] = f'= {val:.6f}'


	nick = find(r_nick, fc)
	date = find(r_date, fc)
	print("[*] "+date+" - "+nick)
	print("[*] Zmiana danych z: ")

	for i, after in enumerate(config):
		before = target[i]
		print(before + " ----> " + after) 
		fc = fc.replace(before, after)

	with open('output.txt', 'w', encoding="UTF-8") as f:
		f.write(fc)

openLogs('logs to be changed.txt', 'logs w/ configuration to use.txt')