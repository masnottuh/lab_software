import pandas as pd
import nidaqmx as ni
import time

vals = 4 #int(input()) 
task = ni.task.Task(new_task_name='blue')

task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai0")
task.start()
df = pd.DataFrame(task.read(number_of_samples_per_channel=vals,timeout=10))
#time out is how long to wait for samples before returning error
df = df/100 #converting to amps

path = "C:\\Users\\lapto\\Desktop\\Gavin"
df.to_csv(path+'LOOK')


task.stop()
task.close()
