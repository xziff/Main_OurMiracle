import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

k_size = 6
state_menu = 0
def create_image_for_model(pass_obj):
    buff_image = ImageTk.PhotoImage(Image.open(pass_obj))
    width_image = buff_image.width()/k_size
    image = ImageTk.PhotoImage(Image.open(pass_obj).resize((int(width_image), int((width_image)*buff_image.height()/buff_image.width())), Image.ANTIALIAS))
    #imagesprite2 = canv.create_image(WIDTH/2,HEIGHT/2,image=image2)
    return image

n_fig = 1

class KZ_Bus:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    switch_time_Q = [[7],[0]]
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    position_switch_Q = True
    help_var_switch_Q = False
    help_var_switch_Qon = False
    toff= 0
    ton = 0
    R = 0.0001
    Roff = 0
    Lc = 0.0002
    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.image_model_data = create_image_for_model("Image/KZ_Bus.png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')

        self.width_input = len(self.get_first())
        self.width_matrix = len(self.get_main_determinant(self.get_first())[0])
        self.height_matrix = len(self.get_main_determinant(self.get_first()))
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, 0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[-self.Lc, self.Lc, 0],
                            [0, -self.Lc, self.Lc],
                            [0, 0, -self.Lc]
                            ]                             
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        if ((self.position_switch_Q == False) and ((t - self.toff) < 0.01)):
            self.Lc= 50000/0.01*(t - self.toff)
        if ((self.position_switch_Q == False) and ((t - self.toff) > 0.01)):
            self.Lc = 0  
        if ((self.position_switch_Q == True) and ((t - self.ton) < 0.01)):
            self.Lc= -0.05/0.01*(t - self.ton) + 0.05
        if ((self.position_switch_Q == True) and ((t - self.ton) > 0.01)):
            self.Lc = 0
        self.Roff = 0
        own_matrix = [input_variable[0]*(self.R+self.Roff) - input_variable[1]*(self.R+self.Roff),
                    input_variable[1]*(self.R+self.Roff) - input_variable[2]*(self.R+self.Roff),
                    input_variable[2]*(self.R+self.Roff)
                    ]  
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        ] 
            return current_matrix

    def get_additional_variable(self, input_variable, t):
        additional_variable = []
        return additional_variable

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (((t - j) >= 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_Q = True
            self.help_var_switch_Q == False
            if (self.help_var_switch_Qon == True):
                self.ton = t
                self.help_var_switch_Qon = False
            self.Roff = 0
        elif (index_switcth == 1):
            self.position_switch_Q = False
            self.help_var_switch_Qon = True
            if (self.help_var_switch_Q == False):
                self.toff = t
                self.help_var_switch_Q = True

    def time_interrupt(self):
        list_time_interrupt = []
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    if (j == 0):
                        list_time_interrupt.append(j)
                    else:
                        list_time_interrupt.append(j + 0.01)
        return list_time_interrupt

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if ((self.x > bus_x) and (self.y + self.image_height > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
            if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
            return ("Q:ON_SWITCH")
        else:
            return ("none")


    def set_state_click(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        pass
        
    def view_result(self, m_x, m_y):
        pass

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        pass

    def set_parameter_in_model(self):
        pass


    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y