import time
import subprocess
import select
import os

cwd = os.getcwd()
filename = "../resources/test.txt"

f = subprocess.Popen(['tail','-F', filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print(f)
# p = select.poll()
p = select.kqueue()
print(p)
# p.register(f.stdout)

# while True:
#     if p.poll(1):
#         print f.stdout.readline()
#     time.sleep(1)
