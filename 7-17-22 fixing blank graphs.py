import nidaqmx
from nidaqmx.constants import TerminalConfiguration
import matplotlib.pyplot as plt
import pandas as pd
import os
import time
from datetime import datetime



task1 = nidaqmx.Task()
task1.ai_channels.add_ai_voltage_chan('Dev1/AI2', terminal_config = TerminalConfiguration(-1)) #initialize data acquisition task

numsampls = 5000
data = task1.read(number_of_samples_per_channel=numsampls, timeout=100) 
rangsamples = [range(0,numsampls,1)]

task1.close()

folder_path = "C:/Users/lapto/Desktop/Gavin/troubleshooting_data/"
os.makedirs(folder_path, exist_ok=True) #only makes a new folder if there isnt one named 'folder_path'

df_induc = pd.DataFrame(data) #csv for the induction sensor collected.
csv_induc_id = datetime.now().strftime("%B%d Time %I-%M-%S") #Create the file name. Spaces, word without quotes seem to work, see 'time'.
file_name = f'Csv_{csv_induc_id}.csv' 
file_path = os.path.join(folder_path,file_name)
df_induc.to_csv(file_path)



plt.scatter(rangsamples,data,c='b')  #This section creates the Png of the induction sensor graph.
plt.xlabel('# of samples')
plt.ylabel('voltage')  
png_induc_id = datetime.now().strftime("%B%d Time %I-%M-%S") #Create the file name. Spaces, word without quotes seem to work, see 'time'.
file_name = f'plot_{png_induc_id}.png' 
file_path = os.path.join(folder_path,file_name)
plt.savefig(file_path, dpi=1000)
plt.show()



#to-do:
# 1. figure out how sample rate is working, and make number of samples and timeout easy to use in general
# 2. add channel and plots for the LVIT
# 3. output all data as csv with reasonable filenames relating to the trial/experiment/date/etc
# 5. format plot to have thinner lines (scatter would be preferred if possible) 
# 6. format plots to have readable axis' and title, legends, etc
# 7. output both separate plots for LVIT and inductive sensor, and also a copy where we combine them on one plot
# 8. gavin decide if subplots are reasonable/look good
# 9. clean up / comment code
