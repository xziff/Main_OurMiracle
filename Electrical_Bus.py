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
    
class Electrical_Bus:
    state_click = 0
    k_expand = 6
    list_connection = []
    connectivity_to_bus = 0
    number_of_connection = 0
    position = 0

    def __init__(self, init_x, init_y, canv, root):
        self.canv = canv
        self.root = root
        self.image_model_data = create_image_for_model("Image/Electrical Bus/" + str(self.position) + ".png")
        self.image_width = self.image_model_data.width()
        self.image_height = self.image_model_data.height()
        self.x_menu = 0
        self.y_menu = 0
        self.x = init_x
        self.y = init_y
        self.image_model = self.canv.create_image(self.x,self.y,image = self.image_model_data, anchor = 'nw')
        self.model_text = self.canv.create_text(self.x, self.y, text = str(self.number_of_connection), fill = "black", font = ("GOST Type A", "14"), anchor="sw")   
  

    def __del__(self):
        self.canv.delete(self.model_text)
    
    def menu_click(self, m_x, m_y, width_object_menu):
        if ((m_x > self.x_menu) and (m_x < self.x_menu + width_object_menu) and (m_y > self.y_menu) and (m_y < self.y_menu + width_object_menu)):
            return True

    def control_connection(self, models):
        if (self.state_click  == 0):
            self.list_connection = []
            self.number_of_connection = 0
            for i in range(len(models)):
                self.list_connection.append([])
                for j in models[i]:
                    if (j != 0):
                        if (j.connectivity_to_bus == 1):
                            self.list_connection[i].append(j.set_connection(self.x, self.y, self.image_width, self.image_height))
                        else:
                            self.list_connection[i].append("none")
                    else:
                        self.list_connection[i].append("none")

            for i in self.list_connection:
                for j in i:
                    if (j != "none"):
                        self.number_of_connection += 1

            self.canv.delete(self.model_text)
            self.model_text = self.canv.create_text(self.x, self.y, text = str(self.number_of_connection), fill = "black", font = ("GOST Type A", "14"), anchor="sw")
           #print(self.list_connection)
    def set_state_click(self, m_x, m_y):
        if ((m_x > self.x) and (m_x < self.x + self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            if (self.state_click  == 0):
                self.state_click = 1
                self.delta_x = m_x - self.x
                self.delta_y = m_y - self.y
            else:
                self.state_click = 0

    def rotation(self, m_x, m_y):
        if (self.state_click == 1):
            self.position += 1
            if (self.position > 1):
                self.position = 0
            self.image_model_data = create_image_for_model("Image/Electrical Bus/" + str(self.position) + ".png")
            self.image_width = self.image_model_data.width()
            self.image_height = self.image_model_data.height()
            self.canv.delete(self.image_model)
            self.delta_x = 5
            self.delta_y = 5 
            self.image_model = self.canv.create_image(m_x - self.delta_x, m_y - self.delta_y,image = self.image_model_data, anchor = 'nw')



    def view_result(self, m_x, m_y):
        if ((m_x > self.x) and (m_x < self.x + self.image_width) and (m_y > self.y) and (m_y < self.y + self.image_height)):
            return True

    def expand_image_model(self, m_x, m_y):
        if (self.state_click == 1):
            if (self.position == 0):
                buff_image = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/0.png"))
                width_image = buff_image.width()/k_size
                height_image = self.image_model_data.height() + self.k_expand
                self.image_model_data = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/0.png").resize((int(width_image), int(height_image)), Image.ANTIALIAS))
                self.x = m_x - self.delta_x
                self.y = m_y - self.delta_y
                self.image_width = self.image_model_data.width()
                self.image_height = self.image_model_data.height()
                self.canv.delete(self.image_model)
                self.image_model = self.canv.create_image(self.x, self.y ,image = self.image_model_data, anchor = 'nw')
            if (self.position == 1):
                buff_image = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/1.png"))
                height_image = (buff_image.width()/k_size)*buff_image.height()/buff_image.width()
                width_image = self.image_model_data.width() + self.k_expand
                self.image_model_data = ImageTk.PhotoImage(Image.open("Image/Electrical Bus/1.png").resize((int(width_image), int(height_image)), Image.ANTIALIAS))
                self.x = m_x - self.delta_x
                self.y = m_y - self.delta_y
                self.image_width = self.image_model_data.width()
                self.image_height = self.image_model_data.height()
                self.canv.delete(self.image_model)
                self.image_model = self.canv.create_image(self.x, self.y ,image = self.image_model_data, anchor = 'nw')
        
    def move_model(self, m_x, m_y):
        if (self.state_click  == 1):
            self.canv.coords(self.image_model, m_x - self.delta_x, m_y - self.delta_y)
            self.canv.coords(self.model_text, m_x - self.delta_x, m_y - self.delta_y)
            self.x = m_x - self.delta_x           
            self.y = m_y - self.delta_y