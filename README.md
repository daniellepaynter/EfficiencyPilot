efficiency_pilot 
==============================
### Repository used for the "efficiency pilot" experiment, as part of the TTT project.
This repo contains: notebooks (currently not used), reports (contains 'figures' folder, and may contain other overviews/reports/summaries in the future), and src (contains code used to process data and produce figures).
There is also an 


### eff_landmark_picker
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

When all windows are open, click toggle button 'Add landmarks'. It will turn green.

Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── interim        <- Intermediate data that has been transformed; not currently used.
    │   ├── processed      <- Frame averages, smoothed images, z-projections, etc.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── notebooks          <- Jupyter notebooks (empty for now)
    │
    ├── references         <- Notes from literature, etc.
    │
    ├── reports            <- Overviews of the 2P structural data, as PDFs and .ai files.
    │   └── figures        <- Generated graphics and figures (currently unused)
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
        ├── __init__.py    <- Makes src a Python module
        │
        ├── data           <- Scripts to work with 2P structural data 
        │
        └── visualization  <- Scripts to create exploratory and results oriented visualizations
            └── visualize.py
    

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
