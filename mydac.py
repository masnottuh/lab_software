import nidaqmx
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType

def mydac_collection(samplerate, numsamples):
    with nidaqmx.Task() as task:
 #   task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
     task.ai_channels.add_ai_voltage_chan("Dev1/ai7")
     task.timing.cfg_samp_clk_timing(samplerate)

     sensor_data = task.read(number_of_samples_per_channel=numsamples)
     task.close()  
     print(sensor_data)  
# Sample Settings

samplerate=2   # Sample Rate in Hz
numsamples=10

mydac_collection((samplerate),(numsamples))

# sample_mode=AcquisitionType.CONTINUOUsS

