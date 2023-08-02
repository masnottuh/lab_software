import dearpygui.dearpygui as dpg

dpg.create_context()
def change_state(sender, app_data, user_data):
    state = user_data
    state = not state
    print("button is ")
    print(state)

def print_value(sender, app_data):
    aaa = dpg.get_value(sender)
    print(aaa)
def run_function(sender):
    Accel_Get = dpg.get_value(accel)
    print(f"Acceleration is {Accel_Get}")
    Velo_Get = dpg.get_value(velo)
    print(f" Velocity is {Velo_Get}")
    SampleRate_Get = dpg.get_value(samplerate)
    print(f" Sample Rate is {SampleRate_Get}")
    Position_Get = dpg.get_value(position)
    print(f"Move to (absolute position) {Position_Get}")
with dpg.window(label="LST Settings", width=400, height=150, pos=(0,0)):
   
    button1 = dpg.add_button(label="home", callback=change_state)
    accel = dpg.add_input_float(label="acceleration", default_value =4, tag = "Accel")
    velo = dpg.add_input_float(label="velocity", default_value =10, )
    position = dpg.add_input_float(label="move to", default_value =10, )

with dpg.window(label="MYDAC", width=400, height=150, pos=(0,150)):
    samplerate = dpg.add_input_float(label="sample rate HZ", default_value =100, max_value=50, min_value=0)
with dpg.window(width=150, height=150,pos=(400,0)):
    RUN = dpg.add_button(label = "RUN", width=100, height=100, callback=run_function)

with dpg.theme() as item_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (200, 200, 100), category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 0, category=dpg.mvThemeCat_Core)
dpg.bind_item_theme(RUN, item_theme)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

