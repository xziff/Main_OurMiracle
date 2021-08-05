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
def get_wc(Xc, delta, S):
    mu0 = 4 * math.pi * (10 ** (-7))
    return math.sqrt(Xc*math.pi*delta*math.pi/(100*math.pi*2*mu0*2*S*1.5))

def get_wr(wc, delta, S, Pn, cosfi, Un, Ifn, Xc, Rc):
    mu0 = 4 * math.pi * (10 ** (-7))
    return ((math.sqrt((Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc)**2 + (Un*1000/math.sqrt(3)*math.sqrt(2))**2 + 2*Pn/math.sqrt(3)/cosfi/Un*1000*math.sqrt(2)*Xc*Un*1000/math.sqrt(3)*math.sqrt(2)*math.sin(math.fabs(math.acos(cosfi)))))*(math.pi*delta*math.pi)/(100*math.pi*wc*Ifn*mu0*4*S))

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

class SM:
    state_click = 0
    state_change_parameter = 0
    connectivity_to_bus = 1
    position = 0
    delta_x = 0
    delta_y = 0
    k_click = 0.1
    Un = 6.38
    Ur = 350
    tau = 1.2
    l = 1
    wc = 14
    wr = 72
    mu0 = 4 * math.pi * (10 ** (-7))
    delta = 0.015
    Rs = 0.005
    Rr = 0.5
    Ls = 0.004
    Lrs = 0.005
    J = 3000
    D = 2*tau/math.pi
    M_max = -50000
    t0 = 1
    t2 = 1
    Ir_start = Ur/Rr
    w_start = 2*50*math.pi
    phi_start = 0
    Urxx = Un/math.sqrt(3)*1000*Rr*math.pi*delta*math.pi/(100*math.pi*math.sqrt(2)*wc*wr*mu0*2*tau*l)
    Ir_start = Urxx/Rr
    var_text = ["Номинальное напряжение, кВ:",
    "Напряжение возбуждения, В:",
    "Момент инерции ротора, кг*м2:",
    "Активное сопротивление обмотки статора, Ом:",
    "Активное сопротивление обмотки возбуждения, Ом:",
    "Индуктивность поля рассеяния обмотки статора, Гн:",
    "Индуктивность поля рассеяния обмотки ротора, Гн:",
    "Длина машины, м:",
    "Полюсное деление машины, м:",
    "Длина воздушного зазора, м:",
    "Число витков обмотки , шт:",
    "Число витков обмотки ротора, шт:",
    "Момент ПД, Н*м:",
    "Время, при котором начинается подача момента, с:",
    "Время подачи момента ПД, с:",
    "Значение тока возбуждения в начальный момент времени, А:",
    "Значение циклической частоты вращения ротора в начальный момент времени, Гц:",
    "Значение начального угла поворота ротора в начальный момент времени, градус:"  
    ]

    example_SM = [[10.5, 139.61, 2615, 0.002, 0.0953, 0.0001, 0.0002, 3.1, 1.075*math.pi/2, 0.0425, get_wc(2.118, 0.0425, 3.1*1.075*math.pi/2), get_wr(get_wc(2.118, 0.0425, 3.1*1.075*math.pi/2), 0.0425, 3.1*1.075*math.pi/2, 63, 0.8, 10.5, 1465, 2.118, 0)],
    [10.5, 219.24, 3750, 0.00104, 0.126, 0.0001, 0.0002, 3.1, 1.128*math.pi/2, 0.064, get_wc(1.636, 0.064, 3.1*1.128*math.pi/2), get_wr(get_wc(1.636, 0.064, 3.1*1.128*math.pi/2), 0.064, 3.1*1.128*math.pi/2, 110, 0.8, 10.5, 1740, 1.636, 0)],
    [10.5, 205.8, 3750, 0.00104, 0.12, 0.0001, 0.0002, 3.1, 1.128*math.pi/2, 0.064, get_wc(1.402, 0.064, 3.1*1.128*math.pi/2), get_wr(get_wc(1.402, 0.064, 3.1*1.128*math.pi/2), 0.064, 3.1*1.128*math.pi/2, 120, 0.8, 10.5, 1715, 1.402, 0)],
    [15.75, 274.72, 4375, 0.0024, 0.136, 0.0001, 0.0002, 3.85, 1.17*math.pi/2, 0.085, get_wc(2.257, 0.085, 3.85*1.17*math.pi/2), get_wr(get_wc(2.257, 0.085, 3.85*1.17*math.pi/2), 0.085,  3.85*1.17*math.pi/2, 160, 0.85, 15.75, 2020, 2.257, 0)],
    [15.75, 327.12, 6070, 0.00115, 0.174, 0.0001, 0.0002, 4.3, 1.235*math.pi/2, 0.080, get_wc(1.99, 0.080, 4.3*1.235*math.pi/2), get_wr(get_wc(1.99, 0.080, 4.3*1.235*math.pi/2), 0.080, 4.3*1.235*math.pi/2, 200, 0.85, 15.75, 1880, 1.99, 0)],
    [20, 332.05, 7950, 0.001335, 0.1145, 0.0001, 0.0002, 6, 1.265*math.pi/2, 0.095, get_wc(1.804, 0.095, 6*1.265*math.pi/2), get_wr( get_wc(1.804, 0.095, 6*1.265*math.pi/2), 0.095, 6*1.265*math.pi/2, 320, 0.85, 20, 2900, 1.804, 0)],
    [20, 299.154, 10280, 0.0011, 0.0683, 0.0001, 0.0002, 6.3, 1.315*math.pi/2, 0.095, get_wc(1.467, 0.095, 6.3*1.315*math.pi/2), get_wr(get_wc(1.467, 0.095, 6.3*1.315*math.pi/2), 0.095, 6.3*1.315*math.pi/2, 500, 0.85, 20, 4380, 1.467, 0)],
    [18, 439.9616, 8670, 0.00084, 0.2644, 0.0001, 0.0002, 5.3, 1.29*math.pi/2, 0.0824, get_wc(1.62, 0.0824, 5.3*1.29*math.pi/2), get_wr(get_wc(1.62, 0.0824, 5.3*1.29*math.pi/2), 0.0824, 5.3*1.29*math.pi/2, 400, 0.95, 18, 1667, 1.62, 0)]
    ]

    mass_entry = []
    mass_var = []

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = [
        "Пользовательский",
        "ТВФ-63-2УЗ",
        "ТВФ-110-2ЕУЗ",
        "ТВФ-120-2УЗ",
        "ТВВ-160-2ЕУЗ",
        "ТГВ-200-2УЗ",
        "ТВВ-320-2ЕУЗ",
        "ТГВ-500-4УЗ",
        "390H"
        ],state="readonly")
        self.list_example.current(0)
        self.image_model_data = create_image_for_model("Image/SM/" + str(self.position) + ".png")
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

        print(self.width_input, self.width_matrix, self.height_matrix)
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def get_first(self):
        return ([0, 0, self.Ir_start, self.w_start, self.phi_start])

    def get_main_determinant(self, input_variable):
        main_determinant = [[-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(1 + (-1)*math.sin(math.pi/2 - 2*math.pi/3) - (-1)*math.sin(math.pi/6) - (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3)) - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 + 2*math.pi/3) + (-1)*math.sin(math.pi/2 - 2*math.pi/3) - (-1)*math.sin(math.pi/6 - 2*math.pi/3) - (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3)) + self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2+input_variable[4]) - (-1)*math.sin(math.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6) + (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3) - math.sin(-math.pi/6) - (-1)*math.sin(-math.pi/6 + 2*math.pi/3))  - self.Ls, -(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6 - 2*math.pi/3) + (-1)*(-1)*math.sin(math.pi/6 + 2*math.pi/3) - math.sin(-math.pi/6 - 2*math.pi/3) - (-1)*math.sin(-math.pi/6 + 2*math.pi/3)) - self.Ls - self.Ls, -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*((-1)*math.sin(math.pi/6-input_variable[4]) - math.sin(-math.pi/6-input_variable[4]))],
    	                   [-(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 - input_variable[4]) + (-1)*math.sin(math.pi/2 - input_variable[4] - 2*math.pi/3)), -(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-1)*math.sin(math.pi/2 - input_variable[4] - 2*math.pi/3)), -(2*self.wr*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.sin(math.pi/2)) - self.Lrs]
    	                  ]                      
        return main_determinant

    def get_own_matrix(self, input_variable, t):
        own_matrix = [input_variable[0]*self.Rs - input_variable[1]*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(math.cos(math.pi/2 + input_variable[4]) + (-1)*math.cos(math.pi/6 - input_variable[4])),
                    input_variable[1]*self.Rs - (-input_variable[0]-input_variable[1])*self.Rs + input_variable[3]*(2*self.wc*self.wr*input_variable[2]*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(-(-1)*math.cos(math.pi/6 - input_variable[4]) + math.cos(-math.pi/6 - input_variable[4])),
                   input_variable[2]*self.Rr - self.Urxx - moment_pd(t, self.t0, self.t2, self.Ur - self.Urxx) - input_variable[3]*(2*self.wc*self.wr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*(input_variable[0]*math.cos(math.pi/2 - input_variable[4]) + input_variable[1]*math.cos(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-input_variable[0]-input_variable[1])*math.cos(math.pi/2 - input_variable[4] - 2*math.pi/3))]        
        return own_matrix

    def get_voltage_matrix(self, parameter):
        if (parameter == "Q"):
            voltage_matrix = [[-1, 0],
                        [0, -1],
                        [0, 0]
                        ] 
            return voltage_matrix

    def get_current_matrix(self, parameter):
        if (parameter == "Q"):
            current_matrix = [[1, 0, 0],
                        [0, 1, 0],
                        [-1, -1, 0]
                        ] 
            return current_matrix

    def get_additional_variable(self, input_variable, t):
        Melmag = (self.D - 0*self.delta)*self.wr*(2*self.wc*input_variable[2]*self.l*self.mu0)/(math.pi*self.delta)*(input_variable[0]*math.cos(math.pi/2 - input_variable[4]) + input_variable[1]*math.cos(math.pi/2 - input_variable[4] + 2*math.pi/3) + (-input_variable[0]-input_variable[1])*math.cos(math.pi/2 - input_variable[4] - 2*math.pi/3))
        additional_variable = [
                            (moment_pd(t, self.t0, self.t2, self.M_max) - Melmag)/self.J,
                            input_variable[3]
                            ]
        return additional_variable

    def time_interrupt(self):
        return []

    def set_connection(self, bus_x, bus_y, bus_width, bus_height):
        if (self.position == 0):
            if ((self.x + self.image_width > bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x + self.image_width < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 1):
            if ((self.x + self.image_width/2 > bus_x) and (self.y + self.image_height > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y + self.image_height < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 2):
            if ((self.x> bus_x) and (self.y + self.image_height/2 > bus_y) and (self.x < bus_x + bus_width) and (self.y + self.image_height/2 < bus_y + bus_height)):
                return ("Q:ON_SWITCH")
            else:
                return ("none")
        if (self.position == 3):
            if ((self.x + self.image_width/2 > bus_x) and (self.y > bus_y) and (self.x + self.image_width/2 < bus_x + bus_width) and (self.y < bus_y + bus_height)):
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
            self.image_model_data = create_image_for_model("Image/SM/" + str(self.position) + ".png")
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
            current_var = [self.Un,self.Ur,self.J, self.Rs,self.Rr,self.Ls,self.Lrs,self.l,self.tau, self.delta, self.wc, self.wr, self.M_max, self.t0, self.t2, self.Ir_start, self.w_start/2/math.pi, self.phi_start*180/math.pi]
            for i in range(len(self.var_text)):
                self.mass_var.append(StringVar(value=str(round(current_var[i], 3))))
                self.mass_entry.append(Entry(textvariable = self.mass_var[i], width = 12, relief = SOLID, borderwidth = 1, justify = CENTER))
            self.mass_canv_text = []
            for i in range(len(self.var_text)):
                self.mass_canv_text.append(self.canv.create_text(WIDTH/2, i*25, text = self.var_text[i], fill = "black", font = ("GOST Type A", "16"), anchor="ne"))
                self.mass_entry[i].place(x = WIDTH/2+ 20, y = i*25)
            self.mass_canv_text.append(self.canv.create_text(WIDTH/2, len(self.var_text)*25 + 25, text = "Синхронное индуктивное сопротивление в УР, Ом: " + str(round(100*math.pi*((2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)+(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2-2*math.pi/3)*math.cos(2*math.pi/3)+(2*self.wc*self.wc*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi)*math.sin(math.pi/2+2*math.pi/3)*math.cos(2*math.pi/3) + self.Ls), 3)), fill = "black", font = ("GOST Type A", "16"), anchor="center"))
            self.mass_canv_text.append(self.canv.create_text(WIDTH/2, (1+len(self.var_text))*25 + 25, text = "Действующее значение ЭДС генератора в УР, кВ: " + str(round(100/1000*math.pi*(math.sqrt(2)*self.wc*self.wr*self.Ur/self.Rr*self.mu0*2*self.tau*self.l)/(math.pi*self.delta*math.pi), 3)), fill = "black", font = ("GOST Type A", "16"), anchor="center"))
            self.mass_canv_text.append(self.canv.create_text(WIDTH/2, (2+len(self.var_text))*25 + 25, text = "Выбор существующего генератора", fill = "black", font = ("GOST Type A", "16"), anchor="center"))
            self.list_example.place(x = WIDTH/2 - 50, y = (3+len(self.var_text))*25 + 25)

    def set_parameter_in_model(self):
        print(self.list_example.get())
        if (self.list_example.get() == "Пользовательский"):
            for i in range(len(self.mass_var)):
                if (i == 0):
                    self.Un = float(self.mass_var[i].get())
                elif (i == 1):
                    self.Ur = float(self.mass_var[i].get())
                elif (i == 2):
                    self.J = float(self.mass_var[i].get())
                elif (i == 3):
                    self.Rs = float(self.mass_var[i].get())
                elif (i == 4):
                    self.Rr = float(self.mass_var[i].get())
                elif (i == 5):
                    self.Ls = float(self.mass_var[i].get())
                elif (i == 6):
                    self.Lrs = float(self.mass_var[i].get())
                elif (i == 7):
                   self.l = float(self.mass_var[i].get())
                elif (i == 8):
                    self.tau = float(self.mass_var[i].get())
                elif (i == 9):
                    self.delta = float(self.mass_var[i].get())
                elif (i == 10):
                    self.wc = float(self.mass_var[i].get())
                elif (i == 11):
                    self.wr = float(self.mass_var[i].get())
                elif (i == 12):
                    self.M_max = float(self.mass_var[i].get())
                elif (i == 13):
                    self.t0 = float(self.mass_var[i].get())
                elif (i == 14):
                    self.t2 = float(self.mass_var[i].get())
                elif (i == 15):
                    self.Ir_start = float(self.mass_var[i].get())
                elif (i == 16):
                    self.w_start = float(self.mass_var[i].get()) * 2 * math.pi
                elif (i == 17):
                    self.phi_start = float(self.mass_var[i].get()) * math.pi / 180
        else:
            if (self.list_example.get() == "ТВФ-63-2УЗ"):
                current_index = 0
            if (self.list_example.get() == "ТВФ-110-2ЕУЗ"):
                current_index = 1
            if (self.list_example.get() == "ТВФ-120-2УЗ"):
                current_index = 2
            if (self.list_example.get() == "ТВВ-160-2ЕУЗ"):
                current_index = 3
            if (self.list_example.get() == "ТГВ-200-2УЗ"):
                current_index = 4
            if (self.list_example.get() == "ТВВ-320-2ЕУЗ"):
                current_index = 5
            if (self.list_example.get() == "ТГВ-500-4УЗ"):
                current_index = 6
            if (self.list_example.get() == "390H"):
                current_index = 7
            for i in range(len(self.mass_var)):
                if (i == 0):
                    self.Un = self.example_SM[current_index][i]
                elif (i == 1):
                    self.Ur = self.example_SM[current_index][i]
                elif (i == 2):
                    self.J = self.example_SM[current_index][i]
                elif (i == 3):
                    self.Rs = self.example_SM[current_index][i]
                elif (i == 4):
                    self.Rr = self.example_SM[current_index][i]
                elif (i == 5):
                    self.Ls = self.example_SM[current_index][i]
                elif (i == 6):
                    self.Lrs = self.example_SM[current_index][i]
                elif (i == 7):
                   self.l = self.example_SM[current_index][i]
                elif (i == 8):
                    self.tau = self.example_SM[current_index][i]
                elif (i == 9):
                    self.delta = self.example_SM[current_index][i]
                elif (i == 10):
                    self.wc = self.example_SM[current_index][i]
                elif (i == 11):
                    self.wr = self.example_SM[current_index][i]
                elif (i == 12):
                    self.M_max = float(self.mass_var[i].get())
                elif (i == 13):
                    self.t0 = float(self.mass_var[i].get())
                elif (i == 14):
                    self.t2 = float(self.mass_var[i].get())
                elif (i == 15):
                    self.Ir_start = float(self.mass_var[i].get())
                elif (i == 16):
                    self.w_start = float(self.mass_var[i].get()) * 2 * math.pi
                elif (i == 17):
                    self.phi_start = float(self.mass_var[i].get()) * math.pi / 180

            self.Urxx = self.Un/math.sqrt(3)*1000*self.Rr*math.pi*self.delta*math.pi/(100*math.pi*math.sqrt(2)*self.wc*self.wr*self.mu0*2*self.tau*self.l)
            self.Ir_start = self.Urxx/self.Rr
        self.D = 2*self.tau/math.pi
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y