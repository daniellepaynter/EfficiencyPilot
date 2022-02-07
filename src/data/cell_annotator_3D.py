# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 2019
@author: pgoltstein
"""
# Important Settings
# im_title should be mouse name, loc name, and one or both dates of imaging
im_title = 'DP_220429_loc1_210527_210602'
# Set data type: either "two_chans" or "two_times"
data_type = "two_times"

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
list_ims = []

# List to hold variables needed to run the canvas.create_oval command in the update_im function.
# This variable will be overwritten as an empty list, if "Load_ROIs" is used.




class MainWindow():
    """Class that runs the main options window"""

    def __init__(self, main):
        self.main = main

        # ROI container
        self.ROIs = []
        self.ROIids = []
        self.gfp_ROIhandles = []
        self.tom_ROIhandles = []
        self.rgb_ROIhandles = []
        self.adding_rois = False
        self.deleting_rois = False
        self.modifying_ids = False
        self.roi_data = []
        
        # Create load and save buttons
        self.main.title("TTT 2P image annotation")
        self.button_load = tk.Button( self.main, text="Select directories", fg="black", command=self.select_dirs )
        self.button_load.pack()


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

    def select_dirs(self):
        gfp_dir = filedialog.askdirectory()
        tom_dir = filedialog.askdirectory()
        
        self.gfp_dirname = gfp_dir
        self.tom_dirname = tom_dir
        
        self.gfp_win = image_window( 0, self.main, self.main_position, self.gfp_dirname )
        self.tom_win = image_window( 1, self.main, self.main_position, self.tom_dirname )
        self.rgb_win = image_window( 2, self.main, self.main_position, "RGB image", [self.tom_win.planes_list,self.gfp_win.planes_list] )
        self.gfp_win.top.bind( "<Button-1>", self.edit_rois )
        self.tom_win.top.bind( "<Button-1>", self.edit_rois )
        self.rgb_win.top.bind( "<Button-1>", self.edit_rois )
        
        list_ims.append(self.gfp_win)
        list_ims.append(self.tom_win)
        list_ims.append(self.rgb_win)

    def edit_rois(self, event):
        if self.adding_rois:
            if self.find_closeby_roi(event.x, event.y, self.rgb_win.z_slider.get()) is None:
                z = self.rgb_win.z_slider.get()
                self.ROIs.append( [event.x, event.y, z] )
                x1, y1 = ( event.x - ROImargin ), ( event.y - ROImargin )
                x2, y2 = ( event.x + ROImargin ), ( event.y + ROImargin )
                
                # Find ID
                im_size = (self.gfp_win.im_height,self.gfp_win.im_width)
                roi_mask = np.zeros(im_size, np.uint8)
                cv2.circle(roi_mask,(event.x,event.y),ROImargin,1,thickness=-1)
                gfp_data = cv2.bitwise_and(self.gfp_win.im, self.gfp_win.im, mask=roi_mask)
                gfp_int = np.sum(gfp_data) / np.sum(roi_mask)
                tom_data = cv2.bitwise_and(self.tom_win.im, self.tom_win.im, mask=roi_mask)
                tom_int = np.sum(tom_data) / np.sum(roi_mask)
                if tom_int / gfp_int > ROIid_ratio:
                    self.ROIids.append(1)
                    ROIid = 1
                elif gfp_int / tom_int > ROIid_ratio:
                    self.ROIids.append(2)
                    ROIid = 2
                else:
                    self.ROIids.append(0)
                    ROIid = 0
                    
                self.roi_data.append(  [x1, y1, x2, y2, z, ROIid]  )
                
                self.gfp_ROIhandles.append( self.gfp_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
                self.tom_ROIhandles.append( self.tom_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
                self.rgb_ROIhandles.append( self.rgb_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
        if self.deleting_rois:
            nr = self.find_closeby_roi(event.x, event.y, self.rgb_win.z_slider.get())
            if nr is not None:
                self.gfp_win.canvas.delete(self.gfp_ROIhandles[nr])
                self.tom_win.canvas.delete(self.tom_ROIhandles[nr])
                self.rgb_win.canvas.delete(self.rgb_ROIhandles[nr])
                del self.ROIs[nr]
                del self.ROIids[nr]
                del self.gfp_ROIhandles[nr]
                del self.tom_ROIhandles[nr]
                del self.rgb_ROIhandles[nr]
                del self.roi_data[nr]
                update_im(self.rgb_win.z_slider.get())
        if self.modifying_ids:
            nr = self.find_closeby_roi(event.x, event.y, self.rgb_win.z_slider.get())
            if nr is not None:
                self.ROIids[nr] = np.mod(self.ROIids[nr]+1,3)
                self.gfp_win.canvas.delete(self.gfp_ROIhandles[nr])
                self.tom_win.canvas.delete(self.tom_ROIhandles[nr])
                self.rgb_win.canvas.delete(self.rgb_ROIhandles[nr])
                z = self.rgb_win.z_slider.get()
                x1, y1 = ( self.ROIs[nr][0] - ROImargin ), ( self.ROIs[nr][1] - ROImargin )
                x2, y2 = ( self.ROIs[nr][0] + ROImargin ), ( self.ROIs[nr][1] + ROImargin )
                self.gfp_ROIhandles[nr] = ( self.gfp_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )
                self.tom_ROIhandles[nr] = ( self.tom_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )
                self.rgb_ROIhandles[nr] = ( self.rgb_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[nr]], width=ROIthickness ) )
                self.roi_data[nr] =([x1, y1, x2, y2, z, self.ROIids[nr]])
                    
    def find_closeby_roi(self, x, y, z):
        for nr,(_x,_y,_z) in enumerate(self.ROIs):
            if abs(_x-x)<ROImargin and abs(_y-y)<ROImargin and abs(_z-z)<4:
                return nr
        return None

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

    def load_rois(self):
        filename = filedialog.askopenfilename()
        print("Loading ROIs from: {}".format(filename))
        data_mat = np.load(filename, allow_pickle=True).item()["roidata"]
        n_rois = data_mat.shape[0]
        for nr in range(n_rois):
            x = int(data_mat[nr,0])
            y = int(data_mat[nr,1])
            z = int(data_mat[nr,3])
            roi_id = int(data_mat[nr,2])
            self.ROIs.append( [x, y, z] )
            x1, y1 = ( x - ROImargin ), ( y - ROImargin )
            x2, y2 = ( x + ROImargin ), ( y + ROImargin )
            self.ROIids.append(roi_id)
            self.gfp_ROIhandles.append( self.gfp_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            self.tom_ROIhandles.append( self.tom_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            self.rgb_ROIhandles.append( self.rgb_win.canvas.create_oval( x1, y1, x2, y2, outline=IDcolors[self.ROIids[-1]], width=ROIthickness ) )
            self.roi_data.append([x1, y1, x2, y2, z, roi_id])

    def save_rois(self):
        n_rois = len(self.ROIs)
        data_mat = np.zeros((n_rois,4))
        for nr in range(n_rois):
            data_mat[nr,0] = self.ROIs[nr][0]
            data_mat[nr,1] = self.ROIs[nr][1]
            data_mat[nr,3] = self.ROIs[nr][2]
            data_mat[nr,2] = self.ROIids[nr]
        data_dict = { "roidata": data_mat}
        filename = os.path.join(os.path.commonpath([self.gfp_dirname, self.tom_dirname]),  im_title + "_ROIs.npy")
        print("Saving ROIs to: {}".format(filename))
        np.save(filename,data_dict)

    def export_data(self):
        n_rois = len(self.ROIs)
        im_size = (self.gfp_win.im_height,self.gfp_win.im_width)
        gfp = self.gfp_win.im
        tom = self.tom_win.im
        if data_type == "two_chans":
            filename = os.path.join(os.path.commonpath([self.gfp_dirname, self.tom_dirname]), im_title + "_two_chan_data.csv")
        elif data_type == "two_times":
            filename = os.path.join(os.path.commonpath([self.gfp_dirname, self.tom_dirname]),  im_title +"_two_times_data.csv")
        else:
            filename = os.path.join(os.path.commonpath([self.gfp_dirname, self.tom_dirname]),  im_title +"_data.csv")
        print("Exporting data to: {}".format(filename))
        with open(filename, "w") as csv_file:
            print("sep=,", file=csv_file)
            print("x,y,z,id,gfp,tom", file=csv_file)
            for nr in range(n_rois):
                roi_mask = np.zeros(im_size, np.uint8)
                cv2.circle(roi_mask,(self.ROIs[nr][0],self.ROIs[nr][1]),ROImargin,1,thickness=-1)
                gfp_data = cv2.bitwise_and(gfp, gfp, mask=roi_mask)
                gfp_int = np.sum(gfp_data) / np.sum(roi_mask)
                tom_data = cv2.bitwise_and(tom, tom, mask=roi_mask)
                tom_int = np.sum(tom_data) / np.sum(roi_mask)
                save_str = "{:4.0f}, {:4.0f}, {:1.0f}, {}, {:7.2f}, {:7.2f}".format( self.ROIs[nr][0], self.ROIs[nr][1], self.ROIs[nr][2], self.ROIids[nr], gfp_int, tom_int )
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

    def __init__(self, nr, main, position, im_dir, gfp_tom_data=None ):
        self.top = tk.Toplevel()

        # Load image from file
        if gfp_tom_data is None:
            title_name = im_title
            self.top.title(title_name)

            # Load image and get meta_data
            self.planes_list = []
            for it, filename in enumerate(os.listdir(im_dir)):
                if filename.endswith('.tif'):
                        im = cv2.imread(os.path.join(im_dir, filename))
                        im = im[:, :, 1]
                        self.planes_list.append(im)
            
            self.top = tk.Toplevel()
            self.top.title(str(nr))
                        
            # Set starting image
            self.im = self.planes_list[0]
            self.im = cv2.resize(self.im, ImageSize)
            self.im_height, self.im_width = self.im.shape[:2]

        # Construct image from gfp_tom_data
        else:
            self.top.title(im_title + "Merge")
            self.planes_list = []
            for it, plane in enumerate(gfp_tom_data[0]):
            
                self.im = np.zeros( (gfp_tom_data[0][0].shape[0], gfp_tom_data[0][0].shape[1], 3), np.uint8)
                self.im[:,:,0] = gfp_tom_data[0][it]
                self.im[:,:,1] = gfp_tom_data[1][it]
                self.im_height, self.im_width = self.im.shape[:2]
                self.planes_list.append(self.im)
                        
            # Set up a slider to choose which z plane to display
            self.nr_z_planes = len(self.planes_list)
            self.z_slider = tk.Scale(self.top, orient='horizontal', resolution=1, length=ImageSize[1], from_=0,
                                         to=self.nr_z_planes - 1,
                                         command=update_im)
            self.z_slider.pack()                 
        self.im_file_name = im_title

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
    
def update_im(val):
    for chan in list_ims:
        chan.im = chan.planes_list[int(val)]
        chan.im = cv2.resize(chan.im, ImageSize)
        chan.im_height, chan.im_width = chan.im.shape[:2]
        chan.imgTk = ImageTk.PhotoImage(Image.fromarray(chan.im))
        chan.image_on_canvas = chan.canvas.create_image(0, 0, anchor=tk.NW, image=chan.imgTk)
        chan.roi_vals = []
        for roi in range(len(mainwin.roi_data)):
            if mainwin.roi_data[roi][4] == list_ims[2].z_slider.get():
                chan.roi_vals.append(mainwin.roi_data[roi])
        for roi in chan.roi_vals:
            chan.canvas.create_oval(roi[0], roi[1], roi[2], roi[3], outline=IDcolors[roi[5]], width=ROIthickness)
        chan.top.update()


# Set up main window and start main loop
root = tk.Tk()
mainwin = MainWindow(root)
root.mainloop()