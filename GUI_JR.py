import dearpygui.dearpygui as dpg


HOME_STAGE = 0

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

def popup_funct_home(sender):#function to home stage, after homing HOME_STAGE remains =1 **bug?**
    dpg.configure_item("modal_id", show=False)
    global HOME_STAGE
    HOME_STAGE = 1

def change_state(sender, app_data, user_data):
    state = user_data
    state = not state
    print("button is ")
    print(state)

def print_value(sender, app_data):
    print(sender)


def run_function(sender):  #pulls input parameters and assigns them variables when run button is clicked
    Accel_Get = dpg.get_value(accel)
    print(f"Acceleration is {Accel_Get}")
    Velo_Get = dpg.get_value(velo)
    print(f" Velocity is {Velo_Get}")
    SampleRate_Get = dpg.get_value(samplerate)
    print(f" Sample Rate is {SampleRate_Get}")
    Position_Get = dpg.get_value(position)
    print(f"Move to (absolute position) {Position_Get}")

with dpg.window(label="LST Settings", width=400, height=150, pos=(0,0)):
   
    Home = dpg.add_button(label="HOME STAGE", callback=change_state)
    with dpg.popup(dpg.last_item(), mousebutton=dpg.mvMouseButton_Left, modal=True, tag="modal_id"):
        dpg.add_text("Do you want to home the stage? check if LVIT and stablizers are out of the way")
        YES_HOME = dpg.add_button(label="Yes, home the stage", callback=popup_funct_home)
        NO_HOME = dpg.add_button(label="Negative, do not home the stage", callback=lambda: dpg.configure_item("modal_id", show=False))

    accel = dpg.add_input_float(label="acceleration", default_value =4, tag = "Accel")
    velo = dpg.add_input_float(label="velocity", default_value =10, )
    position = dpg.add_input_float(label="move to", default_value =10, )

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

print(HOME_STAGE)