# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 14:20:54 2021

Efficiency pilot landmark picker. Used to select cells that will
later be used to re-register imaging stacks from multiple days to each other.

Based off of Pieter's cell annotator used for the in vitro cell counting, but 
modified to handle images in one channel from multiple imaging sessions

@author: dpaynter
"""
# Imports
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import cv2
import os

# Settings
ROImargin = 7
ROIthickness = 2
ImageSize = (300, 300)

# List of colors to use as landmark outlines
colors = ['VioletRed1', 'DarkOliveGreen1', 'SpringGreen2', 'medium spring green', 'turquoise1', 'MediumOrchid1',
          'maroon1', 'red2', 'orange', 'yellow', 'light pink', 'thistle1', 'MediumPurple1', 'SkyBlue1', 'DeepPink2',
          'lemon chiffon', 'snow','VioletRed1', 'DarkOliveGreen1', 'SpringGreen2', 'medium spring green', 'turquoise1', 'MediumOrchid1',
          'maroon1', 'red2', 'orange', 'yellow', 'light pink', 'thistle1', 'MediumPurple1', 'SkyBlue1', 'DeepPink2',
          'lemon chiffon', 'snow', 'VioletRed1', 'DarkOliveGreen1', 'SpringGreen2', 'medium spring green', 'turquoise1', 'MediumOrchid1',
          'maroon1', 'red2', 'orange', 'yellow', 'light pink', 'thistle1', 'MediumPurple1', 'SkyBlue1', 'DeepPink2',
          'lemon chiffon']

# List to hold variables needed to run the canvas.create_oval command in the update_im function
landmark_circle_data = []

# Some inputs
save_data = input('Which mouse + location are you opening? This will name the exported CSV:')
num_timepoints = int(input('How many imaging timepoints will you open?'))

# Set up based on number of timepoints before opening main GUI window
im_nums = []
for tp in range(num_timepoints):
    im_nums.append(tp)

# List of lists to append landmark handles:
im_landmark_handles = []
for tp in range(num_timepoints):
    im_landmark_handles.append([])


class MainWindow():
    """Class that runs the main options window"""

    def __init__(self, main):
        self.main = main

        # landmark container
        self.landmarks = []

        # variable for which image is being annotated
        self.im_var = tk.IntVar(self.main)
        self.im_var.set(0)

        # Counter for which landmark is being added
        self.landmark_id = 0

        self.adding_landmarks = False

        # Create buttons
        self.main.title("Efficiency pilot image annotation")
        self.button_load = tk.Button(self.main, text="Add image directory", fg="black",
                                     command=self.add_image_directory)
        self.button_load.pack()

        self.button_add_landmark = tk.Button(self.main, text="Add landmarks", fg="black",
                                             command=self.add_landmark_toggle)
        self.button_add_landmark.pack()

        # Create button to change the landmark id after annotating a landmark in all timepoints:
        self.button_landmark_counter = tk.Button(self.main, text="Next landmark", fg="black",
                                                 command=self.landmark_count)
        self.button_landmark_counter.pack()

        # Create a label for the value of the landmark counter
        self.lbl = tk.Label(self.main, text='Landmark ID is 0')
        self.lbl.pack()

        # Create an options menu to select which image is being annotated
        self.landmark_im = tk.OptionMenu(self.main, self.im_var, *im_nums, command=self.update_active_im)
        self.landmark_im.pack()

        self.im_lbl = tk.Label(self.main, text='Annotating image 0')
        self.im_lbl.pack()

        self.button_export_data = tk.Button(self.main, text="Export", fg="black", command=self.export_data)
        self.button_export_data.pack()

        self.button_about = tk.Button(self.main, text="About", fg="black", command=self.about)
        self.button_about.pack()

        self.button_quit = tk.Button(self.main, text="Quit", fg="black", command=root.destroy)
        self.button_quit.pack()

        # Set main window position
        main.update()
        w_main = self.main.winfo_width()
        h_main = 400
        w_scr = self.main.winfo_screenwidth()
        h_scr = self.main.winfo_screenheight()
        x_main = int(w_scr * 0.01)
        y_main = int(h_scr * 0.1)
        main.geometry('{}x{}+{}+{}'.format(w_main, h_main, x_main, y_main))

        # start info window
        self.main_position = {'x': x_main + w_main, 'y': y_main}

    def add_image_directory(self):
        """Opens a file window where one image from each imaging session can be selected"""
        self.im_win_list = []
        for tp in range(num_timepoints):
            self.im_dir = filedialog.askdirectory(title="Select folder")
            self.im_win_list.append(image_window(tp, self.main, self.main_position, self.im_dir))
            self.im_win_list[tp].top.bind("<Button-1>", self.edit_landmarks)

    def edit_landmarks(self, event):
        if self.adding_landmarks:
            im_num = int(self.im_var.get())
            z_num = self.im_win_list[im_num].z_slider.get()
            self.landmarks.append([self.landmark_id, im_num, event.x, event.y, z_num])
            x1, y1 = (event.x - ROImargin), (event.y - ROImargin)
            x2, y2 = (event.x + ROImargin), (event.y + ROImargin)

            im_landmark_handles[im_num].append(
                self.im_win_list[im_num].canvas.create_oval(x1, y1, x2, y2, outline=colors[self.landmark_id],
                                                            width=ROIthickness))
            landmark_circle_data.append([x1, y1, x2, y2, self.landmark_id, z_num])

    def landmark_count(self):

        self.landmark_id += 1
        self.lbl.config(text=f'Landmark ID is {self.landmark_id}')

    def update_active_im(self, val):
        self.im_lbl.config(text=f'Annotating image {self.im_var.get()}')

    def add_landmark_toggle(self):

        if self.adding_landmarks:
            self.adding_landmarks = False
            self.button_add_landmark.config(fg="black")
        else:
            self.adding_landmarks = True
            self.button_add_landmark.config(fg="green")

    def export_data(self):

        filename = self.im_dir + '/' + save_data + "-landmarks.csv"
        print("Exporting data to: {}".format(filename))
        with open(filename, "w") as csv_file:
            print("sep=,", file=csv_file)
            print("landmark_ID, im_num, x, y, z ", file=csv_file)
            for nr in range(len(self.landmarks)):
                save_str = "{}, {}, {:1.0f}, {:7.2f}, {}".format(self.landmarks[nr][0], self.landmarks[nr][1],
                                                                 self.landmarks[nr][2], self.landmarks[nr][3],
                                                                 self.landmarks[nr][4])
                print(save_str, file=csv_file)

    def about(self):
        top = tk.Toplevel()
        top.title("About this application...")
        msg = tk.Message(top,
                         text="This little gui can display several images, in which the locations of a given neuron can be annotated over multiple imaging sessions, with the purpose of using the annotations to align"
                              "stacks to each other.", width=600)
        msg.pack()
        msg = tk.Message(top, text="Manual:", width=600)
        msg.pack()
        msg = tk.Message(top,
                         text="- Select images: Select several images, from the same location and channel, from different dates.",
                         width=600)
        msg.pack()
        msg = tk.Message(top,
                         text="- Export: Saves landmarks coordinates to a comma-separated values file (.csv) that has the same name as the first image, but ends on '-landmarks.csv'. This file has one header row, and subsequently one row per landmark  and can be easily openend in e.g. excel or using pandas.",
                         width=600)
        msg.pack()
        msg = tk.Message(top, text="- About: Shows manual and information about version.", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Quit: Ends program --without saving!!--", width=600)
        msg.pack()
        button = tk.Button(top, text="Ok", command=top.destroy)
        button.pack()


class image_window():
    """Class that runs the image windows"""

    def __init__(self, timepoint, main, position, im_directory):
        self.timepoint = timepoint
        # Load in all tiffs in im_directory, store in a list
        self.im_list = []
        for nr, filename in enumerate(os.listdir(im_directory)):
            if filename.endswith('.tiff'):
                im = cv2.imread(os.path.join(im_directory, filename))
                im = im[:, :, 1]
                self.im_list.append(im)

        self.nr_z_planes = len(self.im_list)
        print("Timepoint {} has {} z-planes.".format(timepoint, self.nr_z_planes))

        # Make the window and give it a boring title
        self.top = tk.Toplevel()
        self.top.title(str(self.timepoint))

        # Set up a slider to choose with z plane to display
        self.z_slider = tk.Scale(self.top, orient='horizontal', resolution=1, length=ImageSize[1], from_=0,
                                 to=self.nr_z_planes - 1,
                                 command=self.update_im)
        self.z_slider.pack(side=BOTTOM)

        # Set starting image
        self.im = self.im_list[self.z_slider.get()]
        self.im = cv2.resize(self.im, ImageSize)
        self.im_height, self.im_width = self.im.shape

        # Create canvas to display image on
        self.canvas = tk.Canvas(self.top, height=self.im_height, width=self.im_width)
        self.canvas.pack()

        # Display image on canvas
        self.imgTk = ImageTk.PhotoImage(Image.fromarray(self.im))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgTk)

        # Set image window position
        self.top.update()
        x_temp = int(position['x']) + (self.top.winfo_width() * self.timepoint)
        y_temp = int(position['y'])
        self.top.geometry('+{}+{}'.format(x_temp, y_temp))

    def update_im(self, val):
        self.im = self.im_list[int(val)]
        self.im = cv2.resize(self.im, ImageSize)
        self.im_height, self.im_width = self.im.shape
        self.imgTk = ImageTk.PhotoImage(Image.fromarray(self.im))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgTk)
        self.landmark_vals = []
        for lm in range(len(landmark_circle_data)):
            if landmark_circle_data[lm][5] == self.z_slider.get():
                self.landmark_vals.append(landmark_circle_data[lm])
        for lm in self.landmark_vals:
            self.canvas.create_oval(lm[0], lm[1], lm[2], lm[3], outline=colors[lm[4]], width=ROIthickness)
        self.top.update()
        #TODO make this only update the proper window (as is, landmarks for im0 z26 also show up at im1 z26)



# Set up main window and start main loop
root = tk.Tk()
MainWindow(root)
root.mainloop()
