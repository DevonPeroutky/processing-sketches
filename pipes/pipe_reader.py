import os
import traceback
import time

FIFO = "/tmp/piperoni"

## This works
print(os.getcwd())
os.system("echo Hello from the other side!")

# try:
#     ## This does not
#     os.mkfifo(FIFO)
# except OSError as oe: 
#     if oe.errno != errno.EEXIST:
#         raise

print("Opening FIFO...")
try:
    with open(FIFO) as fifo:
        print("FIFO opened")
        print(fifo)
        while True:
            for line in fifo:
                print("PRICING")
                print(line)
except Exception as error:
    print(traceback.format_exc())
    # or
