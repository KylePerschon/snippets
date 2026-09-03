# %%
import serial
import time
from datetime import datetime


output = []
limit_output_capture = 5000

def read_arduino(comport, baudrate, timestamp=False, timeout=0.1):
    with serial.Serial(comport, baudrate, timeout=timeout) as ser_conn:
        while len(output) < limit_output_capture:
            try:
                data = ser_conn.readline().decode().strip()
            except:
                data = None
            else:
                if data is None or data == '':
                    continue
                if 'failed to send' in data:
                    print(f'{datetime.now()}:{data}')
                data = f'{datetime.now()}:{data}'
                output.append(data)
read_arduino('com3', '9600')
failed_to_send_list = []
for l in output:
    if 'failed to send' in l:
        print(l)
        failed_to_send_list.append(l)
# %%
