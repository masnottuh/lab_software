#------------------------------------------------
#Python script to run lab instruments and form GUI
#Version 1.0
#for questions contact ____ at ____@____.com
#------------------------------------------------

#-------------------
#TO-DO:
#fix voltage ranges on nidaq
#handle computation for run time based on acc, vel
#finish gui
#-------------------

#this file uses the thorlabs_apt library hosted at https://github.com/qpit/thorlabs_apt/blob/master/thorlabs_apt/core.py

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





#dpg.show_debug()
# dpg.show_style_editor()

dpg.create_context()


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

def data_collection(numsamples, frequency):
    
    with nidaqmx.Task(new_task_name='task') as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai2", terminal_config=TerminalConfiguration(-1)) ##initialize data acquisition task. Dev1 is the name of the DAQ, AV2 is the channel the induc is connected to.
        task.ai_channels.add_ai_voltage_chan("Dev1/ai7", terminal_config=TerminalConfiguration(-1))#For more info on TermConfig see: https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z0000019QRZSA2&l=en-US
        #      and https://www.ni.com/en-us/shop/data-acquisition/sensor-fundamentals/measuring-direct-current-dc-voltage.html
        # task.timing.samp_clk_max_rate(samplerate)
        task.timing.cfg_samp_clk_timing(frequency) #sets sample rate of code
        # global sensor_data
        return task.read(number_of_samples_per_channel=numsamples)

def file_output(sensor_data):
    folder_path = "C:/Users/lapto/Desktop/Data_Output/"
    os.makedirs(folder_path, exist_ok=True)                         #only makes a new folder if there isnt one named 'folder_path'

    df = pd.DataFrame(sensor_data)  
    df_induc = df.iloc[0]
    df_LVIT = df.iloc[1]                           #csv for both sensors collected.
    #print(df)
    # print(df_induc)
    # print(df_LVIT)

    csv_name = datetime.now().strftime("%B_%d_Time_%I-%M-%S")    #Create the file name. Spaces, word without quotes seem to work, ex: 'time'.
    file_name = f'Csv_{csv_name}.csv' 
    file_path = os.path.join(folder_path,file_name)
    df.to_csv(file_path)

    plt.figure(1) #Plots and savesthe induc graph
    plt.xlabel('# of samples'), plt.ylabel('Induction Sensor Voltage') 
    plt.plot(df_induc, c = 'b')  #This section creates the Png of the induction sensor graph. c is the color, s is the size of the points
    png_name = datetime.now().strftime("%B_%d_Time_%I-%M-%S")    #Create the file name. Spaces, word without quotes seem to work, see 'time'.
    file_name = f'Induc_{png_name}.png' 
    file_path = os.path.join(folder_path,file_name)
    plt.savefig(file_path, dpi=1000)


    plt.figure(2) #plots and saves LVIT graph
    plt.xlabel('# of samples'), plt.ylabel('LVIT Volts')
    plt.plot(df_LVIT, c = 'b')  #This section creates the Png of the induction sensor graph. c is the color, s is the size of the points
    png_name = datetime.now().strftime("%B_%d_Time_%I-%M-%S")    
    file_name = f'LVIT_{png_name}.png' 
    file_path = os.path.join(folder_path,file_name)
    plt.savefig(file_path, dpi=1000)


#numsamples = 1000
#frequency = 200


def popup_funct_home(sender):#function to home stage
    dpg.configure_item("modal_id", show=False)
    motor.move_home() #HOMES MOTOR
    dpg.set_value("location", 0 )

def run_function(sender):  #pulls input parameters and assigns them variables when run button is clicked
    Accel_Get = dpg.get_value(accel)
    print(f"Acceleration is {Accel_Get}")
    Velo_Get = dpg.get_value(velo)
    print(f" Velocity is {Velo_Get}")
    SampleRate_Get = dpg.get_value(samplerate)
    print(f" Sample Rate is {SampleRate_Get}")
    Position_Get = dpg.get_value(position)
    frequency = dpg.get_value(samplerate)
    print(f"Move to (absolute position) {Position_Get}")


    MotorPos = motor.position
    dP = abs(MotorPos-Position_Get)
    Taccel = Velo_Get/Accel_Get
    dPaccel = (Velo_Get*Taccel)/2
    dTvelo = abs(dP-dPaccel)/Velo_Get
    dT = dTvelo + Taccel
    numsamples = dT * frequency +2
    print(dT)

    
    motor.set_velocity_parameters(0,Accel_Get,Velo_Get)
    motor.move_to(Position_Get)
    # data_collection((numsamples), (frequency))
    # print(data_collection((numsamples), (frequency)))
    sensor_data = data_collection((numsamples), (frequency))
    file_output(sensor_data)
    dpg.set_value("location", Position_Get )
   # while motor.is_in_motion:
        #
        # print(motor.position)



with dpg.window(label="LST Settings", width=400, height=150, pos=(0,0)):
   
    Home = dpg.add_button(label="HOME STAGE")
    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="modal_id"):
        dpg.add_text("Do you want to home the stage? check if LVIT and stablizers are out of the way")
        YES_HOME = dpg.add_button(label="Yes, home the stage", callback=popup_funct_home)
        NO_HOME = dpg.add_button(label="Negative, do not home the stage", callback=lambda: dpg.configure_item("modal_id", show=False))


    accel = dpg.add_input_float(label="acceleration", default_value =1, tag = "Accel")
    velo = dpg.add_input_float(label="velocity", default_value =5, )
    position = dpg.add_input_float(label="move to (abs position)", default_value =150, )
    Location = dpg.add_input_float(label = "current position mm", default_value = MotorPos, tag = "location" )

with dpg.window(label="MYDAC", width=400, height=150, pos=(0,150)):
    samplerate = dpg.add_input_float(label="sample rate HZ", default_value =100, max_value=50, min_value=0)


with dpg.window(width=150, height=150,pos=(400,0)):
    RUN = dpg.add_button(label = "RUN", width=100, height=100, callback=run_function)


dpg.bind_item_theme(RUN, item_theme1)
dpg.bind_item_theme(Home, item_theme_RED)
dpg.bind_item_theme(NO_HOME, item_theme_RED)
dpg.bind_item_theme(YES_HOME, item_theme_GREEN)

dpg.create_viewport(title='Cantilever Interface', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

