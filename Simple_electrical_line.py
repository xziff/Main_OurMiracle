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

def magnetic_susceptibility(alpha, betta, H):
    return ((alpha * betta)/((betta * H)**2 + 1))

class Simple_electrical_line:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    switch_time_Q1 = [[],[]]
    switch_time_Q2 = [[],[]]
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    position_switch_Q1 = True
    position_switch_Q2 = True
    help_var_switch_Q = False
    toff= 0
    ton = 0
    l = 50
    Rl = 1
    Ll = 2/100/math.pi
    Roff = 0
    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.image_model_data = create_image_for_model("Image/Electrical line/0.png")
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
        return ([0,0,0])

    def get_main_determinant(self, input_variable):
        Ll = self.Ll

        mu0 = 4*math.pi*10**-7
        R1 = 0.07
        R2 = 0.2
        d = 0.4
        Ra = 0.6
        Rn = 6
        Ln = 0
        w = 120
        alpha = 0.228
        betta = 0.04
        Rtt = Ra + Rn
        Rsr = (R1 + R2)/2
        M = (mu0 * d * w * math.log(R2/R1))/(2 * math.pi)
        L = (mu0 * d * w * w * math.log(R2/R1))/(2 * math.pi)
        m = d * w * (R2 - R1) / (2 * math.pi * Rsr)

        main_determinant = [[Ll, -Ll, 0],
                        [Ll, 2*Ll, 0],
                        [M+m*magnetic_susceptibility(alpha, betta, (input_variable[0]+ w * input_variable[2])/(2 * math.pi * Rsr)), 0, L+Ln+m*w*magnetic_susceptibility(alpha, betta, (input_variable[0]+ w * input_variable[2])/(2 * math.pi * Rsr))]
                            ]                             
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        Ra = 0.6
        Rn = 3
        Rtt = Ra + Rn
        own_matrix = [-input_variable[0]*(self.Rl+self.Roff)+input_variable[1]*(self.Rl+self.Roff),
                    -2*input_variable[1]*(self.Rl+self.Roff)-input_variable[0]*(self.Rl+self.Roff),
                    -Rtt*input_variable[2]

                    ]  
        return own_matrix
    
    def get_voltage_matrix(self, parameter):
        if (parameter == "Q1"):     
            voltage_matrix = [[-1, 0],
                            [0, -1],
                            [0, 0]
                            ]
        if (parameter == "Q2"):     
            voltage_matrix = [[1, 0],
                            [0, 1],
                            [0, 0]
                            ]

        return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q1"):
            current_matrix = [[-1,0,0],
                            [0,-1,0],
                            [1,1,0],
                            ] 
        if (parameter == "Q2"):
            current_matrix = [[1,0,0],
                            [0,1,0],
                            [-1,-1,0],
                            ]
        return current_matrix

    def get_additional_variable(self, input_variable, t):
        additional_variable = []
        return additional_variable

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        #index_switcth = 0
        #for i in range(len(self.switch_time_Q)):
        #    for j in self.switch_time_Q[i]:
        #        if (((t - j) >= 0) and ((t - j) < delta_time_swicth)):           
        #            delta_time_swicth = (t - j)
        #            index_switcth = i
        #if (index_switcth == 0):
        #    self.position_switch_Q = True
        #    self.help_var_switch_Q == False
        #    if (self.help_var_switch_Qon == True):
        #        self.ton = t
        #        self.help_var_switch_Qon = False
        #    self.Roff = 0
        #elif (index_switcth == 1):
        #    self.position_switch_Q = False
        #    self.help_var_switch_Qon = True
        #    if (self.help_var_switch_Q == False):
        #       self.toff = t
        #        self.help_var_switch_Q = True
        #print(self.position_switch_Q)

    def time_interrupt(self):
        list_time_interrupt = []
        for i in range(len(self.switch_time_Q1)):
            for j in self.switch_time_Q1[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    if (j == 0):
                        list_time_interrupt.append(j)
                    else:
                        list_time_interrupt.append(j + 0.01)
        return list_time_interrupt

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
            if (self.position_switch_Q1 == False):
                    return ("Q1:OFF_SWITCH")
            return ("Q1:ON_SWITCH")
        elif ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
            if (self.position_switch_Q2 == False):
                    return ("Q2:OFF_SWITCH")
            return ("Q2:ON_SWITCH")
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
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            return True

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        pass

    def set_parameter_in_model(self):
        pass


    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y