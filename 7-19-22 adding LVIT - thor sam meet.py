import nidaqmx
from nidaqmx.constants import TerminalConfiguration
import nidaqmx.system
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime

induc_task = nidaqmx.Task(new_task_name='induc_sensor')
induc_task.ai_channels.add_ai_voltage_chan('Dev1/AI2', terminal_config = TerminalConfiguration(-1)) #initialize data acquisition task. Dev1 is the name of the DAQ, AV2 is the channel the induc is connected to.
lvit_task = nidaqmx.Task(new_task_name='lvit') #For more info on TermConfig see: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019QRZSA2&l=en-US
lvit_task.ai_channels.add_ai_voltage_chan('Dev1/AI7',terminal_config=TerminalConfiguration(-1)) # and https://www.ni.com/en-us/shop/data-acquisition/sensor-fundamentals/measuring-direct-current-dc-voltage.html

numsampls = 5000 # number if sampls for it to collect
rangsamples = [range(0,numsampls,1)] #list to accompany data in graphs


lvit_data = lvit_task.read(number_of_samples_per_channel=numsampls)
induc_data = induc_task.read(number_of_samples_per_channel=numsampls)
lvit_task.close()
induc_task.close()



folder_path = "C:/Users/lapto/Desktop/Gavin/troubleshooting_data/"
os.makedirs(folder_path, exist_ok=True)                         #only makes a new folder if there isnt one named 'folder_path'

df = pd.DataFrame(induc_data,lvit_data)                             #csv for both sensors collected.
csv_induc_id = datetime.now().strftime("%B%d Time %I-%M-%S")    #Create the file name. Spaces, word without quotes seem to work, ex: 'time'.
file_name = f'Csv_{csv_induc_id}.csv' 
file_path = os.path.join(folder_path,file_name)
df.to_csv(file_path)




plt.figure(1) #both graphs are on one subplot
plt.subplot(211), plt.xlabel('# of samples'), plt.ylabel('Induction sensor voltage') 
plt.scatter(rangsamples, induc_data, s =5, c = 'b')  #This section creates the Png of the induction sensor graph. c is the color, s is the size of the points
plt.subplot(212), plt.xlabel('# of samples'), plt.ylabel('LVIT voltage')  
plt.scatter(rangsamples, lvit_data, s = 5, c ='r') #png of LVIT volts
                      
png_induc_id = datetime.now().strftime("%B%d Time %I-%M-%S")    #Create the file name. Spaces, word without quotes seem to work, see 'time'.
file_name = f'plot_{png_induc_id}.png' 
file_path = os.path.join(folder_path,file_name)
plt.savefig(file_path, dpi=1000)
plt.show() #this shows the plot you made prior to saving it.
# print('You must close the plot before running new tests or examining the data.')
print('done')

#to-do:
# 1. figure out how sample rate is working, and make number of samples and timeout easy to use in general
# 7. output both separate plots for LVIT and inductive sensor, and also a copy where we combine them on one plot
# 8. gavin decide if subplots are reasonable/look good
# 9. clean up / comment code
