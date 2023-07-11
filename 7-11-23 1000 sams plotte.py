import pandas as pd
import numpy as np
import nidaqmx as ni
import time
from matplotlib import pyplot as plt

#Number of samples to read
num_samples = 1000

#Initiate NI task from NI package
task = ni.task.Task(new_task_name='blue')

task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai0")
task.start()
data = task.read(number_of_samples_per_channel=num_samples,timeout=10)
#time out is how long to wait for samples before returning error

#matplotlib of samples v. voltage 
x = np.arange(1,1001,1)
print(type(data))
plt.plot(x,data)
plt.show()


task.stop()
task.close()