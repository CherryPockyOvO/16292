import subprocess
#url = f"http://{ip}:5261"
url = "http://10.194.96.73:5261"
subprocess.run(['sudo','-u','elf',"/usr/bin/chromium-browser", "--start-fullscreen", url])

