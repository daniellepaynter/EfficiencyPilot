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
from PIL import Image, ImageTk
import cv2
import numpy as np
import os

# Settings
ROImargin = 7
ROIthickness = 2
ImageSize = (512, 512)

im_names = ['self.im1_filename', 'self.im2_filename', 'self.m3_filename', 'self.im4_filename', 'self.im5_filename',
            'self.im6_filename', 'self.im7_filename', 'self.im8_filename', 'selfim9_filename', 'self.im10_filename']
win_names = ['self.im1_win', 'self.im2_win', 'self.im3_win', 'self.im4_win', 'self.im5_win', 'self.im6_win',
             'self.im7_win', 'self.im8_win', 'self.im9_win', 'self.im10_win']
im_nums = [1,2,3,4,5,6,7,8,9,10]


class MainWindow():
    """Class that runs the main options window"""

    def __init__(self, main):
        self.main = main

        # ROI container

        self.landmarks = []

        self.im_var = tk.StringVar(self.main)
        self.im_var.set(1)

        self.landmark_id = 0

        self.im1_landmark_handles = []
        self.im2_landmark_handles = []
        self.im3_landmark_handles = []
        self.im4_landmark_handles = []
        self.im5_landmark_handles = []
        self.im6_landmark_handles = []
        self.im7_landmark_handles = []
        self.im8_landmark_handles = []
        self.im9_landmark_handles = []
        self.im10_landmark_handles = []

        self.adding_landmarks = False

        # Create load and save buttons
        self.main.title("Efficiency pilot image annotation")
        self.button_load = tk.Button(self.main, text="Select images", fg="black", command=self.select_image_files)
        self.button_load.pack()

        self.button_add_landmark = tk.Button(self.main, text="Add landmarks", fg="black",
                                             command=self.add_landmark_toggle)
        self.button_add_landmark.pack()

        self.button_landmark_counter = tk.Button(self.main, text="Next landmark", fg="black",
                                                 command=self.landmark_count)
        self.button_landmark_counter.pack()

        self.lbl = tk.Label(self.main, text='Landmark ID is 0')
        self.lbl.pack()

        self.landmark_im = tk.OptionMenu(self.main, self.im_var, *im_nums)
        self.landmark_im.pack()

        self.button_save_rois = tk.Button(self.main, text="Save ROIs", fg="black", command=self.save_rois)
        self.button_save_rois.pack()

        self.button_export_data = tk.Button(self.main, text="Export", fg="black", command=self.export_data)
        self.button_export_data.pack()

        self.button_about = tk.Button(self.main, text="About", fg="black", command=self.about)
        self.button_about.pack()

        self.button_quit = tk.Button(self.main, text="Quit", fg="black")
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

    def select_image_files(self):

        filenames = filedialog.askopenfilenames()
        self.im1_filename = filenames[0]
        self.im1_win = image_window(0, self.main, self.main_position, self.im1_filename)
        self.im1_win.top.bind("<Button-1>", self.edit_landmarks)

        self.im2_filename = filenames[1]
        self.im2_win = image_window(1, self.main, self.main_position, self.im2_filename)
        self.im2_win.top.bind("<Button-1>", self.edit_landmarks)
        try:
            self.im3_filename = filenames[2]
            self.im3_win = image_window(2, self.main, self.main_position, self.im3_filename)
            self.im3_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass
        try:
            self.im4_filename = filenames[3]
            self.im4_win = image_window(3, self.main, self.main_position, self.im4_filename)
            self.im4_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass
        try:
            self.im5_filename = filenames[4]
            self.im5_win = image_window(4, self.main, self.main_position, self.im5_filename)
            self.im5_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass
        try:
            self.im6_filename = filenames[5]
            self.im6_win = image_window(5, self.main, self.main_position, self.im6_filename)
            self.im6_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass
        try:
            self.im7_filename = filenames[6]
            self.im7_win = image_window(6, self.main, self.main_position, self.im7_filename)
            self.im7_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass
        try:
            self.im8_filename = filenames[7]
            self.im8_win = image_window(7, self.main, self.main_position, self.im8_filename)
            self.im8_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass
        try:
            self.im9_filename = filenames[8]
            self.im9_win = image_window(8, self.main, self.main_position, self.im9_filename)
            self.im9_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass
        try:
            self.im10_filename = filenames[9]
            self.im10_win = image_window(9, self.main, self.main_position, self.im10_filename)
            self.im10_win.top.bind("<Button-1>", self.edit_landmarks)
        except:
            pass

    def edit_landmarks(self, event):

        if self.adding_landmarks:
            im_num = int(self.im_var.get())
            self.landmarks.append([ self.landmark_id, im_num, event.x, event.y ])
            x1, y1 = (event.x - ROImargin), (event.y - ROImargin)
            x2, y2 = (event.x + ROImargin), (event.y + ROImargin)
            im_size = (self.im1_win.im_height, self.im1_win.im_width)
            if self.im_var.get() == 1:
                self.im1_landmark_handles.append(self.im1_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 2:
                self.im2_landmark_handles.append(self.im2_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 3:
                self.im3_landmark_handles.append(self.im3_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 4:
                self.im4_landmark_handles.append(self.im4_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 5:
                self.im5_landmark_handles.append(self.im5_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 6:
                self.im6_landmark_handles.append(self.im6_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 7:
                self.im7_landmark_handles.append(self.im7_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 8:
                self.im8_landmark_handles.append(self.im8_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 9:
                self.im9_landmark_handles.append(self.im9_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))
            elif self.im_var.get() == 10:
                self.im10_landmark_handles.append(self.im10_win.canvas.create_oval(x1, y1, x2, y2, width=ROIthickness))

    def landmark_count(self):
        self.landmark_id += 1
        self.lbl.config(text=f'Landmark ID is {self.landmark_id}')

    def add_landmark_toggle(self):
        if self.adding_landmarks:
            self.adding_landmarks = False
            self.button_add_landmark.config(fg="black")
        else:
            self.adding_landmarks = True
            self.button_add_landmark.config(fg="green")

    # TODO: make this functional with landmarks
    def delete_roi_toggle(self):
        if self.deleting_rois:
            self.deleting_rois = False
            self.button_delete_rois.config(fg="black")
        else:
            self.deleting_rois = True
            self.button_delete_rois.config(fg="red")
            self.modifying_ids = False
            self.button_modify_ids.config(fg="black")
            self.adding_rois = False
            self.button_add_rois.config(fg="black")
            self.adding_landmarks = False
            self.button_add_landmark.config(fg="black")

    # TODO: make this function for landmarks
    def save_rois(self):
        n_rois = len(self.ROIs)
        data_mat = np.zeros((n_rois, 3))
        for nr in range(n_rois):
            data_mat[nr, 0] = self.ROIs[nr][0]
            data_mat[nr, 1] = self.ROIs[nr][1]
            data_mat[nr, 2] = self.ROIids[nr]
        data_dict = {"roidata": data_mat}
        filename = os.path.splitext(self.im1_filename)[0] + "-ROIs.npy"
        print("Saving ROIs to: {}".format(filename))
        np.save(filename, data_dict)

    def export_data(self):
        n_landmarks = self.landmark_id
        im_size = (self.im1_win.im_height, self.im1_win.im_width)
        im1 = self.im1_win.im
        im2 = self.im2_win.im
        try:
            im3 = self.im3_win.im
        except:
            pass
        try:
            im4 = self.im4_win.im
            im5 = self.im5_win.im
            im6 = self.im6_win_im
            im7 = self.im7_win.im
            im8 = self.im8_win.im
            im9 = self.im9_win.im
            im10 = self.im10_win_im
        except:
            pass
        filename = os.path.splitext(self.im1_filename)[0] + "-landmarks.csv"
        print("Exporting data to: {}".format(filename))
        with open(filename, "w") as csv_file:
            print("sep=,", file=csv_file)
            print("landmark_ID, im_num, x, y ", file=csv_file)
            for nr in range(len(self.landmarks)):
                save_str = "{}, {}, {:1.0f}, {:7.2f}".format(self.landmarks[nr][0], self.landmarks[nr][1],
                                                                       self.landmarks[nr][2], self.landmarks[nr][3])
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

    def __init__(self, nr, main, position, im_file_name):
        self.top = tk.Toplevel()

        # Load image from file

        title_name = os.path.basename(im_file_name)
        self.top.title(title_name)

        self.im = cv2.imread(im_file_name)
        self.im = self.im[:, :, 1]

        self.im = cv2.resize(self.im, ImageSize)
        self.im_height, self.im_width = self.im.shape

        self.im_file_name = im_file_name

        # Create canvas for image
        self.canvas = tk.Canvas(self.top, width=self.im_width, height=self.im_height)
        self.canvas.pack()

        # Display image on canvas for first time
        self.imgTk = ImageTk.PhotoImage(Image.fromarray(self.im))
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgTk)

        # Set image window position
        self.top.update()
        x_temp = int(position['x']) + (self.top.winfo_width() * nr)
        y_temp = int(position['y'])
        self.top.geometry('+{}+{}'.format(x_temp, y_temp))


# Set up main window and start main loop
root = tk.Tk()
MainWindow(root)
root.mainloop()
