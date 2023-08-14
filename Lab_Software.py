#HOW TO RUN IN LAB
#To run this program on the MSI Laptop in Dr. Hanna's lab:
# 1. Open the Lab_Python.py file found in the folder Lab-Software(Program) inside of VSCode. 
# 2. The program's code will open and so should a gitbash terminal, if a gitbash terminal does not open:
#     Click Terminal>New Terminal and a Terminal will open.
#     Then click the down arrow next to the + , and select "Git Bash".
#     If you see a green "lapto@MSI" next to a purple "MINGW64" next to a yellow ~, then step 2 is done
# 3. Type "cd Desktop/Lab_Software" to enter the correct folder.
# 4. When ready to start the GUI, type py -m Lab_Software.py and enter, then wait.

#------------------------------------------------
#Python script to run lab instruments and form GUI
#Version 1.0
#for questions contact Gavin Fisher at GavinFisherProfessional@gmail.com
#                  or  Josh Rudfelt at __________@____.com
#                  or  Sam Hutton   at __________@____.com
#------------------------------------------------

#-------------------
#TO-DO:
#fix voltage ranges on nidaq
#handle computation for run time based on acc, vel
#finish gui
#-------------------

#this file uses the thorlabs_apt library hosted at https://github.com/qpit/thorlabs_apt/blob/master/thorlabs_apt/core.py
#               the nidaqmx library at https://github.com/ni/nidaqmx-python/tree/master
#               and dearpygui at https://github.com/hoffstadt/DearPyGui
#as well as pandas, matplotlib.pyplot, datetime, os, and cytypes.

import dearpygui.dearpygui as dpg
import thorlabs_apt as apt
import ctypes 
import nidaqmx
from nidaqmx.constants import TerminalConfiguration
import nidaqmx.system
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime
matplotlib.use('agg')

HWTYPE_LTS300 = 42 # LTS300/LTS150 Long Travel Integrated Driver/Stages

#motor configs gives device info in tuples
motor_configs = apt.list_available_devices()
motor = apt.Motor(motor_configs[0][1]) #establishes communication with LTS motor, sets class at motor.
MotorPos = motor.position


#code for realtime graphs
nsamples = 200
global data_y
global data_x
global data_z
# Can use collections if you only need the last 100 samples
data_y = collections.deque([0.0],maxlen=nsamples)
data_x = collections.deque([0.0],maxlen=nsamples)
data_z = collections.deque([0.0],maxlen=nsamples)




#dpg.show_debug()
# dpg.show_style_editor()

dpg.create_context()
def update_data():
    sample = 1
    while True:                   
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai2", min_val=0, max_val=10)
            task.ai_channels.add_ai_voltage_chan("Dev1/ai7", min_val=-1, max_val=10)
            task.timing.cfg_samp_clk_timing(10000)  #frequncy of sample rate


                    # Get new data sample. Note we need both x and y values
                    # if we want a meaningful axis unit
            INDUCTOR_Sensor_data = sensor_data[0]
            LVIT_Sensor_data = sensor_data[1]
            
            data_x.append(sample)
            data_y.append(LVIT_Sensor_data[0])
            data_z.append(INDUCTOR_Sensor_data[0])
                    
            dpg.set_value('series_tag', [list(data_x), list(data_y)])          
            dpg.fit_axis_data('x_axis')
            dpg.set_axis_limits('y_axis', ymin=-1, ymax=10)
                    # print(data_y)
                    #print(data_z)
            dpg.set_value('series_tag2', [list(data_x), list(data_z)])          
            dpg.fit_axis_data('x_axis2')
            dpg.fit_axis_data('z_axis')
                    
            sample=sample+1
                
            

#Initial GUI setup
=======
dpg.create_context() #needed to create the window

#Initial GUI setup
with dpg.theme() as item_theme1:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (235, 99, 144), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

with dpg.theme() as item_theme_RED:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (226, 61, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)
        #dpg.add_theme_style(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)

with dpg.theme() as item_theme_GREEN:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_Button, (61, 143, 56), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)

#FUNCTIONS
def popup_funct_home(sender):#Function to home the stage.
    dpg.configure_item("modal_id", show=False)
    motor.move_home() #HOMES MOTOR
    dpg.set_value("location", 0 )

def data_collection(numsamples, frequency):
    
    # with nidaqmx.Task(new_task_name='task') as task:
    
    task = nidaqmx.Task(new_task_name='task')
    print(list(task.ai_channels))
    task.ai_channels.add_ai_voltage_chan("Dev1/ai2", terminal_config=TerminalConfiguration(-1), min_val=0,max_val=10) ##initialize data acquisition task. Dev1 is the name of the DAQ, AV2 is the channel the induc is connected to.
    task.ai_channels.add_ai_voltage_chan("Dev1/ai7", terminal_config=TerminalConfiguration(-1))#For more info on TermConfig see: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019QRZSA2&l=en-US
    #      and https://www.ni.com/en-us/shop/data-acquisition/sensor-fundamentals/measuring-direct-current-dc-voltage.html
    print(list(task.ai_channels))
    task.timing.cfg_samp_clk_timing(frequency) #sets sample rate of code
    sensor_data = task.read(number_of_samples_per_channel=numsamples)
    task.close()
    return sensor_data

def png_output(sensor_data,pos):
    folder_path = "C:/Users/lapto/Desktop/Lab_Software/Data_Output/"
    os.makedirs(folder_path, exist_ok=True)                         #only makes a new folder if there isnt one named 'folder_path'
    posdf = pd.DataFrame(pos)
    df = pd.DataFrame(sensor_data)  
    df_induc = df.iloc[0]
    df_LVIT = df.iloc[1]                         

    plt.figure(1) #Plots and saves the induc graph
    plt.xlabel('# of samples'), plt.ylabel('Induction Sensor Voltage'), plt.ylim(0,10)
    plt.plot(df_induc, c = 'b')  #This section creates the Png of the induction sensor graph. c is the color, s is the size of the points
    png_name = datetime.now().strftime("%B_%d_Time_%I-%M-%S")    #Create the file name. Spaces, word without quotes seem to work, see 'time'.
    file_name = f'Induc_{png_name}.png' 
    file_path = os.path.join(folder_path,file_name)
    plt.savefig(file_path, dpi=1000)

    print(df_LVIT)
    plt.figure(2) #plots and saves LVIT graph
    plt.xlabel('# of samples'), plt.ylabel('LVIT Volts'), plt.ylim(0,10)
    plt.plot(df_LVIT, c = 'b')  
    file_name = f'LVIT_{png_name}.png' 
    file_path = os.path.join(folder_path,file_name)
    plt.savefig(file_path, dpi=1000)

    plt.figure(3) #plots and saves position graph
    plt.xlabel('# of samples'), plt.ylabel('Position in (units?)')
    plt.plot(posdf, c = 'b')
    file_name = f'Position_{png_name}.png' 
    file_path = os.path.join(folder_path,file_name)
    plt.savefig(file_path, dpi=1000)

    plt.close()

def csv_output(sensor_data,pos):
    posdf = pd.DataFrame(pos)
    df = pd.DataFrame(sensor_data)
    df1 = df.transpose()
    #print(df1)
    df2 = pd.concat([df1,posdf], axis=1)
    #print(df2)
    names = ["Induction","LVIT","Position"]
    df2.columns = names
    
    folder_path = "C:/Users/lapto/Desktop/Lab_Software/Data_Output/"
    csv_name = datetime.now().strftime("%B_%d_Time_%I-%M-%S")    #Create the file name. Spaces, word without quotes seem to work, ex: 'time'.
    file_name = f'Csv_{csv_name}.csv' 
    file_path = os.path.join(folder_path,file_name)
    df2.to_csv(file_path)

def run_function(sender):  #pulls input parameters and assigns them variables when run button is clicked
    Accel_Get = dpg.get_value(accel)
    #print(f"Acceleration is {Accel_Get}")
    Velo_Get = dpg.get_value(velo)
    #print(f" Velocity is {Velo_Get}")
    SampleRate_Get = dpg.get_value(samplerate)
    #print(f" Sample Rate is {SampleRate_Get}")
    Position_Get = dpg.get_value(position)
    frequency = dpg.get_value(samplerate)
    #print(f"Move to (absolute position) {Position_Get}")


    MotorPos = motor.position
    dP = abs(MotorPos-Position_Get)
    Taccel = Velo_Get/Accel_Get
    dPaccel = (Velo_Get*Taccel)/2
    dTvelo = abs(dP-dPaccel)/Velo_Get
    dT = dTvelo + Taccel
    numsamples = int(dT * frequency +2)
    print(f"Time to run in Sec: {dT}")
    print(f"Number of samples: {numsamples}")

    
    motor.set_velocity_parameters(0,Accel_Get,Velo_Get)
    print(f"motor is in motion val: {motor.is_in_motion}")
    motor.move_to(Position_Get)
    
    pos = []
    try:
        while motor.is_in_motion:
            cur_pos = motor.position
            pos.append(cur_pos)
            # time.sleep(1/frequency)
    except: 
        raise Exception("motor gave non-moving status after move command")

    sensor_data = data_collection(numsamples, frequency)
    png_output(sensor_data,pos)
    csv_output(sensor_data,pos)
    dpg.set_value("location", Position_Get)

#GUI That references functions
with dpg.window(label="LST Settings", width=400, height=150, pos=(0,0)):
   
    Home = dpg.add_button(label="HOME STAGE")
    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="modal_id"):
        dpg.add_text("Do you want to home the stage? check if LVIT and stablizers are out of the way")
        YES_HOME = dpg.add_button(label="Yes, home the stage", callback=popup_funct_home)
        NO_HOME = dpg.add_button(label="Negative, do not home the stage", callback=lambda: dpg.configure_item("modal_id", show=False))


    accel = dpg.add_input_float(label="acceleration", default_value =1, tag = "Accel")
    velo = dpg.add_input_float(label="velocity", default_value =5, )
    position = dpg.add_input_float(label="move to (abs position)", default_value =15, )
    Location = dpg.add_input_float(label = "current position mm", default_value = MotorPos, tag = "location" )

with dpg.window(label="MYDAC", width=400, height=150, pos=(0,150)):
    samplerate = dpg.add_input_float(label="sample rate HZ", default_value =100, max_value=50, min_value=0)


with dpg.window(width=150, height=150,pos=(400,0)):
    RUN = dpg.add_button(label = "RUN", width=100, height=100, callback=run_function)


with dpg.window(label='LVIT', tag='win',width=800, height=600, pos=(00,200)):

    with dpg.plot(label='LVIT', height=-1, width=-1):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes, set to auto scale.
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label='x', tag='x_axis')
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label='y', tag='y_axis')

        # series belong to a y axis. Note the tag name is used in the update
        # function update_data
        dpg.add_line_series(x=list(data_x),y=list(data_y), 
                            label='LVIT', parent='y_axis', 
                            tag='series_tag')

with dpg.window(label='inductor', tag='win2',width=800, height=600, pos=(850,200)):

    with dpg.plot(label='INDUCTOR', height=-1, width=-1):
        # optionally create legend
        dpg.add_plot_legend()

        # REQUIRED: create x and y axes, set to auto scale.
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label='x', tag='x_axis2')
        z_axis = dpg.add_plot_axis(dpg.mvYAxis, label='z', tag='z_axis')

        # series belong to a y axis. Note the tag name is used in the update
        # function update_data
        dpg.add_line_series(x=list(data_x),y=list(data_z), 
                            label='INDUCTOR', parent='z_axis', 
                            tag='series_tag2')



dpg.bind_item_theme(RUN, item_theme1)
dpg.bind_item_theme(Home, item_theme_RED)
dpg.bind_item_theme(NO_HOME, item_theme_RED)
dpg.bind_item_theme(YES_HOME, item_theme_GREEN)

dpg.create_viewport(title='Cantilever Interface', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
thread = threading.Thread(target=update_data)
thread.start()
dpg.start_dearpygui()
dpg.destroy_context()

