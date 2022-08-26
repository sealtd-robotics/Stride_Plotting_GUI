# Stride Plotting GUI Instructions

This file is a walkthrough for how to setup and run the GUI for plotting Stride data.

Setup
---
Requirements for Machine: Windows or Linux with Python 3 and Anaconda installed

In a new terminal, follow the steps below:
1. Create and activate an environment in which the code will run, with the following commands: 

```
 conda create --name myenv
 conda activate myenv
```
where `myenv` is the desired name of the environment. 

* Note: If there are multiple versions of Python installed on the computer, it is possible to specify which version of python to use in the environment by adding python=version to the environment creation command.  
* Ex) `conda create --name myenv python=3.6`.


2. Install the following libraries one at a time with the commands below:
  
```
conda install pandas
pip install matplotlib
pip install scipy
```

Running the Program
---
To run the program from the environment run the following lines: 
```
cd script_directory
python Stride_Plotting_GUI.py
```
The script_directory is the path of the folder containing Stride_Plotting_GUI.py. The GUI window should pop up. 
* Ex) `cd C:\Stride\Python\Stride_Plotting_GUI`.

Using the GUI
---
The GUI will initially pop up showing 3 empty listboxes(labeled Select CSV Files, Select X axis variables, and Select Y axis variables) and 2 buttons (labeled 'Change Directory' and 'Read CSV').

1. First, click the 'Change Directory' button. This will then prompt you to select the folder containing the CSV file(s) in which to get data from. Once the desired folder has been selected, click the confirmation button (could be 'select folder', 'open', 'ok', etc.). 
<br/>

2. The CSV listbox will be populated with the names of each CSV file in the selected folder. Click on the CSV file(s) of interest, and then click the 'Read CSV' button.

* Note: Repeat step 1 to choose a new directory. The X and Y variable listboxes values will clear until step 2 is repeated. To look at different files in the same directory, simply select/deselect them from the CSV listbox and click 'Read CSV' again. This will also reset the X and Y variable listbox selections. 

3. The X and Y variable listboxes will now be populated with the variable names from the CSV files. Four more buttons will also pop up (Select/Plot Path, Plot Y vs X, and Subplot Y vs X, and Filter).
<br/>

4. To plot or subplot data, select the desired x- and y-axis variables from the corresponding listboxes. The 'X Axis Variable' listbox allows one selection at a time, with the default selection being 'Time (sec)'. The 'Y Axis Variable' listbox allows the selection of as many variables as desired. Each selected variable in this listbox will be highlighted and clicking a variable again will deselect it.  
<br/>

5. Once the variables desired to plot have been selected, click the 'Plot Y vs X' button to see everything on one graph, or the 'Subplot Y vs X' button to see each selected variable as its own subplot. In each case a figure will pop up. The window should look something like the picture below. 

* Note: Close the figure after viewing it to resume using the GUI.

6. To apply a filter to the selected data before plotting, click the 'Filter' button and then plot/subplot as normal. This will update the values of items selected in the listbox. If an item from the listbox is deselected, the variable will remain filtered even if it is later reselected. To remove the filter from the data, click 'Read CSV' again and reselect listbox values. 
<br/> 

7. To plot the Desired and Actual path of STRIDE, click the 'Select/Plot Path' button. Select the folder containing the path file (.txt) in the same way a folder was selected in Step 1. A window will appear with the .txt files in the folder. Click the desired file and then press 'Open' (or double click the .txt file). A plot will automatically pop up in a new window for each CSV.  

* Note 1: If using Linux, the directory selected in the first window may not carry over to the second window. In this case, make sure to navigate to the directory again to select the .txt file.  
<br/>

* Note 2: When finished viewing the figures, close them to resume using the GUI. 

Looking at Plots
---
The 'Select/Plot Path', 'Plot Y vs X', and 'Subplot Y vs X' buttons all use 'Matplotlib' interactive plots to show data. Hovering the cursor over an icon will display text which describes its function, but they are also described below: 

- Clicking the home button will reset the view of the plot to its original view.
<br/>

- The left and right arrow keys will scroll through the different views of the plot which have been used.  
    *  Ex) If the plot has been zoomed in on, click the left arrow to zoom back out and then click the right arrow to zoom back in again.
<br/>

- The 4-way arrow will allow panning or zooming in/out of the figure. Once this icon is selected, left click and drag to pan and right click and drag to zoom. 
<br/>

- The magnifying glass will allow a rectangle to be drawn which zooms into the plot. Once the icon is selected, Left click and drag on the plot to create a rectangle on which to zoom into. 
<br/>

- The Slider icon will configure options for subplots, such as borders and spacing. 
<br/>

- The line graph icon will allow the selection of several axis and curve parameters, such as axis start and end values, labels, scale, line styles, and markers. 

    * Note1: This button does not appear on Linux (Matplotlib version 3.5.2), but does work on Windows.
    <br/>

    * Note 2: Rarely, (if plotting from multiple csv files at once) changing colors/line styles of one dataset makes other datasets swap colors and/or line styles. The GUI itself is set up to provide different colors and line styles. It is not recommended to change these in the interactive plot, as regenerating the legend may still have data labeled incorrectly. However, it is possible to change the legend entries manually, if desired. 
    <br/>

- The last button is the save button, which will save the figure.