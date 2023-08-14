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

<<<<<<< Updated upstream
samplerate=2   # Sample Rate in Hz
numsamples=10
=======
samplerate=500   # Sample Rate in Hz
numsamples=1000
>>>>>>> Stashed changes

mydac_collection((samplerate),(numsamples))

<<<<<<< Updated upstream
# sample_mode=AcquisitionType.CONTINUOUsS

=======
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
    task.ai_channels.add_ai_voltage_chan("Dev1/ai7")
    task.timing.cfg_samp_clk_timing(samplerate)

    sensor_data = task.read(number_of_samples_per_channel=numsamples)
print(sensor_data)
print(len(sensor_data))
print(sensor_data[0])
print(sensor_data[1])
>>>>>>> Stashed changes
