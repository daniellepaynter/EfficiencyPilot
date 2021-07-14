# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 14:20:54 2021

Efficiency pilot cell counting assistant. Based off of Pieter's cell annotator
used for the in vitro cell counting, but modified to handle images in one channel
from multiple imaging sessions'

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
ROIid_ratio = 1
ImageSize = (512,512)
IDcolors = ["#0000FF","#FF0000","#00FF00"]

class MainWindow():
    """Class that runs the main options window"""

    def __init__(self, main):
        self.main = main

        # ROI container
        self.ROIs = []
        self.ROIids = []
        self.landmarks = []
        self.im_var = tk.IntVar()
        self.im1_ROIhandles = []
        self.im2_ROIhandles = []
        self.im3_ROIhandles = []
        self.im4_ROIhandles = []
        self.im5_ROIhandles = []
        self.im1_landmark_handles = []
        self.im2_landmark_handles = []
        self.im3_landmark_handles = []
        self.im4_landmark_handles = []
        self.im5_landmark_handles = []
        self.adding_rois = False
        self.deleting_rois = False
        self.modifying_ids = False
        self.adding_landmarks = False
        
        # Create load and save buttons
        self.main.title("Efficiency pilot image annotation")
        self.button_load = tk.Button( self.main, text="Select images", fg="black", command=self.select_image_files )
        self.button_load.pack()

        self.button_add_landmark = tk.Button( self.main, text="Add landmark", fg="black", command=self.add_landmark_toggle )
        self.button_add_landmark.pack()
        
        
        self.landmark_im = tk.Radiobutton(self.main, text="Image1", variable=self.im_var, value=1)
        self.landmark_im.pack()

        self.landmark_im = tk.Radiobutton(self.main, text="Image2", variable=self.im_var, value=2)
        self.landmark_im.pack()
        
        self.landmark_im = tk.Radiobutton(self.main, text="Image3", variable=self.im_var, value=3)
        self.landmark_im.pack()
        
        self.landmark_im = tk.Radiobutton(self.main, text="Image4", variable=self.im_var, value=4)
        self.landmark_im.pack()
        
        self.landmark_im = tk.Radiobutton(self.main, text="Image5", variable=self.im_var, value=5)
        self.landmark_im.pack()
        


        self.button_add_rois = tk.Button( self.main, text="Add ROIs", fg="black", command=self.add_roi_toggle )
        self.button_add_rois.pack()

        self.button_delete_rois = tk.Button( self.main, text="Del ROIs", fg="black", command=self.delete_roi_toggle )
        self.button_delete_rois.pack()

        self.button_modify_ids = tk.Button( self.main, text="Mod IDs", fg="black", command=self.modify_id_toggle )
        self.button_modify_ids.pack()

        self.button_load_rois = tk.Button( self.main, text="Load ROIs", fg="black", command=self.load_rois )
        self.button_load_rois.pack()

        self.button_save_rois = tk.Button( self.main, text="Save ROIs", fg="black", command=self.save_rois )
        self.button_save_rois.pack()

        self.button_export_data = tk.Button( self.main, text="Export", fg="black", command=self.export_data )
        self.button_export_data.pack()

        self.button_about = tk.Button( self.main, text="About", fg="black", command=self.about )
        self.button_about.pack()

        self.button_quit = tk.Button( self.main, text="Quit", fg="black" )
        self.button_quit.pack()
        

        # Set main window position
        main.update()
        w_main = self.main.winfo_width()
        h_main = 400
        w_scr = self.main.winfo_screenwidth()
        h_scr = self.main.winfo_screenheight()
        x_main = int(w_scr*0.01)
        y_main = int(h_scr*0.1)
        main.geometry('{}x{}+{}+{}'.format(w_main, h_main, x_main, y_main))

        # start info window
        self.main_position = {'x': x_main+w_main, 'y': y_main}
            
        
        
    def select_image_files(self):
        filenames = filedialog.askopenfilenames()
        
        self.im1_filename = filenames[0]
        self.im2_filename = filenames[1]
        self.im3_filename = filenames[2]
        self.im4_filename = filenames[3]
        self.im5_filename = filenames[4]
        
        self.im1_win = image_window( 0, self.main, self.main_position, self.im1_filename )
        self.im2_win = image_window( 1, self.main, self.main_position, self.im2_filename )
        self.im3_win = image_window( 2, self.main, self.main_position, self.im3_filename )
        self.im4_win = image_window( 3, self.main, self.main_position, self.im4_filename )
        self.im5_win = image_window( 4, self.main, self.main_position, self.im5_filename )
        
        self.im1_win.top.bind( "<Button-1>", self.edit_rois )
        self.im2_win.top.bind( "<Button-1>", self.edit_rois )
        self.im3_win.top.bind( "<Button-1>", self.edit_rois )
        self.im4_win.top.bind( "<Button-1>", self.edit_rois )
        self.im5_win.top.bind( "<Button-1>", self.edit_rois )

    def edit_rois(self, event):
        
        if self.adding_landmarks:
            self.landmarks.append( [event.x, event.y, self.im_var.get()] )
            x1, y1 = ( event.x - ROImargin ), ( event.y - ROImargin )
            x2, y2 = ( event.x + ROImargin ), ( event.y + ROImargin )
            im_size = (self.im1_win.im_height,self.im1_win.im_width)
            
            if self.im_var.get() == 1:
                self.im1_landmark_handles.append( self.im1_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
            elif self.im_var.get() == 2:
                self.im2_landmark_handles.append( self.im2_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
            elif self.im_var.get() == 3:
                self.im3_landmark_handles.append( self.im3_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
            elif self.im_var.get() == 4:
                self.im4_landmark_handles.append( self.im4_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
            elif self.im_var.get() == 5:
                self.im5_landmark_handles.append( self.im5_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
                
                
        if self.adding_rois:
            if self.find_closeby_roi(event.x, event.y) is None:
                self.ROIs.append( [event.x, event.y] )
                x1, y1 = ( event.x - ROImargin ), ( event.y - ROImargin )
                x2, y2 = ( event.x + ROImargin ), ( event.y + ROImargin )

                # Find ID
                im_size = (self.im1_win.im_height,self.im1_win.im_width)
                roi_mask = np.zeros(im_size, np.uint8)
                cv2.circle(roi_mask,(event.x,event.y),ROImargin,1,thickness=-1)
                im1_data = cv2.bitwise_and(self.im1_win.im, self.im1_win.im, mask=roi_mask)
                im1_int = np.sum(im1_data) / np.sum(roi_mask)
                im2_data = cv2.bitwise_and(self.im2_win.im, self.im2_win.im, mask=roi_mask)
                im2_int = np.sum(im2_data) / np.sum(roi_mask)
                im3_data = cv2.bitwise_and(self.im3_win.im, self.im3_win.im, mask=roi_mask)
                im3_int = np.sum(im3_data) / np.sum(roi_mask)
                im4_data = cv2.bitwise_and(self.im4_win.im, self.im4_win.im, mask=roi_mask)
                im4_int = np.sum(im4_data) / np.sum(roi_mask)                
                im5_data = cv2.bitwise_and(self.im5_win.im, self.im5_win.im, mask=roi_mask)
                im5_int = np.sum(im5_data) / np.sum(roi_mask)                
                
              #  if im2_int / gfp_int > ROIid_ratio:
              #      self.ROIids.append(1)
             #   elif gfp_int / tom_int > ROIid_ratio:
            #        self.ROIids.append(2)
             #   else:
             #       self.ROIids.append(0)

            #    self.im1_ROIhandles.append( self.im1_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
             #   self.im2_ROIhandles.append( self.im2_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
              # self.im4_ROIhandles.append( self.im4_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
                #self.im5_ROIhandles.append( self.im5_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            
                self.im1_ROIhandles.append( self.im1_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
                self.im2_ROIhandles.append( self.im2_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
                self.im3_ROIhandles.append( self.im3_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
                self.im4_ROIhandles.append( self.im4_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
                self.im5_ROIhandles.append( self.im5_win.canvas.create_oval( x1, y1, x2, y2, width=ROIthickness ) )
                
                
                
        if self.deleting_rois:
            nr = self.find_closeby_roi(event.x, event.y)
            if nr is not None:
                self.im1_win.canvas.delete(self.im1_ROIhandles[nr])
                self.im2_win.canvas.delete(self.im2_ROIhandles[nr])
                self.im3_win.canvas.delete(self.im3_ROIhandles[nr])
                self.im4_win.canvas.delete(self.im4_ROIhandles[nr])
                self.im5_win.canvas.delete(self.im5_ROIhandles[nr])
                
                del self.ROIs[nr]
                del self.ROIids[nr]
                del self.im1_ROIhandles[nr]
                del self.im2_ROIhandles[nr]
                del self.im3_ROIhandles[nr]
                del self.im4_ROIhandles[nr]
                del self.im5_ROIhandles[nr]                
                
        if self.modifying_ids:
            nr = self.find_closeby_roi(event.x, event.y)
            if nr is not None:
                self.ROIids[nr] = np.mod(self.ROIids[nr]+1,3)
                self.im1_win.canvas.delete(self.im1_ROIhandles[nr])
                self.im2_win.canvas.delete(self.im2_ROIhandles[nr])
                self.im3_win.canvas.delete(self.im3_ROIhandles[nr])
                self.im4_win.canvas.delete(self.im4_ROIhandles[nr])
                self.im5_win.canvas.delete(self.im5_ROIhandles[nr])
                x1, y1 = ( self.ROIs[nr][0] - ROImargin ), ( self.ROIs[nr][1] - ROImargin )
                x2, y2 = ( self.ROIs[nr][0] + ROImargin ), ( self.ROIs[nr][1] + ROImargin )
                self.im1_ROIhandles[nr] = ( self.im1_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )
                self.im2_ROIhandles[nr] = ( self.im2_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )
                self.im3_ROIhandles[nr] = ( self.im3_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )
                self.im4_ROIhandles[nr] = ( self.im4_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )
                self.im5_ROIhandles[nr] = ( self.im5_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )

    def find_closeby_roi(self, x, y):
        for nr,(_x,_y) in enumerate(self.ROIs):
            if abs(_x-x)<ROImargin and abs(_y-y)<ROImargin:
                return nr
        return None
    
    def add_landmark_toggle(self):
        if self.adding_landmarks:
            self.adding_landmarks = False
            self.button_add_landmark.config(fg="black")
        else:
            self.adding_landmarks = True
            self.button_add_landmark.config(fg="green")
            self.modifying_ids = False
            self.button_modify_ids.config(fg="black")
            self.deleting_rois = False
            self.button_delete_rois.config(fg="black")
            
            
    def add_roi_toggle(self):
        if self.adding_rois:
            self.adding_rois = False
            self.button_add_rois.config(fg="black")
        else:
            self.adding_rois = True
            self.button_add_rois.config(fg="green")
            self.modifying_ids = False
            self.button_modify_ids.config(fg="black")
            self.deleting_rois = False
            self.button_delete_rois.config(fg="black")
            self.adding_landmarks = False
            self.button_add_landmark.config(fg="black")
            self.adding_rois = False
            self.button_add_rois.config(fg="black")

    def delete_roi_toggle( self ):
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

    def modify_id_toggle(self):
        if self.modifying_ids:
            self.modifying_ids = False
            self.button_modify_ids.config(fg="black")
        else:
            self.modifying_ids = True
            self.button_modify_ids.config(fg="blue")
            self.deleting_rois = False
            self.button_delete_rois.config(fg="black")
            self.adding_rois = False
            self.button_add_rois.config(fg="black")
            self.adding_landmarks = False
            self.button_add_landmark.config(fg="black")

    def load_rois(self):
        filename = filedialog.askopenfilename()
        print("Loading ROIs from: {}".format(filename))
        data_mat = np.load(filename, allow_pickle=True).item()["roidata"]
        n_rois = data_mat.shape[0]
        for nr in range(n_rois):
            x = int(data_mat[nr,0])
            y = int(data_mat[nr,1])
            roi_id = int(data_mat[nr,2])
            self.ROIs.append( [x, y] )
            x1, y1 = ( x - ROImargin ), ( y - ROImargin )
            x2, y2 = ( x + ROImargin ), ( y + ROImargin )
            self.ROIids.append(roi_id)
            self.im1_ROIhandles.append( self.im1_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            self.im2_ROIhandles.append( self.im2_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            self.im3_ROIhandles.append( self.im3_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            self.im4_ROIhandles.append( self.im4_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            self.im5_ROIhandles.append( self.im5_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )

    def save_rois(self):
        n_rois = len(self.ROIs)
        data_mat = np.zeros((n_rois,3))
        for nr in range(n_rois):
            data_mat[nr,0] = self.ROIs[nr][0]
            data_mat[nr,1] = self.ROIs[nr][1]
            data_mat[nr,2] = self.ROIids[nr]
        data_dict = { "roidata": data_mat}
        filename = os.path.splitext(self.im1_filename)[0] + "-ROIs.npy"
        print("Saving ROIs to: {}".format(filename))
        np.save(filename,data_dict)

    def export_data(self):
        n_rois = len(self.ROIs)
        im_size = (self.im1_win.im_height,self.im1_win.im_width)
        im1 = self.im1_win.im
        im2 = self.im2_win.im
        im3 = self.im3_win.im
        im4 = self.im4_win.im
        im5 = self.im5_win.im

        filename = os.path.splitext(self.im1_filename)[0] + "-data.csv"
        print("Exporting data to: {}".format(filename))
        with open(filename, "w") as csv_file:
            print("sep=,", file=csv_file)
            print("x, y, id, gfp, tom", file=csv_file)
            for nr in range(n_rois):
                roi_mask = np.zeros(im_size, np.uint8)
                cv2.circle(roi_mask,(self.ROIs[nr][0],self.ROIs[nr][1]),ROImargin,1,thickness=-1)
                im1_data = cv2.bitwise_and(im1, im1, mask=roi_mask)
                im1_int = np.sum(im1_data) / np.sum(roi_mask)
                tom_data = cv2.bitwise_and(im2, im2, mask=roi_mask)
                tom_int = np.sum(tom_data) / np.sum(roi_mask)
                save_str = "{:4.0f}, {:4.0f}, {:1.0f}, {:7.2f}, {:7.2f}".format( self.ROIs[nr][0], self.ROIs[nr][1], self.ROIids[nr], im1_int, tom_int )
                print(save_str, file=csv_file)

        n_landmarks = len(self.landmarks)
        im_size = (self.im1_win.im_height,self.im1_win.im_width)
        gfp = self.gfp_win.im
        tom = self.tom_win.im
        filename = os.path.splitext(self.im1_filename)[0] + "-landmarks.csv"
        print("Exporting data to: {}".format(filename))
        with open(filename, "w") as csv_file:
            print("sep=,", file=csv_file)
            print("x, y, id, gfp, tom", file=csv_file)
            for nr in range(n_rois):
                roi_mask = np.zeros(im_size, np.uint8)
                cv2.circle(roi_mask,(self.ROIs[nr][0],self.ROIs[nr][1]),ROImargin,1,thickness=-1)
                gfp_data = cv2.bitwise_and(gfp, gfp, mask=roi_mask)
                gfp_int = np.sum(gfp_data) / np.sum(roi_mask)
                tom_data = cv2.bitwise_and(tom, tom, mask=roi_mask)
                tom_int = np.sum(tom_data) / np.sum(roi_mask)
                save_str = "{:4.0f}, {:4.0f}, {:1.0f}, {:7.2f}, {:7.2f}".format( self.ROIs[nr][0], self.ROIs[nr][1], self.ROIids[nr], gfp_int, tom_int )
                print(save_str, file=csv_file)


    def about(self):
        top = tk.Toplevel()
        top.title("About this application...")
        msg = tk.Message(top, text="This little gui can display two images, in which the locations of neurons can be simultaneously annotated. These neuron-ROI's can be also deleted again. Neurons can be annotated as being double labeled (blue), GFP-only (green) and tdTomato-only (red).", width=600)
        msg.pack()
        msg = tk.Message(top, text="Manual:", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Select images: Select two images, one GFP and one tdTomato, of the same field of view.", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Add ROIs: Toggle, ROIs will appear under mouse click in any image. Text turns green when activated.", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Del ROIs: Toggle, ROIs will disappear when mouse clicked in any image. Text turns red when activated.", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Mod IDs: Toggle, the ROI identity (as displayed in color, see above) will change when mouse clicked in any image. Text turns blue when activated.", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Load ROIs: Loads ROIs from predefined file that has the same name as the GFP image, but ending on '-ROIs.npy'. (there is currently no option to use a different ROI-file name)", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Save ROIs: Saves ROIs to predefined file that has the same name as the GFP image, but ending on '-ROIs.npy'. (there is currently no option to use a different ROI-file name)", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Export: Saves ROI coordinates, ID's and mean brightness to a comma-separated values file (.csv) that has the same name as the GFP image, but ends on '-data.csv'. This file has one header row, and subsequently one row per ROI and can be easily openend in e.g. excel or using pandas.", width=600)
        msg.pack()
        msg = tk.Message(top, text="- About: Shows manual and information about version.", width=600)
        msg.pack()
        msg = tk.Message(top, text="- Quit: Ends program --without saving!!--", width=600)
        msg.pack()
        button = tk.Button(top, text="Ok", command=top.destroy)
        button.pack()

class image_window():
    """Class that runs the image windows"""

    def __init__(self, nr, main, position, im_file_name ):
        self.top = tk.Toplevel()

        # Load image from file

        title_name = os.path.basename(im_file_name)
        self.top.title(title_name)

        self.im = cv2.imread(im_file_name)
        if nr == 0:
            self.im = self.im[:,:,1]
        if nr == 1:
            self.im = self.im[:,:,1]
        if nr == 2:
            self.im = self.im[:,:,1]
        if nr == 3:
            self.im = self.im[:,:,1]
        if nr == 4:
            self.im = self.im[:,:,1]
            
        self.im = cv2.resize(self.im, ImageSize)
        self.im_height,self.im_width = self.im.shape

        self.im_file_name = im_file_name

        # Create canvas for image
        self.canvas = tk.Canvas( self.top, width=self.im_width, height=self.im_height )
        self.canvas.pack()

        # Display image on canvas for first time
        self.imgTk = ImageTk.PhotoImage( Image.fromarray(self.im) )
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.imgTk)

        # Set image window position
        self.top.update()
        x_temp = int(position['x']) + (self.top.winfo_width()*nr)
        y_temp = int(position['y'])
        self.top.geometry('+{}+{}'.format(x_temp, y_temp))

# Set up main window and start main loop
root = tk.Tk()
MainWindow(root)
root.mainloop()