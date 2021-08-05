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
###
def ksi_dif(H):
    return 70

def get_wc(Xc, delta, S):
    mu0 = 4 * math.pi * (10 ** (-7))
    return math.sqrt(Xc*math.pi*delta*math.pi/(100*math.pi*2*mu0*2*S*1.5))

def get_wr(wc, delta, S, Pn, cosfi, Un, Ifn, Xc, Rc):
    mu0 = 4 * math.pi * (10 ** (-7))
    return ((math.sqrt((Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc)**2 + (Un*1000/math.sqrt(3)*math.sqrt(2))**2 + 2*Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc*Un*1000/math.sqrt(3)*math.sqrt(2)*math.sin(math.fabs(math.acos(cosfi)))))*(math.pi*delta*math.pi)/(100*math.pi*wc*Ifn*mu0*4*S))

def get_wZ(w1, UnZ, UnT):
    return (w1*UnZ/UnT/math.sqrt(3))
def get_R_Z_T_11(Pkz, UnZ, Sn):
    return (Pkz/1000*(UnZ*UnZ)/(Sn*Sn))
def get_Z_Z_T_11(Uk, UnZ, Sn):
    return (Uk/100*(UnZ**2)/Sn)

class Transformator_Z_T_11:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    switch_time_T = [[],[]]
    position_switch_T = True
    help_var_switch_T = False
    toff_T = 0
    switch_time_Z = [[],[]]
    position_switch_Z = True
    help_var_switch_Z = False
    toff_Z = 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    UnZ = 121
    UnT = 6.3
    Sn = 80
    Pkz = 300
    Pxx = 10
    Ukz = 11
    Ixx = 1
    L = 1
    ra = 0.4
    R_t = 0.1
    lm = 2*(L + ra)
    S = math.pi*R_t**2
    R1 = 0.0009612
    R2 = 0.355
    Ls1 = 0.000087
    Ls2 = 0.032
    w1 = 100*int(121/(math.sqrt(3)*6.3))
    w2 = 100
    Roff_T = 0
    Roff_Z = 0

    var_text = ["Номинальная мощность, МВА:",
    "Номинальное напряжение обмотки звезды, кВ:",
    "Номинальное напряжение обмотки треугольника, кВ:",
    "Активная мощность потерь короткого замыкания, кВт:",
    "Активная мощность потерь холостого хода, кВт:",
    "Напряжение короткого замыкания, %:",
    "Ток холостого хода, %:",
    "Моменты времени, при которых контакты выключателя на стороне Y замыкаются, с:",
    "Моменты времени, при которых контакты выключателя на стороне Y размыкаются, с:", 
    "Моменты времени, при которых контакты выключателя на стороне D замыкаются, с:",
    "Моменты времени, при которых контакты выключателя на стороне D размыкаются, с:" 
    ]
    
    example_Transformator_Z_T_11 = [[80, 121, 6.3, 310, 85, 11, 0.6],
    [80, 121, 15, 310, 85, 11, 0.6],
    [125, 121, 10.5, 400, 120, 10.5, 0.55],
    [200, 121, 15.75, 550, 170, 10.5, 0.5],
    [250, 121, 15.75, 640, 200, 10.5, 0.5],
    [400, 121, 20, 900, 320, 10.5, 0.45],
    [2.5, 110, 6.6, 22, 5.5, 10.5, 1.55],
    [2.5, 110, 11, 22, 5.5, 10.5, 1.55],
    [6.3, 115, 6.6, 44, 10, 10.5, 1],
    [6.3, 115, 11, 44, 10, 10.5, 1],
    [10, 115, 6.6, 58, 14, 10.5, 0.9],
    [10, 115, 11, 58, 14, 10.5, 0.9],
    [16, 115, 6.6, 85, 18, 10.5, 0.7],
    [16, 115, 11, 85, 18, 10.5, 0.7],
    [16, 115, 22, 85, 18, 10.5, 0.7],
    [16, 115, 34.5, 85, 18, 10.5, 0.7],
    [25, 115, 38.5, 120, 25, 10.5, 0.65],
    [40, 115, 38.5, 170, 34, 10.5, 0.55],
    [63, 115, 38.5, 245, 50, 10.5, 0.5],
    [80, 115, 38.5, 310, 58, 10.5, 0.45],
    [80, 242, 6.3, 315, 79, 11, 0.45],
    [80, 242, 10.5, 315, 79, 11, 0.45],
    [125, 242, 10.5, 380, 120, 11, 0.55],
    [200, 242, 15.75, 660, 130, 11, 0.4],
    [250, 242, 15.75, 600, 207, 11, 0.5],
    [400, 242, 15.75, 880, 330, 11, 0.4],
    [400, 242, 20, 880, 330, 11, 0.4],
    [630, 242, 15.75, 1200, 400, 12.5, 0.35],
    [630, 242, 20, 1200, 400, 12.5, 0.35],
    [630, 242, 24, 1200, 400, 12.5, 0.35],
    [1000, 242, 24, 2200, 480, 11.5, 0.4],
    [125, 347, 10.5, 380, 125, 11, 0.55],
    [200, 347, 15.75, 520, 180, 11, 0.5],
    [250, 347, 15.75, 605, 214, 11, 0.5],
    [400, 347, 20, 790, 300, 11.5, 0.45],
    [630, 347, 15.75, 1300, 345, 11.5, 0.35],
    [630, 347, 20, 1300, 345, 11.5, 0.35],
    [630, 347, 24, 1300, 345, 11.5, 0.35],
    [1000, 347, 24, 2200, 480, 11.5, 0.4],
    [1250, 347, 24, 2200, 715, 14.5, 0.55],
    [250, 525, 15.75, 590, 205, 13, 0.45],
    [250, 525, 20, 590, 205, 13, 0.45],
    [400, 525, 15.75, 790, 315, 13, 0.45],
    [400, 525, 20, 790, 315, 13, 0.45],
    [630, 525, 15.75, 1210, 420, 14, 0.4],
    [630, 525, 20, 1210, 420, 14, 0.4],
    [630, 525, 24, 1210, 420, 14, 0.4],
    [1000, 525, 24, 1800, 570, 14.5, 0.45],
    ]

    mass_entry = []
    mass_var = []

    def __init__(self, init_x, init_y, canv, root):
        print(self.example_Transformator_Z_T_11)
        self.canv = canv
        self.root = root
        self.string_list_expample = [
        "Пользовательский",
        "ТДЦ-80000/121/6,3",
        "ТДЦ-80000/121/15",
        "ТДЦ-1250000/121/10,5",
        "ТДЦ-200000/121/15,75",
        "ТДЦ-250000/121/15,75",
        "ТДЦ-400000/121/20",
        "ТМН-2500/110/6,6",
        "ТМН-2500/110/11",
        "ТМН-6300/115/6,6",
        "ТМН-6300/115/11",
        "ТДН-10000/115/6,6",
        "ТДН-10000/115/11",
        "ТДН-16000/115/6,6",
        "ТДН-16000/115/11",
        "ТДН-16000/115/22",
        "ТДН-16000/115/34,5",
        "ТДН-25000/115/38,5",
        "ТДН-40000/115/38,5",
        "ТДН-63000/115/38,5",
        "ТДН-80000/115/38,5",
        "ТД-80000/242/6,3",
        "ТД-80000/242/10,5",
        "ТДЦ-125000/242/10,5",
        "ТДЦ-200000/242/15,75",
        "ТДЦ-250000/242/15,75",
        "ТДЦ-400000/242/15,75",
        "ТДЦ-400000/242/20",
        "ТНЦ-630000/242/15,75",
        "ТНЦ-630000/242/20",
        "ТНЦ-630000/242/24",
        "ТНЦ-1000000/242/24",
        "ТДЦ-125000/347/10,5",
        "ТДЦ-200000/347/15,75",
        "ТДЦ-250000/347/10,5",
        "ТДЦ-400000/347/20",
        "ТНЦ-630000/347/15,75",
        "ТНЦ-630000/347/20",
        "ТНЦ-630000/347/24",
        "ТНЦ-1000000/347/24",
        "ТНЦ-1250000/347/24",
        "ТДЦ-250000/525/15,75",
        "ТДЦ-250000/525/20",
        "ТДЦ-400000/525/15,75",
        "ТДЦ-400000/525/20",
        "ТЦ-630000/525/15,75",
        "ТЦ-630000/525/20",
        "ТЦ-630000/525/24",
        "ТНЦ-1000000/525/24"
        ]
        self.list_example = ttk.Combobox(self.root, values = self.string_list_expample, state="readonly")
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/Transformator/" + str(self.position) + ".png")
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
        return ([0, 0, 0, 0, 0, 0])

    def get_main_determinant(self, input_variable):
        main_determinant = [[self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0, 0, 0, self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0],
                            [0, self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, 0, self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])],
                            [0, 0, self.Ls1 - self.w1*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), self.w1*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), 0, 0],
                            [self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0, -self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[2]+self.w2/self.lm*input_variable[3]), self.Ls2 - self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), 0],
                            [-self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[0]+self.w2/self.lm*input_variable[4]), self.Ls2 - self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])],
                            [0, -self.w2*self.w1*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5]), 0, 0, 0, -self.Ls2 + self.w2*self.w2*self.S/self.lm*ksi_dif(self.w1/self.lm*input_variable[1]+self.w2/self.lm*input_variable[5])]
                            ]

        return main_determinant
    
    def get_own_matrix(self, input_variable, t):
        if (self.position_switch_T == False):
            self.Roff_T = 10000000/0.1*(t - self.toff_T)
        if (self.position_switch_Z == False):
            self.Roff_Z = 1000000/0.1*(t - self.toff_Z)
        own_matrix = [-input_variable[0]*self.R1 + (input_variable[2] - input_variable[0])*self.Roff_T - (input_variable[0] - input_variable[1])*self.Roff_T,
                    -input_variable[1]*self.R1 + (input_variable[0] - input_variable[1])*self.Roff_T - (input_variable[1] - input_variable[2])*self.Roff_T,
                    -input_variable[2]*self.R1 + (input_variable[1] - input_variable[2])*self.Roff_T - (input_variable[2] - input_variable[0])*self.Roff_T,
                    input_variable[3]*self.R2 - input_variable[4]*self.R2 + (input_variable[3] - input_variable[4])*self.Roff_Z,
                    input_variable[4]*self.R2 - input_variable[5]*self.R2 + (input_variable[4] - input_variable[5])*self.Roff_Z,
                    input_variable[5]*self.R2 + input_variable[5]*self.Roff_Z
                    ] 

        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "T"):
            voltage_matrix = [[1, 0],
                        [0, 1],
                        [-1, -1], 
                        [0, 0], 
                        [0, 0],
                        [0, 0]
                        ] 
            return voltage_matrix

        if (parameter == "Z"):
            voltage_matrix = [[0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0],
                        [-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "T"):
            current_matrix = [[1, 0, -1, 0, 0, 0],
                        [-1, 1, 0, 0, 0, 0],
                        [0, -1, 1, 0, 0, 0]
                        ] 
            return current_matrix

        if (parameter == "Z"):
            current_matrix = [[0, 0, 0, 1, 0, 0],
                        [0, 0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 0, 1]
                        ] 
            return current_matrix

    def get_additional_variable(self, input_variable, t):
        additional_variable = []
        return additional_variable

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_T)):
            for j in self.switch_time_T[i]:
                if (((t - j) > 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_T = True
            self.help_var_switch_T = False
            self.Roff_T = 0
        elif (index_switcth == 1):
            self.position_switch_T = False
            if (self.help_var_switch_T == False):
                self.toff_T = t
                self.help_var_switch_T = True


        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_Z)):
            for j in self.switch_time_Z[i]:
                if (((t - j) > 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_Z = True
            self.help_var_switch_Z = False
            self.Roff_Z = 0
        elif (index_switcth == 1):
            self.position_switch_Z = False
            if (self.help_var_switch_Z == False):
                self.toff_Z = t
                self.help_var_switch_Z = True

    def time_interrupt(self):
        list_time_interrupt = []
        for i in range(len(self.switch_time_T)):
            for j in self.switch_time_T[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    list_time_interrupt.append(j + 0.1)
        for i in range(len(self.switch_time_Z)):
            for j in self.switch_time_Z[i]:
                if (i == 0):
                    list_time_interrupt.append(j)
                if (i == 1):
                    list_time_interrupt.append(j + 0.1)
        return list_time_interrupt


    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            elif ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            elif ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            elif ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                if (self.position_switch_T == False):
                    return ("T:OFF_SWITCH")
                return ("T:ON_SWITCH")
            elif ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                if (self.position_switch_Z == False):
                    return ("Z:OFF_SWITCH")
                return ("Z:ON_SWITCH")
            else:
                return ("none")

    def set_state_click(self, m_x, m_y):
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
            self.image_model_data = create_image_for_model("Image/Transformator/" + str(self.position) + ".png")
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
            self.switch_time_Z_on_string = ""
            for i in self.switch_time_Z[0]:
                self.switch_time_Z_on_string = self.switch_time_Z_on_string + str(i) + ", "
            self.switch_time_Z_off_string = ""
            for i in self.switch_time_Z[1]:
                self.switch_time_Z_off_string = self.switch_time_Z_off_string + str(i) + ", "
            self.switch_time_T_on_string = ""
            for i in self.switch_time_T[0]:
                self.switch_time_T_on_string = self.switch_time_T_on_string + str(i) + ", "
            self.switch_time_T_off_string = ""
            for i in self.switch_time_T[1]:
                self.switch_time_T_off_string = self.switch_time_T_off_string + str(i) + ", "
            current_var = [self.Sn,self.UnZ, self.UnT,self.Pkz,self.Pxx,self.Ukz,self.Ixx, self.switch_time_Z_on_string, self.switch_time_Z_off_string, self.switch_time_T_on_string, self.switch_time_T_off_string]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(current_var[i])))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)
            self.mass_canv_text.append(self.canv.create_text(WIDTH/2, (0+len(self.var_text))*25 + 25, text = "Выбор существующего трансформатора", fill = "black", font = ("GOST Type A", "16"), anchor="center"))
            self.list_example.place(x = WIDTH/2 - 50, y = (1+len(self.var_text))*25 + 25)


    def set_parameter_in_model(self):
        if (self.list_example.get() == "Пользовательский"):
            for i in range(len(self.mass_var)):
                if (i == 0):
                    self.Sn = float(self.mass_var[i].get())
                elif (i == 1):
                    self.UnZ = float(self.mass_var[i].get())
                elif (i == 2):
                    self.UnT = float(self.mass_var[i].get())
                elif (i == 3):
                    self.Pkz = float(self.mass_var[i].get())
                elif (i == 4):
                    self.Pxx = float(self.mass_var[i].get())
                elif (i == 5):
                    self.Ukz = float(self.mass_var[i].get())
                elif (i == 6):
                    self.Ixx = float(self.mass_var[i].get())
                elif (i == 7):
                    self.switch_time_Z = []
                    self.switch_time_Z.append([])
                    self.switch_time_Z.append([])
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_Z[0].append(float(j))  
                elif (i == 8):
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_Z[1].append(float(j)) 
                elif (i == 9):
                    self.switch_time_T = []
                    self.switch_time_T.append([])
                    self.switch_time_T.append([])
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_T[0].append(float(j))  
                elif (i == 10):
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_T[1].append(float(j)) 
        else:
            for i in range(len(self.string_list_expample)):
                if (self.string_list_expample[i] == self.list_example.get()):
                    current_index = i-1
            for i in range(len(self.mass_var)):
                if (i == 0):
                    self.Sn = self.example_Transformator_Z_T_11[current_index][i]
                elif (i == 1):
                    self.UnZ = self.example_Transformator_Z_T_11[current_index][i]
                elif (i == 2):
                    self.UnT = self.example_Transformator_Z_T_11[current_index][i]
                elif (i == 3):
                    self.Pkz = self.example_Transformator_Z_T_11[current_index][i]
                elif (i == 4):
                    self.Pxx = self.example_Transformator_Z_T_11[current_index][i]
                elif (i == 5):
                    self.Ukz = self.example_Transformator_Z_T_11[current_index][i]
                elif (i == 6):
                    self.Ixx = self.example_Transformator_Z_T_11[current_index][i]
                elif (i == 7):
                    self.switch_time_Z = []
                    self.switch_time_Z.append([])
                    self.switch_time_Z.append([])
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_Z[0].append(float(j))  
                elif (i == 8):
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_Z[1].append(float(j)) 
                elif (i == 9):
                    self.switch_time_T = []
                    self.switch_time_T.append([])
                    self.switch_time_T.append([])
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_T[0].append(float(j))  
                elif (i == 10):
                    for j in self.mass_var[i].get().split(", "):
                        if (j != ""):
                            self.switch_time_T[1].append(float(j)) 

        self.w1 = 100
        self.w2 = get_wZ(self.w1, self.UnZ, self.UnT)
        self.R2 = get_R_Z_T_11(self.Pkz, self.UnZ, self.Sn)/2
        self.R1 = get_R_Z_T_11(self.Pkz, self.UnZ, self.Sn)/2*3*self.UnT*self.UnT/self.UnZ/self.UnZ
        self.L2 = math.sqrt((get_Z_Z_T_11(self.Ukz, self.UnZ, self.Sn))**2 - (get_R_Z_T_11(self.Pkz, self.UnZ, self.Sn))**2)/2/100/math.pi
        self.L1 = math.sqrt((get_Z_Z_T_11(self.Ukz, self.UnZ, self.Sn))**2 - (get_R_Z_T_11(self.Pkz, self.UnZ, self.Sn))**2)/2*3*self.UnT*self.UnT/self.UnZ/self.UnZ/100/math.pi
 
        print(self.w2, self.w1, self.R2, self.R1, self.L2, self.L1)
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y