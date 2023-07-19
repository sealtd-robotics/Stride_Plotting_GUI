# ========================================================================
# Copyright (c) 2022, SEA Ltd.
# All rights reserved.

# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. 
# ========================================================================

#Import needed libraries
from math import cos, pi, sin
from itertools import count
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
import statistics
from tkinter import *
from tkinter import filedialog as fd
import tkinter as tk
import tkinter.font as font
import os
from cycler import cycler

#Create the root window for GUI
root = tk.Tk()
root.update()
root.title('STRIDE Plotting GUI')
root.resizable(False, False)
root.geometry('900x525')
root.config(bg= "white")

#Set up figure
plt.rcParams["figure.figsize"] = [10.00, 5.00]
plt.rcParams["figure.autolayout"] = True
plt.rc('axes', prop_cycle=(cycler('color', ['r', 'b', 'k', 'g','magenta','orange','c','purple','gray','brown','limegreen'])) + cycler('linestyle', ['-', '--', ':', '-.', '-', '--', ':', '-.','-', '--', ':']))  #Cycle through line colors for plotting

###Adding to GUI
#Creation of frames
my_frame = Frame(root)   #Create frame in root window
x_axis_scrollbar = Scrollbar(my_frame, orient= VERTICAL)  #Create listbox scrollbar for x variable listbox
y_frame = Frame(root) #Y variable listbox frame
y_axis_scrollbar = Scrollbar(y_frame, orient= VERTICAL)  #Scrollbar for y variable listbox
plot_button_frame = Frame(root)  #Plot button frame
csv_frame = Frame(root)  #CSV file listbox frame
csv_scrollbar = Scrollbar(csv_frame, orient= VERTICAL)    #Vertical scrollbar for csv listbox
csv_scrollbar2 = Scrollbar(csv_frame, orient= HORIZONTAL) #Horizontal scrollbar for csv listbox

#Create variable and CSV file listboxes
x_axis = Listbox(my_frame, width=25, yscrollcommand= x_axis_scrollbar.set, exportselection= 0)  #exportselection=0 allows to select from both listboxes at the same time
y_axis = Listbox(y_frame, width=25, yscrollcommand= y_axis_scrollbar.set, selectmode= MULTIPLE, exportselection= 0) 
CSV_listbox = Listbox(csv_frame,width=50, yscrollcommand = csv_scrollbar.set,selectmode= MULTIPLE, exportselection= 0)

#Configure and pack listbox scrollbars
x_axis_scrollbar.config(command= x_axis.yview) #Configure and pack scrollbars
x_axis_scrollbar.pack(side=RIGHT, fill=Y)
y_axis_scrollbar.config(command= y_axis.yview)
y_axis_scrollbar.pack(side=RIGHT, fill=Y)
csv_scrollbar.config(command = CSV_listbox.yview)
csv_scrollbar.pack(side=RIGHT, fill=Y)
csv_scrollbar2.config(command = CSV_listbox.xview)
csv_scrollbar2.pack(side=BOTTOM, fill=X)

#Place frames in window and pack listboxes
csv_frame.place(x=30, y=110) #Place frames on window
my_frame.place(x=440,y=110)
y_frame.place(x=700,y=110) 
x_axis.pack() #Pack listboxes
y_axis.pack()
CSV_listbox.pack()
folder = ''  #Make folder a global

cwd = os.getcwd()
#Default listbox to display files from current directory (same one as python script is in)
for f in os.listdir(cwd):   #For loop to look at files in selected directory and extract csv files
        name, ext = os.path.splitext(f)   #Split file name and extension
        if ext == '.csv':   #Add only csv files to listbox
            CSV_listbox.insert(tk.END, f)   #Add each csv file to listbox

#Function to allow for changing the directory
def change_directory():
    global folder #Add global folder to function
    folder = fd.askdirectory(title="Select Folder") #Open directory

    #Populate CSV file listbox
    CSV_listbox.delete(0,END)    #Clear CSV file listbox every time directory is changed
    for f in os.listdir(folder): #For loop to look at files in selected directory and extract csv files
        name, ext = os.path.splitext(f)   #Split file name and extension
        if ext == '.csv':   #Add only csv files to listbox
            CSV_listbox.insert(tk.END, f) #Add each csv file in selected directory to listbox

    x_axis.delete(0,END)  #Delete listbox values and repopulate them so user doesn't plot old data by accident
    y_axis.delete(0,END)

#Create font for buttons
myFont = font.Font(weight="bold")

#Add button for changing directory to GUI
Directory_Button = Button(root, text= "Change Directory", width=15, height=3, command= change_directory)
Directory_Button['font'] = myFont
Directory_Button.place(x=75,y=425)

#Read in selected csv files
def return_values():
        values = [CSV_listbox.get(idx) for idx in CSV_listbox.curselection()] #Get list of names of each selected item in csv
        dict_list = [] #Initialize list of dictionaries for plotting/subplotting
        for item in values: #Access each element of the values list
            join_path = os.path.join(folder, item)   #Put directory and filename together with slash inbetween
            Read_file = pd.read_csv(join_path)  #Read in full path of file

            ### Pass each column of csv into its own variable
            #Time and status variables
            time_milli = Read_file["utc_time(ms)"] 
            time_milli = time_milli - time_milli[1]   #Convert time into seconds
            time = time_milli / 1000

            #Location Variables
            latitude = Read_file["latitude(deg)"]
            longitude = Read_file["longitude(deg)"]
            cross_track_error = Read_file["cte(m)"]
            adj_rpm_l = Read_file["adj_rpm_L"]
            adj_rpm_r = Read_file["adj_rpm_R"]
            heading = Read_file["heading(deg)"]
            altitude = Read_file["altitude(m)"]
            RTK_status= Read_file["RTK_status"]
            gnss_satellites = Read_file["gnss_satellites"]
            diff_age = Read_file["diff_age(ms)"]
        
            #Velocities
            east_vel = Read_file["vel_east(m/s)"]
            north_vel = Read_file["vel_north(m/s)"]
            vel_z = Read_file["vel_z(m/s)"]
            vel_lateral = Read_file["vel_lateral(m/s)"]
            vel_longitudinal = Read_file["vel_forward(m/s)"]

            #Roll Pitch Yaw
            roll = Read_file["roll(deg)"]
            pitch = Read_file["pitch(deg)"]
            yaw_rate = Read_file["yaw_rate(rad/s)"]

            #Accelerations
            accel_x = Read_file["Ax(g)"]
            accel_y = Read_file["Ay(g)"]
            accel_z = Read_file["Az(g)"]

            #Desired vs actual values
            desired_omega = Read_file["desired_omega(rad/s)"]
            desired_vel = Read_file["desired_velocity(m/s)"]
            actual_RPM_RL = Read_file["actual_rpm_RL"]
            desired_RPM_RL = Read_file["desired_rpm_RL"]
            actual_RPM_RR = Read_file["actual_rpm_RR"]
            desired_RPM_RR = Read_file["desired_rpm_RR"]
            actual_RPM_FL = Read_file["actual_rpm_FL"]
            desired_RPM_FL = Read_file["desired_rpm_FL"]
            actual_RPM_FR= Read_file["actual_rpm_FR"]
            desired_RPM_FR = Read_file["desired_rpm_FR"]

            #Currents
            I_RL = Read_file["actual_current_RL(A)"]
            I_RR = Read_file["actual_current_RR(A)"]
            I_FL = Read_file["actual_current_FL(A)"]
            I_FR = Read_file["actual_current_FR(A)"]
            I_total = I_RL + I_RR + I_FL + I_FR  #Total current

            #Winding Temperatures
            wind_temp_RL = Read_file["winding_temp_RL(F)"]
            wind_temp_RR = Read_file["winding_temp_RR(F)"]
            wind_temp_FL = Read_file["winding_temp_FL(F)"]
            wind_temp_FR = Read_file["winding_temp_FR(F)"]

            #Motor Controller Error Words
            motor_error_code_RL = Read_file["error_code_RL"]
            motor_error_code_RR = Read_file["error_code_RR"]
            motor_error_code_FL = Read_file["error_code_FL"]
            motor_error_code_FR = Read_file["error_code_FR"]

            #Battery and robot temps/voltage
            bat_voltage = Read_file["battery_voltage(V)"]
            bat_temp = Read_file["battery_temp(F)"]
            robot_temp = Read_file["robot_temp(F)"]

            #Subject Vehicle Variables
            vehicle_speed = Read_file["vehicle_speed(m/s)"]
            vehicle_latitude = Read_file["vehicle_latitude(deg)"]
            vehicle_longitude = Read_file["vehicle_longitude(deg)"]
            vehicle_heading = Read_file["vehicle_heading(deg)"]

            #Brake Variables
            brake_command = Read_file["brake_command"]
            brake_status = Read_file["brake_status"]
            Left_Brake_fullyseated = Read_file["Left_Brake_fullyseated"]
            Right_Brake_fullyseated = Read_file["Right_Brake_fullyseated"]
            disable_motors = Read_file["disable_motors"]

            #Lateral Acceleration for IMU and V*YawRate
            east_vel_squared = np.square(east_vel) #Compute square velocities for north and south
            north_vel_squared = np.square(north_vel)
            velocity = np.sqrt(east_vel_squared + north_vel_squared) #Get magnitude of velocity
            yaw_rate_deg = yaw_rate * 180/pi  #Convert yaw rate to degrees
            omega_actual = -yaw_rate

            #GPS and wheel speed plot variables (RL, RR, FL, FR)
            rwheel = 22/1000 #Wheel radius
            vel_RL = actual_RPM_RL * 2 * pi /60 * rwheel  #Compute wheel velocities using rpm and wheel radius
            vel_RR = actual_RPM_RR * 2 * pi /60 * rwheel
            vel_FL = actual_RPM_FL * 2 * pi /60 * rwheel
            vel_FR = actual_RPM_FR * 2 * pi /60 * rwheel
            
            #Create a dictionary for x and y axis variables
            var_dict = {
            'Time (sec)':time, 
            "GNSS Satellites ": gnss_satellites, "Differential age (ms)":diff_age, "RTK Status": RTK_status, 
            "Latitude (deg)":latitude, "Longitude (deg)":longitude, "Altitude (m)": altitude,
            "Forward Velocity (m/s)":vel_longitudinal, "Lateral Velocity (m/s)": vel_lateral, "Velocity Magnitude (m/s)":velocity, 
            "East Velocity (m/s)":east_vel, "North Velocity (m/s)":north_vel, "Z-Direction Velocity (m/s)": vel_z,
            "Heading (deg)": heading, "Roll (deg)": roll, "Pitch (deg)": pitch, 
            "Ax (g)":accel_x, "Ay (g)":accel_y, "Az (g)": accel_z, "Yaw Rate (rad/s)": yaw_rate, "Yaw Rate (deg/s)": yaw_rate_deg, 
            "Cross Track Error (m)":cross_track_error,
            "Desired Omega (rad/s)":desired_omega, "Actual Omega (rad/s)": omega_actual, "Desired Velocity (m/s)": desired_vel, 
            "Velocity RL (m/s)":vel_RL, "Velocity RR (m/s)": vel_RR, "Velocity FL (m/s)": vel_FL, "Velocity FR (m/s)": vel_FR, 
            "Desired RPM RL":desired_RPM_RL, "Actual RPM RL":actual_RPM_RL, "Desired RPM RR":desired_RPM_RR, "Actual RPM RR":actual_RPM_RR, 
            "Desired RPM FL":desired_RPM_FL, "Actual RPM FL":actual_RPM_FL,"Desired RPM FR":desired_RPM_FR, "Actual RPM FR":actual_RPM_FR, 
            "Left Wheel RPM adj": adj_rpm_l, "Right Wheel RPM adj": adj_rpm_r, 
            "Actual Current RL (A)": I_RL,"Actual Current RR (A)":I_RR, "Actual Current FL (A)":I_FL, "Actual Current FR (A)":I_FR, "Total Current (A)": I_total, 
            "Winding Temp RL (F)":wind_temp_RL, "Winding Temp RR (F)":wind_temp_RR, "Winding Temp FL (F)":wind_temp_FL, "Winding Temp FR (F)":wind_temp_FR, 
            "Error_Word_RL": motor_error_code_RL, "Error_Word_RR": motor_error_code_RR, "Error_Word_FL": motor_error_code_FL, "Error_Word_FR": motor_error_code_FR,
            "Battery Voltage (V)": bat_voltage, "Battery Temp (F)":bat_temp, "Robot Temp (F)":robot_temp, 
            "Vehicle Speed (m/s)": vehicle_speed, "Vehicle Latitude (deg)": vehicle_latitude, "Vehicle Longitude (deg)": vehicle_longitude, "Vehicle Heading (deg)": vehicle_heading,
            "Brake Command":brake_command, "Brake Status":brake_status, 
            "Left Brake Fullyseated":Left_Brake_fullyseated, "Right Brake Fullyseated":Right_Brake_fullyseated, "Disable Motors":disable_motors }
           
            #For loop for adding variables to each listbox
            x_axis.delete(0,END)  #Delete listbox values and repopulate them so read csv button doesn't duplicate listbox entries
            y_axis.delete(0,END)
            for item in var_dict: #For loop to populate x and y var listboxes
                x_axis.insert(END, item) #Populate x axis listbox
                y_axis.insert(END, item) #Populate y axis listbox  
            keys_list = list(var_dict)   #Get list of keys from variable dictionary

            x_axis.select_set(0) #Select time in x_axis listbox by default
            dict_list.append(var_dict)  #Append the dictionary to a new spot in the dictionary list for each selected csv

            #Function to plot selected variables
            def select_vars(): #Function to plot selected variables
                #Loop through list of dictionaries to plot for each csv
                count = 0
                for dictionary in dict_list:
                    for item in x_axis.curselection(): #For selected items from x_axis listbox
                        keys = keys_list[item]         #Get key string
                        x_value = (dictionary[keys])   #Use key to get dict value
                        plt.xlabel(keys)
        
                    for item in y_axis.curselection(): #For selected items from y_axis listbox
                        keys = keys_list[item]         #Get key string
                        y_value = (dictionary[keys])   #Use key to get dict value
                        remove_extension = os.path.splitext(values[count])[0]  #Split extension from csv file name
                        plt.plot(x_value, y_value, label = remove_extension + "\n" + '*' + keys)  #Create Plot with csv filename and y_value labels
                    count = count + 1

                #Show plot
                plt.legend(bbox_to_anchor=(1.04,1), loc= "upper left") #Set legend to be outside of plot
                plt.grid(True) #Add plot grid
                plt.show() #Show plots           

            def select_txt_file():
                pd.set_option('display.float_format', '{:.17f}'.format)  #Keep 17 decimal places like .txt file has
                folder2 = fd.askdirectory(title="Select TXT File's Folder") #Open directory
                filepath2 = fd.askopenfilename(title = "Select a TXT file",filetypes = (("TXT Files","*.txt"),))  #Get user to open the txt file
                Filename_txt = os.path.basename(filepath2)  #Get file name from file path
                join_path2 = os.path.join(folder2, Filename_txt) 
                
                with open(join_path2) as Path_file:
                    new_data = np.loadtxt(Path_file, skiprows=1)  #Skip header row of file
                Mlat = new_data[:,0]   #Assign 1st column of data into variable
                Mlong = new_data[:,1]  #Assign 2nd column of data into variable

                count = 0
                for _ in CSV_listbox.curselection():
                    csv_name = values[count]
                    path_dict = dict_list[count]
                    latitude_path = path_dict.get("Latitude (deg)")
                    longitude_path = path_dict.get("Longitude (deg)")
                
                    #Create variables to plot actual and desired path variables
                    RefLat = Mlat[0]    #Set reference value equal to first latitude value of desired path
                    RefLong = Mlong[0]  #Set reference value equal to first longitude value of desired path
                        
                    def func_LL2NE(RefLat,RefLong, latitude, longitude): #Some conversion formula obtained from GeneSys documentation
                        e = 0.0818191908426; #Some constant
                        R = 6378137; #Some constant

                        #Scale factor for longitude (deg) to East (m)
                        Efactor = cos(RefLat*pi/180)*pi/180*R/ np.sqrt(1-np.square((sin(RefLat*pi/180)))* e ** 2)
                        #Scale factor for latitude (deg) to North (m)
                        Nfactor = (1-e**2)*R/((1-(np.square(sin(RefLat*pi/180))*e**2))*np.sqrt(1-(np.square(sin(RefLat*pi/180))*e**2)))*pi/180

                        col1 = Efactor * (longitude - RefLong)  #Apply east scale factor and put into column variable
                        col2 = Nfactor * (latitude - RefLat)    #Apply north scale factor and put into column variable
                        return col1, col2   #Return values from each column as their own variable

                    #Plot actual and desired path
                    East, North = func_LL2NE(RefLat, RefLong, latitude_path, longitude_path) #Call function to apply scale factors to actual latitude/longitude
                    M_East, M_North = func_LL2NE(RefLat, RefLong, Mlat, Mlong) #Call function to apply scale factors to desired latitude/longitude
                    plt.figure()
                    plt.plot(East, North, label= 'Actual')   #Make desired plot
                    plt.plot(M_East, M_North, label= 'Desired')
                    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(5))   #Set x_axis tick mark step to 5
                    plt.gca().yaxis.set_major_locator(plt.MultipleLocator(5))   #Set y_axis tick mark step to 5
                    plt.gca().set_aspect("equal") #Set aspect ratio for plot axes equal to make path look like it does in real life
                    plt.title('Actual vs Desired Path of %s' % csv_name)        #Plot labels
                    plt.xlabel('East (m)')
                    plt.ylabel('North (m)')
                    plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")       #Set legend to be outside of plot
                    plt.grid(True)
                    count = count + 1

                plt.show()

            #Function to allow for subplotting
            def make_subplot():
                count = 0
                for dictionary in dict_list:
                    for item in x_axis.curselection(): #For selected items from x_axis listbox
                        keys = keys_list[item]         #Get key string
                        x_value = (dictionary[keys])   #Use key to get dict values
                    i=1
                    for item in y_axis.curselection(): #For selected items from y_axis listbox
                        keys = keys_list[item]         #Get key string
                        y_value = (dictionary[keys])   #Use key to get dict value
                        remove_extension = os.path.splitext(values[count])[0]  #split extension from csv file name
                        plt.subplot(len(y_axis.curselection()),1,i)
                        plt.plot(x_value, y_value, label= remove_extension + "\n" + "*" + keys)
                        plt.ylabel(keys)
                        plt.legend(bbox_to_anchor=(1.04,1), loc="upper left")
                        plt.grid(True)
                        i += 1
                    for item in x_axis.curselection():
                        keys = keys_list[item]   #Get key string
                        plt.xlabel(keys)
                    count = count +1

                plt.show()

            #Function to filter data by clicking button
            def Filter_data():
                for dictionary in dict_list:
                    for item in x_axis.curselection() and y_axis.curselection(): #Filter items selected in x and y listboxes
                        keys = keys_list[item]       #Get key string
                        value = (dictionary[keys])   #Use key to get dict value

                        #Filtering parameters
                        dt = statistics.mode(np.diff(time)) #Compute mode of all delta t values
                        Fs = 1/dt                           #Use mode to compute frequency
                        b, a = signal.butter(4, 10/(Fs/2))   #Butterworth filter
                        var_filtered = signal.filtfilt(b, a, value)   #Filter Each value selected from x/y listboxes
                        dictionary[keys]=var_filtered   #Replace dictionary values for each key filter

            #Adding more buttons to GUI at specific locations
            Plot_button = Button(root, text="Plot Y vs X", width=15, height=3, command= select_vars)
            TxT_File_Button = Button(root, text="Select/Plot Path", width=15, height=3, command= select_txt_file)
            Subplot_Button = Button(root, text= "Subplot Y vs X", width=15, height=3, command= make_subplot)
            Filter_Button = Button(root, text= "Filter", width=15, height=3, command= Filter_data)
            Plot_button['font'] = myFont
            TxT_File_Button['font'] = myFont
            Subplot_Button['font'] = myFont
            Filter_Button['font'] = myFont
            Plot_button.place(x=475, y=375)
            TxT_File_Button.place(x=275,y=375)
            Subplot_Button.place(x=675,y=325)
            Filter_Button.place(x=675,y= 425)

#Add text boxes above listboxes
message1 = "Select X Axis Variable"   #Message above x variables
message2 = "Select Y Axis Variables"  #Message above y variables
message3 = "Select CSV Files" #Message above csv files
text_box_1 = Text(root,height=1,width=25,borderwidth=0) #Set textbox properties
text_box_1.place(x=437,y=90)  #Place textbox on tkinter window above x axis listbox
text_box_1.insert('end', message1)  #Insert message to textbox
text_box_1.config(state='disabled') #Make textbox uneditable
text_box_2 = Text(root,height=1,width=25,borderwidth=0) #Repeat commands for placing text above y variable listbox
text_box_2.place(x=693,y=90)
text_box_2.insert('end', message2)
text_box_2.config(state='disabled')
text_box_3 = Text(root,height=1,width=25,borderwidth=0) #Repeat commands for placing text above y variable listbox
text_box_3.place(x=120,y=90)
text_box_3.insert('end', message3)
text_box_3.config(state='disabled')

#Add button for reading csv file into program
return_val_but = Button(root, text= "Read CSV", width=15, height=3, command= return_values)
return_val_but['font'] = myFont
return_val_but.place(x=75,y=325)

#Run the GUI
root.mainloop()