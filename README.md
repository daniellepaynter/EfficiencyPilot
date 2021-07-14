efficiency_pilot test edit
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
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
