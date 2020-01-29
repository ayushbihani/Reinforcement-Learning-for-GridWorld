import time
import tkinter as tk
import numpy as np
from tkinter import ttk
from PIL import ImageTk, Image


pixels = 100
PhotoImage = ImageTk.PhotoImage
NORM_FONT= ("Verdana", 10)

class Environment(tk.Tk):
    def __init__(self):
        super(Environment, self).__init__()
        self.height = 5
        self.width = 5
        self.actions = ['UP','LEFT','DOWN','RIGHT']
        self.title = "Dog Gridworld"
        self.images = self.get_images()
        self.canvas = self.create_env()
        self.initial_state = self.get_state_no(self.dog)
        self.fire_states = [self.get_state_no(x) for x in self.fires]
        self.texts = []

    def create_env(self):
        canvas = tk.Canvas(self, height = (self.height+1) * pixels, width = self.width * pixels, bg='white')
        for i in range(0, self.width * pixels, 100):
            canvas.create_line(0, i, pixels*self.width, i)

        for i in range(0, (self.height+1) * pixels, 100):
            canvas.create_line(i,0,i, pixels * self.height)
        self.dog = canvas.create_image(1*pixels/2, 1*pixels/2, image = self.images['dog'])
        self.fire_1 = canvas.create_image(3*pixels/2, 3*pixels/2, image = self.images['fire'])
        self.fire_2 = canvas.create_image(3*pixels/2, 5*pixels/2, image = self.images['fire'])
        self.fire_3 = canvas.create_image(1*pixels/2, 7*pixels/2, image = self.images['fire'])
        self.fire_4 = canvas.create_image(7*pixels/2, 5*pixels/2, image = self.images['fire'])
        self.fire_5 = canvas.create_image(7*pixels/2, 9*pixels/2, image = self.images['fire'])
        self.apple_1 = canvas.create_image(5*pixels/2, 5*pixels/2, image = self.images['apple'])
        self.apple_2 = canvas.create_image(1*pixels/2, 9*pixels/2, image = self.images['apple'])
        self.text_msg = canvas.create_text(5*pixels/2, 11*pixels/2, text="Welcome to the dog world")
        self.fires = [self.fire_1, self.fire_2, self.fire_3, self.fire_4, self.fire_5]
        self.goals_achieved = set()
        canvas.pack()
        return canvas

    def get_images(self):
        dog = PhotoImage(Image.open("images/dog.jpg").resize((int(0.8*pixels), int(0.8*pixels))))
        fire = PhotoImage(Image.open("images/fire.jpg").resize((int(0.8*pixels), int(0.8*pixels))))
        apple = PhotoImage(Image.open("images/apple.jpg").resize((int(0.8*pixels), int(0.8*pixels))))
        return {'dog':dog, 'fire':fire, 'apple':apple}

    def get_state(self, coords):
        x = int((coords[0] - pixels/2)/pixels)
        y = int((coords[1] - pixels/2)/pixels)
        return x*self.width + y

    def get_state_no(self, canvas_object):
        return self.get_state(self.canvas.coords(canvas_object))
    
    def restart(self):
        time.sleep(0.01)
        self.canvas.itemconfigure(self.text_msg, text="New Simulation")
        self.canvas.delete(self.apple_2)
        self.canvas.delete(self.apple_1)
        self.goals_achieved.clear()
        self.apple_1 = self.canvas.create_image(5*pixels/2, 5*pixels/2, image = self.images['apple'], tag="apple")
        self.apple_2 = self.canvas.create_image(1*pixels/2, 9*pixels/2, image = self.images['apple'], tag="apple1")
        self.goal_states = {self.get_state_no(self.apple_1): self.apple_1, self.get_state_no(self.apple_2):self.apple_2}
        self.goal_states_no = {self.get_state_no(self.apple_1), self.get_state_no(self.apple_2)}
        x, y = self.canvas.coords(self.dog)
        self.canvas.move(self.dog, pixels / 2 - x, pixels / 2 - y)
        self.render()
        return self.get_state_no(self.dog)

    def num_states(self):
        return self.width * self.height

    def num_actions(self):
        return len(self.actions)
    
    def step(self, action):
        dog_state = self.canvas.coords(self.dog)
        new_state_coords = np.array([0, 0])
        self.render()
        #up
        if action == 0:
            if dog_state[1] > pixels:
                new_state_coords[1] = -pixels
                 
        #left
        elif action == 1:
            if dog_state[0] > pixels:
                new_state_coords[0] = -pixels
                 
        #down
        elif action == 2:
            if dog_state[1] < (self.height - 1)*pixels:
                new_state_coords[1] = pixels
                 
        #right
        elif action == 3:
            if dog_state[0] < (self.width-1)*pixels:
                new_state_coords[0] = pixels
                 
        self.canvas.move(self.dog, new_state_coords[0], new_state_coords[1])
        next_state = self.get_state_no(self.dog)
        
        if(next_state in self.goal_states):
            self.goals_achieved.add(next_state)
            print(self.goals_achieved)
            self.canvas.delete(self.goal_states[next_state])
            self.goal_states.pop(next_state)
            if self.goals_achieved == self.goal_states_no:
                done, reward = [True, 100] 
            else:
                done, reward = [False, 10]
            self.canvas.itemconfigure(self.text_msg, text = "Found apple!")
        elif(next_state in self.fire_states):
            done, reward = [True, -100]
            self.canvas.itemconfigure(self.text_msg, text = "Burned!Restarting simulation")
        else:
            done, reward = [False, -1]
        self.update()
        return next_state, reward, done

    def get_action(self, index):
        if(index >=0 and index <=3):
            return self.actions[index]
        return -1

    def get_next_state(self, state_, action):
        x, y = state_%self.width, state_/self.width
        state = 0
        if(action == 0):
            state = (y-1)*self.width + x
        elif(action == 1):
            state = y*self.width + (x-1)
        elif(action == 2):
            state = (y+1)*self.width + x
        else:
            state =  y*self.width + (x+1)

        return int(state) if state < self.num_states() else int(state_)

    def render(self):
        time.sleep(0.01)
        self.update()
        