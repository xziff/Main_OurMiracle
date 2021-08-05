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

def B_delta(Ica, Icb, Icc, Ira, Irb, Irc, x, phi, mu0, delta, wc, wr, tau, p):
    return (2*mu0/(math.pi*delta)*(wc*Ica*math.cos(math.pi/tau*x)+wc*Icb*math.cos(math.pi/tau*x-2*math.pi/3)+wc*Icc*math.cos(math.pi/tau*x+2*math.pi/3)+wr*Ira*math.cos(math.pi/tau*x-phi*p)+wr*Irb*math.cos(math.pi/tau*x-phi*p-2*math.pi/3)+wr*Irc*math.cos(math.pi/tau*x-phi*p+2*math.pi/3)))

def moment_pd(t, t0, t2, M_max):
    t1 = t0 + t2
    if ((t >= t0) and (t <= t1)):
        return ((M_max)/(t1-t0)*t - (M_max)/(t1-t0)*t0)
    if (t < t0):
        return 0
    if (t > t1):
        return M_max

class AMY:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    switch_time_Q = [[],[]]
    position_switch_Q = True
    help_var_switch_Q = False
    toff= 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    
    M = 19200*1
    p = 3
    tau = math.pi*0.795/2/p
    l = 0.57
    wc = 108
    wr = 27
    mu0 = 4 * math.pi * (10 ** (-7))
    delta = 0.0018
    Rc = 0.101
    Rr = 0.0073
    Roff = 0
    Lcs = 0.003638
    Lrs = 0.0001836
    J = 200
    D = 2*p*tau/math.pi

    var_text = [
    "Число пар полюсов, шт:",
    "Момент инерции ротора, кг*м2:",
    "Активное сопротивление обмотки статора, Ом:",
    "Активное сопротивление обмотки ротора, Ом:",
    "Индуктивность поля рассеяния обмотки статора, Гн:",
    "Индуктивность поля рассеяния обмотки ротора, Гн:",
    "Длина машины, м:",
    "Полюсное деление машины, м:",
    "Длина воздушного зазора, м:",
    "Число витков обмотки статора, шт:",
    "Число витков обмотки ротора, шт:",
    "Механический момерн нагрузки, Н*м:",
    "Моменты времени, при которых контакты выключателя замыкаются, с:",
    "Моменты времени, при которых контакты выключателя размыкаются, с:"  
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
        self.image_model_data = create_image_for_model("Image/AM/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, 0, 0, 0, 0, 0])

    def get_main_determinant(self, input_variable):
        #main_determinant =                   
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        if (self.position_switch_Q == False):
            self.Roff = 50000/0.01*(t - self.toff)
        if (0.4 < (1-self.p*input_variable[6]/(2*50*math.pi))):
            self.Rr = 10*0.0073
        if (0.4 >= (1-self.p*input_variable[6]/(2*50*math.pi))):
            self.Rr = 1*0.0073
        #self.Rr = 10*0.0073
        #own_matrix = 
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0, 0],
                        [0, -1, 0],
                        [0, 0, -1],
                        [0, 0, 0],
                        [0, 0, 0],
                        [0, 0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[1, 0, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0, 0],
                        [0, 0, 1, 0, 0, 0]
                        ] 
            return current_matrix

    def get_derw(self, input_variable, t):
        Melmag = self.p*self.D*self.l*self.wr*(input_variable[3]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/math.pi*input_variable[7]*self.p-self.tau/2, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[4]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/math.pi*input_variable[7]*self.p+self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p)+input_variable[5]*B_delta(input_variable[0], input_variable[1], input_variable[2], input_variable[3], input_variable[4], input_variable[5], self.tau/math.pi*input_variable[7]*self.p-7*self.tau/6, input_variable[7], self.mu0, self.delta, self.wc, self.wr, self.tau, self.p))
        derw = (-self.M*math.tanh(0.04*input_variable[6]) - Melmag)/self.J
        return derw
    
    def get_w(self, input_variable):
        return input_variable[6]

    def get_position_switches(self, t):
        delta_time_swicth = 1000 #dlya nachalnogo sravneniya
        index_switcth = 0
        for i in range(len(self.switch_time_Q)):
            for j in self.switch_time_Q[i]:
                if (((t - j) > 0) and ((t - j) < delta_time_swicth)):           
                    delta_time_swicth = (t - j)
                    index_switcth = i
        if (index_switcth == 0):
            self.position_switch_Q = True
            self.help_var_switch_Q == False
            self.Roff = 0
        elif (index_switcth == 1):
            self.position_switch_Q = False
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
        if (self.position == 0):
            if ((self.x > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
                if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                if (self.position_switch_Q == False):
                    return ("Q:OFF_SWITCH")
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
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
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/AM/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw')

        
    def view_result(self, m_x, m_y):
        global n_fig
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):               
            return True
    
    def change_parameter_in_model(self, m_x, m_y, WIDTH):
        self.k_click = 0.1
        if ((m_x > self.x + self.k_click*self.image_width) and (m_x < self.x + self.image_width - self.k_click*self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            self.state_change_parameter = 1
            self.mass_entry = []
            self.mass_var = []
            switch_time_Q_on_string = ""
            for i in self.switch_time_Q[0]:
                switch_time_Q_on_string = switch_time_Q_on_string + str(i) + ", "
            switch_time_Q_off_string = ""
            for i in self.switch_time_Q[1]:
                switch_time_Q_off_string = switch_time_Q_off_string + str(i) + ", "
            current_var = [self.p, self.J, self.Rc,self.Rr,self.Lcs,self.Lrs,self.l,self.tau, self.delta, self.wc, self.wr, self.M, switch_time_Q_on_string, switch_time_Q_off_string]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(current_var[i])))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)

    def set_parameter_in_model(self):
        for i in range(len(self.mass_var)):
            if (i == 0):
                self.p = float(self.mass_var[i].get())
            elif (i == 1):
                self.J = float(self.mass_var[i].get())
            elif (i == 2):
                self.Rc = float(self.mass_var[i].get())
            elif (i == 3):
                self.Rr = float(self.mass_var[i].get())
            elif (i == 4):
                self.Lcs = float(self.mass_var[i].get())
            elif (i == 5):
                self.Lrs = float(self.mass_var[i].get())
            elif (i == 6):
                self.l = float(self.mass_var[i].get())
            elif (i == 7):
                self.tau = float(self.mass_var[i].get())
            elif (i == 8):
                self.delta = float(self.mass_var[i].get())
            elif (i == 9):
                self.wc = float(self.mass_var[i].get())
            elif (i == 10):
                self.wr = float(self.mass_var[i].get())
            elif (i == 11):
                self.M = float(self.mass_var[i].get())
            elif (i == 12):
                self.switch_time_Q[0] = []
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_Q[0].append(float(j))  
            elif (i == 13):
                self.switch_time_Q[1] = []
                for j in self.mass_var[i].get().split(", "):
                    if (j != ""):
                        self.switch_time_Q[1].append(float(j)) 

    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y
