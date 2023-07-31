import nidaqmx
import matplotlib.pyplot as plt
from nidaqmx.constants import AcquisitionType


# Sample Settings

samplerate=20   # Sample Rate in Hz
numsamples=200

# sample_mode=AcquisitionType.CONTINUOUS

with nidaqmx.Task() as task:
 #   task.ai_channels.add_ai_voltage_chan("Dev1/ai2")
    task.ai_channels.add_ai_voltage_chan("Dev1/ai7")
    task.timing.cfg_samp_clk_timing(samplerate)

    sensor_data = task.read(number_of_samples_per_channel=numsamples)
task.close()
print(sensor_data)
