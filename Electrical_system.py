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

class Electrical_system:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    Lc = 0.2/(100*math.pi)
    Uc = 6386.3621*math.sqrt(3)*10
    fc = 50
    phic = -1*math.pi/6

    var_text = ["Действующее значение напряженя, кВ:",
    "Частота, Гц:",
    "Начальная фаза напряжения, градус:",
    "Индуктивное сопротивление сети, Ом:",
    ]

    mass_entry = []
    mass_var = []

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = [
        "Пользовательский",
        ])
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/Electrical System/" + str(self.position) + ".png")
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
        own_matrix = [self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t + 0 + self.phic) - self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t - 2*math.pi/3 + self.phic),
                    self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t - 2*math.pi/3 + self.phic) - self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t + 2*math.pi/3 + self.phic),
                    self.Uc*math.sqrt(2)*math.sin(2*math.pi*self.fc*t + 2*math.pi/3 + self.phic)
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

    def time_interrupt(self):
        return []

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
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
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/Electrical System/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')

        
    def view_result(self, m_x, m_y):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):               
            return True

    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            self.state_change_parameter = 1
            self.mass_entry = []
            self.mass_var = []
            current_var = [self.Uc/1000,self.fc, self.phic*180/math.pi,self.Lc*self.fc*2*math.pi]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(round(current_var[i], 3))))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)  

    def set_parameter_in_model(self):
        for i in range(len(self.mass_var)):
            if (i == 0):
                self.Uc = float(self.mass_var[i].get())*1000
            elif (i == 1):
                self.fc = float(self.mass_var[i].get())
            elif (i == 2):
                self.phic = float(self.mass_var[i].get())*math.pi/180
            elif (i == 3):
                self.Lc = float(self.mass_var[i].get())/self.fc/2/math.pi

    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y