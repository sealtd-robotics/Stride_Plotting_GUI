# Stride Plotting GUI Instructions

This file is a walkthrough for how to setup and run the GUI for plotting Stride data.

Setup
---
Requirements for Machine: Windows or Linux with Python 3 and Anaconda installed

In a new terminal, follow the steps below:
1. Create and activate an environment in which you want to run your code with the following commands:

```
 conda create --name myenv
 conda activate myenv
```
where `myenv` is the name of the environment you want. 

* Note: If you have multiple versions of Python, you can specify which versdion of python you want to use in your environment by adding `python=version` to the environemnt creation command. 
EX) `conda create --name nyenv python=3.6`.


2. Install the following libraries one at a time with the commands below:
  
```
conda install pandas
pip install matplotlib
pip install scipy
```

Running the Program
---
To run the program from your environment run the following lines: 
```
cd script_directory
python Stride_Plotting_GUI.py
```
The script_directory is the path of the folder containing Stride_Plotting_GUI.py. The GUI window should pop up. For example, `cd C:\Stride\Python\Stride_Plotting_GUI`.

Using the GUI
---
The GUI will intially pop up showing 3 empty listboxes(labeled Select CSV Files, Select X axis variables, and Select Y axis variables) and 2 buttons (labeled 'Change Directory' and 'Read CSV').

1. The first thing you will want to do is click the 'Change Directory' button. This will prompt you to select the folder containing the CSV file(s) you want to get data from. Once you have navigated to your folder, click the confirmation button(could be 'select folder', 'open', 'ok', etc.).
<br/>

2. The CSV listbox will be populated with the names of each CSV file in the selected folder. Click on the CSV file(s) you would like to look at data for, and then click the 'Read CSV' button.

* Note: Repeat step 1 to choose a new directory. The X and Y variable listboxes values will clear until you repeat step 2. To look at different files in the same directory, simply select/deselect them from the CSV listbox and click 'Read CSV' again. This will also reset your X and Y variable listbox selections.

3. You will now see the X and Y variable listboxes populate with the variable names from the CSV files. 4 more buttons will also pop up (Select/Plot Path, Plot Y vs X, and Subplot Y vs X, and Filter)
<br/>

4. To plot or subplot data, you will need to select your x and y axis variables from the corresponding listboxes. The 'X Axis Variable' listbox allows one selection at a time, with the default selection being 'Time (sec)'. The 'Y Axis Variable' listbox allows you to select as many variables as you want at a time. Each selected variable in this listbox will be highlighted, and clicking a variable again will deselect it. 
<br/>

5. Once you have selected the variables you want to plot, click the 'Plot Y vs X' button to see everything on one graph, or the 'Subplot Y vs X' button to see each selected variable as it's own subplot. In each case a figure will pop up.

* Note: When you are done with the figure, close it to resume using the GUI. 

6. If you would like to apply a filter to your selected data before plotting, then you can click the 'Filter' button and then plot/subplot as normal. This will update the values of items selected in the lisbox. If you deselect an item from the listbox, the variable will remain filtered even if reselect it. To remove the filter from the data you will need to click 'Read CSV' again and reselect listbox values. 
<br/> 

7. If you would like to plot the Desired and Actual path of STRIDE, click the 'Select/Plot Path' button. You will be prompted to select the folder containing the path file (.txt) in the same way you selected a folder in step 1. Then you should see a window with the .txt files in the folder. Click the one you want and then press 'Open' (or double click the .txt file). A plot will automatically pop up in a new window for each CSV. 

* Note 1: If you are using Linux, the directory you select in the first window may not carry over to the second window. In this case, make sure to navigate to your directory again to select your .txt file. 
<br/>

* Note 2: When you are done with the figures, close them to resume using the GUI.

Looking at Plots
---
The 'Select/Plot Path', 'Plot Y vs X', and 'Subplot Y vs X' buttons all use 'matplotlib' interactive plots to show data. You can hover your mouse over an icon to see what it does, and they are also described below:

- Clicking the home button will reset the view of the plot to its original view.
<br/>

- The left and right arrow keys will allow you scroll throught the different views of the plot you have used (For example if you have zoomed in you can click the left arrow to zoom back out and then click the right arrow to zoom back in again).
<br/>

- The 4 way arrow will allow you to pan or zoom in/out of the figure. Once this icon is selected, left click and drag to pan and right click and drag to zoom. 
<br/>

- The magnifying glass with allow you to zoom in to an area of the plot using a rectangle. Omce the icon is selected, Left click and drag on the plot to create a rectangle on where you want to zoom in.
<br/>

- The 3 lines with dots will allow you to configure options for subplots, such as borders and spacing.
<br/>

- The line graph icon will allow you to set several axis and curve paramaters, such as axis start and end values, labels, scale, line styles, and markers.
<br/>

- The last button is the save button, which will allow you to save the figure.