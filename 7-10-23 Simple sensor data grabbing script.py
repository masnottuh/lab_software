import pandas as pd
import nidaqmx as ni
import time

vals = int(input())
task = ni.task.Task(new_task_name='blue')

task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai0")
task.start()
data = task.read(number_of_samples_per_channel=vals,timeout=10)
#time out is how long to wait for samples before returning error


task.stop()
task.close()
print(data)