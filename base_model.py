import math
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from scipy. integrate import odeint
import numpy as np

def create_image_for_model(pass_obj, k_size):
    buff_image = ImageTk.PhotoImage(Image.open(pass_obj))
    width_image = buff_image.width()/k_size
    image = ImageTk.PhotoImage(Image.open(pass_obj).resize((int(width_image), int((width_image)*buff_image.height()/buff_image.width())), Image.ANTIALIAS))
    #imagesprite2 = canv.create_image(WIDTH/2,HEIGHT/2,image=image2)
    return image


class Base_model():

    def __init__(self, init_x, init_y, canv, root, example_models, path_to_image_model, d0, position):
        self.canv = canv
        self.root = root
        self.list_example = ttk.Combobox(self.root, values = example_models,state="readonly")
        self.list_example.current(0)
        self.k_size = 6
        self.connection_coords = []
        self.position = position
        self.d0 = d0
        self.image_model_data = create_image_for_model(path_to_image_model + str(self.position) + ".png", self.k_size)
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()

        for item in range(len(self.d0)):
            self.connection_coords.append([])
            if (self.position == 0):
                self.connection_coords[-1].append(self.d0[item][0] / self.k_size)
                self.connection_coords[-1].append(self.d0[item][1] / self.k_size)
            elif (self.position == 1):
                self.connection_coords[-1].append(self.image_height - self.d0[item][1] / self.k_size)
                self.connection_coords[-1].append(self.d0[item][0] / self.k_size)
            elif (self.position == 2):  
                self.connection_coords[-1].append(self.image_width - self.d0[item][0] / self.k_size)
                self.connection_coords[-1].append(self.image_height - self.d0[item][1] / self.k_size)
            elif (self.position == 3):
                self.connection_coords[-1].append(self.d0[item][1] / self.k_size)
                self.connection_coords[-1].append(self.image_width - self.d0[item][0] / self.k_size)

        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')

        self.state_click = 0 #
        self.k_click = 0.1 #
        self.position = 0 #

    def set_state_click(self, m_x, m_y):
        if ((m_x >= self.x + self.k_click*self.image_width) and (m_x <= self.x + self.image_width - self.k_click*self.image_width) and (m_y >= self.y + self.k_click*self.image_height) and (m_y <= self.y + self.image_height - self.k_click*self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0 
            
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x
            self.y = m_y - self.delta_y

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 3):
                self.position = 0
            self.image_model_data = create_image_for_model(self.path_to_image_model + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = self.k_click*self.image_width
            self.delta_y = self.k_click*self.image_height
            self.image_model = self.canv.create_image(m_x - self.k_click*self.image_width, m_y - self.k_click*self.image_height,image = self.image_model_data, anchor = 'nw') 

        self.connection_coords = []

        for item in range(len(self.d0)):
            self.connection_coords.append([])
            if (self.position == 0):
                self.connection_coords[-1].append(self.d0[item][0] / self.k_size)
                self.connection_coords[-1].append(self.d0[item][1] / self.k_size)
            elif (self.position == 1):
                self.connection_coords[-1].append(self.image_height - self.d0[item][1] / self.k_size)
                self.connection_coords[-1].append(self.d0[item][0] / self.k_size)
            elif (self.position == 2):  
                self.connection_coords[-1].append(self.image_width - self.d0[item][0] / self.k_size)
                self.connection_coords[-1].append(self.image_height - self.d0[item][1] / self.k_size)
            elif (self.position == 3):
                self.connection_coords[-1].append(self.d0[item][1] / self.k_size)
                self.connection_coords[-1].append(self.image_width - self.d0[item][0] / self.k_size)
