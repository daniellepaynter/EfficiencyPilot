# EfficiencyPilot
Code used to process and analyze structural 2-photon data over multiple timepoints for the "efficiency" TTT pilot experiment.

### Input file requirements:
One folder for each imaging timepoint of interest.
Within that folder should be all tiff images comprising one channel from one stack (i.e., a pre-processed tiff for each z-plane).
The code DOES NOT (currently) work with raw data input that has not been averaged over frame repeats.

### Instructions:
Code can be run from ipython in command line.   
Download code to a given directory.  
Navigate to directory where code is.  
Run iPython and enter the command 'run eff_landmark_picker'.  
First, the code asks for an input of how many timepoints to open -- enter an integer from 1 to ??? depending on how many repeated imaging sessions you'd like to see.  
After entering this, a GUI pops up. Clicking "Add image directory" opens a file dialog where you should navigate to the directory with the stack of the earliest timepoint.   
A stack will load in one window with a slider bar to move through the stack. Then, the file dialog returns, and you can select the next timepoint's directory, etc.  

When all 
