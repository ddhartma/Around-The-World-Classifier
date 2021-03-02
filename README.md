[image1]: assets/web_app_image.png "image1"
[image2]: assets/config_folder.png "image2"
[image3]: assets/google_api.png "image3"

# Around The World Classifier

## Outline
- [What is the goal of this project](#project_goal)
- [The web app goal](#web_app_goal)
- [The elemnts of the web app](#elements_web_app)
- [In order to prepare the web app](#prep_web_app) 
    - [1_ETL_aorund_the_world_classifier.ipynb](#1_etl)
    - [2_ML_around_the_worl_classifier.ipynb](#2_ml)
    - [3_Filter_around_the_world_classifier.ipynb](#3_filter)
- [How is the Data collected?](#data_collect)
- [How is the output of the notebooks organized](#output_organized)
- [Detailed file list description](#file_descr)
- [What is still missing and will be implemented in the future?](#still_miss)
- [Setup Instructions](#setup)
- [Acknowledgments](#Acknowledgments)
- [Further Links](#Further_Links)

## What is the goal of this project <a name="project_goal"></a>
Suppose, you collected thousands of images during a long-term travel and now you want to filter out an image subset based on datetime, image objects and GPS data. Maybe you want to tell your friends a funny story about your travel based on "showing only images with certain objects or datetime ranges". For example: You want to show only images with persons in combination with a beach at sunset from June until July 2014 and/or for a certain geolocation. Or you are only interested in images where you can see a water bottle. Such interactive image filtering is the purpose of this project. 

This is a Flask webserver application for image filtering. There are three types of filters:
- Object filtering via Deep Learning Image Classification (Yolo and ImageNet)
- Datetime Filtering 
- GPS filtering 

The idea is to provide an image database and extract meta exif data (like GPS and Datetime) from each image. In addition, image objects will be classified with pretrained neural networks. After some data cleaning and data preparation the final result (a Classification-Meta-Data Report and a prepared image data base) will be provided to a Flask web app. Now, a user can filter out single or multiple class objects and date/GPS ranges via HTML select boxes, input checkboxes, buttons and date windows etc. a certain images subset. 

The project incorporates Jupyter notebook operation with Python code for the data preparation and HTML/Javascript files - mainly based on Bootstrap - for the Flask web server.

## The web app goal <a name="web_app_goal"></a>
The web app provides a user inteface to allow an interaction with a image database. A user can filter out images based on his filter criteria. Below you can see a gif movie of the web app to get a first impression. 

[![Demo CountPages alpha](https://j.gifs.com/nxBnNl.gif)](https://j.gifs.com/nxBnNl.gif)

## The elements of the web app <a name="elements_web_app"></a>

![image1]

The main part of the web app consists of five segments. 
- ***The User Control Board***: Choose up to eight Yolo and/or ImageNet classes for which you want to filter your image database. In addition, you can reduce the amount of images by adding a date range. If you provide a GPS API KEY you can also enable a GPS MAP within the web app. If not, the GPS section will be inactive. There are four buttons:
    - ***Load Favourites***: If you had marked images with the Like button before and had saved this set you can now load your 'most wanted' images subset.
    - ***Save Favourites***: Save your favourite subset.
    - ***Export Table***: Export your actual filter setting as an HTML table. This table contains path settings, image meta data, original and Yolo thumbnail images with object boundary boxes.
    - ***Apply Filter***: With this button you submit your filter setting to the Flask web server and the database. The reponse will be a corresponding filtered image subset.
-  ***Thumbnail image gallery***: Here, your image subset will be listed as thumbnail images in a scrollable frame. By clicking on an image, the image will be shown in the image carousel below and the Google Map will be updated with repect to the actual geoloaction.
- ***Google Maps***: If you provide your private GOOGLE MAPS API KEY you can geolocate your images on the map. You can zoom in and out with a zoom slider. Furthermore, you can set a circle with a radius slider around the actual GPS location. This is useful to indicate the actual position as well as for measuring distances in meters (radial distance). 
- ***Info summary***: Image path, datetime, GPS latitude and longitude, predicted Yolo classes and predicted Imagenet classes will be shown here for the actual image.
- ***Image carousel***: This bootstrap carousel slides through your filtered image subset. There are control buttons (Prev, Play, Pause, Next) as well as a slider to adjust the carousel sliding interval. With a 'Like button' you can highlight your best-off images. 


## In order to prepare the web app... <a name="prep_web_app"></a>
3 Jupyter Notebooks are necessary for the important Data Engineering/Science part

#### 1_ETL_aorund_the_world_classifier.ipynb <a name="1_etl"></a>

This notebook is an ETL (Exract-Transform-Load) step, which is needed for an optimized Flask web app workflow. Its goals are: 
- It reads in images of an image dataset that you provided 
- It extracts meta data information out of each image  
- It transforms the data so that it can be used for image classification and for the web_app workflow.
- It corrects the rotation of images by using image exif data 
- It deletes damaged images 
- It sorts images based on datetime
- it renames images to simplify image access for the web app 
- It stores the corrected images in a new folder called ***./images***
- It creates and stores an Image-Meta-Data Report as a pickle file called ***images_meta.pkl***

#### 2_ML_around_the_worl_classifier.ipynb <a name="2_ml"></a>
The purposes of this notebook are:
- It classifies images via yolo3v and ImageNet.
- It creates an Classifcation-Meta-Data Report based on the extracted data as a Pandas DataFrame. This report will be the main input for the web app.

#### 3_Filter_around_the_world_classifier.ipynb <a name="3_filter"></a>
The purposes of this notebook are:
- Develop and test code for /web_app_atw/wranglings_scripts/filter_data.py. The file filter_data.py contains the filter functions needed for the web app.
- However, the output of this notebook is not needed for the web app.
- This notebook is just a test for filtering algorithms based on datetime and classification objects.


## How is the Data collected? <a name="data_collect"></a>
- In this repo a small image dataset (9 images) is provided as a demo. This image subset is extracted from a Kaggle image dataset: [736 geolocated Scotland images](https://www.kaggle.com/jbakerdstl/geolocated-imagery-dataset-scotland).
- Datetimes and GPS data are extracted from the image meta data using the pillow library in the ETL notebook (1_ETL_around_the_world_clssifier.ipynb)
- The photo classification is done in two different approaches:
    1. by using a ***yolov3*** object detection algorithm. Here, I am using yolov3 pretrained weights (248 MB, not in this repo, see download instructions below). Deep Learning Inference enables a detection of up to 80 different classes within one image. A boundary box with a class description is provided for each object detction within the image.
    2. by using a convolutional neural network (CNN) based on a ***pretrained model from Torchvision*** via ***Transfer Learning***. As a standard ***VGG16*** is chosen. However, you can replace VGG16 by any other torchvision model. VGG16 is using the whole ***ImageNet*** classification system, The total number of classes is 1000. The file **data/imagenet_classes.txt** provides a dictionary of all one 1000 classes.

## How is the output of the notebooks organized <a name="output_organized"></a>
- The **output of 1_ETL_around_the_world_classifier.ipynb** is stored in the folder called ***./images***. This folder contains all your (readable) images, with corrected orientation (auto corrected using exif data), sorted and renamed by datetime. This folder is the source for the following image classification step and for the web app. In addition, this notebook creates the first part of the Classification-Meta-Data-Report which is stored as a pickle file called ***images_meta.pkl***. This file contains for example the absolute filepaths to the images, datetimes and GPS information. 
- The ***output of 2_ML_around_the_world_classifier.ipynb*** is an update of ***images_meta.pkl*** with Yolo and ImageNet classification results. Those results will be concated to the dataframe of images_meta.pkl and stored as a new file called ***images.pkl***. In adition, the Classification-Meta-Data report will be exported as an html table with thumbnail images (***images.html***). Images detected by Yolo are stored with object boundaries in a separate folder called **images_yolo**. Besides that, images with one or more persons detected by Yolo are stored in a folder called ***images_personal***. This subset will be the base for future projects with CNN based classifiers for person detection.
- The notebook ***3_Filter_around_the_world_classifier.ipynb*** contains filtering code for the web app file ***/wrangling_scripts/filter.data.py***. There is no direct output from this notebook which would be needed for the web app.

## Detailed file list description <a name="file_descr"></a>

| File/folder name    | Location in repo     | Aim of file
| :------------- | :------------- | :------------- 
| run.py     |    /web_app_atw    | The main file to start the Flask web app. Use ***python run.py*** to start the web app
| settings.json | /web_app_atw | It contains YOUR PERSONAL Google Maps API key. This key is needed by the web app to visualize GPS locations via Google Maps in the web app. If you do not provide this key. The Google Maps screen will be inactive.
| like_settings.json | /web_app_atw | Dictionary containing file paths to favourite images in the web app. This file is needed for the web app. It is accessed/updated by the 'Load Favourites' and 'Save Favourites' buttons in the web app.
| env_macOS.yml | /environments | Conda environment file used for this project based on mac OS
| env_windows.yml | /environments | Conda environment file used for this project based on Windows
| /data  | /web_app_atw | Folder containing classification data (like pretrained weights), the three notebooks as well the image demo sets with Scotland images. 
| /static | /web_app_atw | Folder containing javascripts and static images needed for the web app
| /templates | /web_app_atw  | Folder containing the html files needed for the web app
| /wrangling_scripts | /web_app_atw | Folder containing the filter_data.py file which is needed for data filtering in the web app
| /data | /web_app_atw/data | Folder containing helper files needed for Yolo and Imagenet classification
| /images | /web_app_atw/data | Folder containing the images used by the web app. It is the output of 1_ETL_aorund_the_world_classifier.ipynb
| /images_personal | /web_app_atw/data | Folder containing images with persons which were detected by Yolo. This folder is part  of 2_ML_around_the_worl_classifier.ipynb outputs.
| /images_yolo | /web_app_atw/data | Folder containing images with boundary boxes created by Yolo. It is part of the outputs of 2_ML_around_the_worl_classifier.ipynb 
| /scotland_set | /web_app_atw/data | Folder containing a demo set of 9 images extracted from the Kaggle imageset with 736 geolocated Scotland images described above. 
| /utils |  /web_app_atw/data | Folder containing further helper files for Yolo detection
| 1_ETL_aorund_the_world_classifier.ipynb | /web_app_atw/data | Notebook needed for the ETL process (see above). Meta data extraction, image fixing and damged image deletion is done within this notebook.
| 2_ML_around_the_worl_classifier.ipynb | /web_app_atw/data | Notebook needed to create the Classifcation-Meta-Data Report (images.pkl). Yolo and Imagenet classification of the dataset is done in this notebook.
| 3_Filter_around_the_world_classifier.ipynb |  /web_app_atw/data | Notebook to test filtering algorithms
| filter_result.html | /web_app_atw/data | Classification-Meta-Data-Report which is created when the Button 'Export Table' is clicked in the web app. This file contains the actual image information of the image set filtered by the user.
| images.pkl | /web_app_atw/data | The data containing file used by the web app. This is the Classification-Meta-Data Report. This file is the main output of 2_ML_around_the_worl_classifier.ipynb
| images.html | /web_app_atw/data | an HTML version of images.pkl with thumbnail images and Yolo classification boundaries
| images_meta.pkl | /web_app_atw/data | The Meta-Data Report from 1_ETL_aorund_the_world_classifier.ipynb
| index.html | /web_app_atw/templates | Main HTML file of the web app 
| carousel.html | /web_app_atw/templates | HTML file containing code for the bootstrap carousel
| gps_map.html  | /web_app_atw/templates | HTML file containing code to visualize the Google GPS map
| table.html | /web_app_atw/templates | HTML file containing code for the user control board
| thumbnail.html | /web_app_atw/templates | HTML file containing code for the thumbnail gallery
| directive.js | /web_app_atw/static | Javascript file to zoom in (and out) an carousel image via mouse scroll 
| lazy_load.js | /web_app_atw/static | Javascript file needed to lazy load images into the thumbnail gallery



## What is still missing and will be implemented in the future? <a name="still_miss"></a>
In the future will be implemented:
- a GPS filter via the haversine method. This will allow you to filter images based on adjustable radial distances referred to a provided GPS location (longitude and latitude).
- a third  CNN based classifier with a layer combination of three times 'Conv-ReLU-MaxPool'. This approach should be deeply enough for sufficient feature extraction and for an appropriate image size/feature reduction. The goal of this CNN will be to filter peronalized images, e.g. to identify images of yourself. 

## Setup Instructions <a name="setup"></a>
Let's get a copy of this repo and run it on your local machine for development and testing purposes.

### Prerequisites: Installation of Python via Anaconda and Command Line Interaface
- Install [Anaconda](https://www.anaconda.com/distribution/). Install Python 3.7 - 64 Bit
- If you need a Command Line Interface (CLI) you could use [git](https://git-scm.com/) for example.
- Upgrade Anaconda via
```
$ conda upgrade conda
$ conda upgrade --all
```

- Optional: In case of trouble add Anaconda to your system path. Write in your CLI
```
$ export PATH="/path/to/anaconda/bin:$PATH"
```
The project installation is divided into two parts: 
- Part A describes how to clone this project and how to install the project environment. 
- Part B describes how to get Yolo weights and a Google Maps API Key.

### Project installation Part A
- Open your preferred CLI
- Change Directory to your project folder, e.g. `cd my_github_projects`
- Clone the Github Project inside this folder with via:
```
$ git clone https://github.com/ddhartma/Around-the-World-Classifier.git
```

- Change Directory
```
$ cd ./Around-the-World-Classifier/environments/
```

- Create a new Python environment via the provided yml file. Inside your terminal write:
```
$ conda env create -f env_macOS.yml (for Mac OS)
$ conda env create -f env_windows.yml (for Windows)
```

- Check the environment installation via
```
$ conda env list
```

- Activate the installed environment via
```
$ conda activate atw_macOS (for Mac OS)
$ conda activate atw_windows (for Windows)
```

- Add environment to Jupyter Notebook kernel list:
```
$ python -m ipykernel install --user --name=atw_macOS (for Mac OS)
$ python -m ipykernel install --user --name=atw_windows (for Windows)
```

### Project installation Part B
- Download the [yolov3 weights](https://pjreddie.com/media/files/yolov3.weights).
Place this file called ***yolov3.weights*** into the config folder, `.../web_app_atw/data/data/config/`.  This file contains the pretrained weights for a yolov3 image detection with 80 classes. More details can be found [here](https://towardsdatascience.com/object-detection-and-tracking-in-pytorch-b3cf1a696a98).
- Your config folder should contain the following files now:

    ![image2]

- Get your [GMPAS API](https://developers.google.com/maps/documentation?hl=de)
  When you start the web app paste your API key into text input on the top of the user control board. Then click on save. Your API key will be saved to ***setting.json***

    

- Change directory to the location of ***run.py*** and enter

```
$ python run.py
```

- Open your browser and enter 
```
http://0.0.0.0:3001/
```
- Now the Flask web server is active and you can start with object and date filtering

- Paste your Google Maps API Key in the input text window of the User Control board and click save.

    ![image3]

- Now you can locate image GPS data on the map.

- In order to quit the web server process ***Press CTRL+C***


## Acknowledgments <a name="Acknowledgments"></a>
* This project is part of the Udacity Nanodegree program 'Data Science'. Please check this [link](https://www.udacity.com) for more information.

## Further Links <a name="Further_Links"></a>
Git/Github
* [GitFlow](https://datasift.github.io/gitflow/IntroducingGitFlow.html)
* [A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/)
* [5 types of Git workflows](https://buddy.works/blog/5-types-of-git-workflows)

Docstrings, DRY, PEP8
* [Python Docstrings](https://www.geeksforgeeks.org/python-docstrings/)
* [DRY](https://www.youtube.com/watch?v=IGH4-ZhfVDk)
* [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

Readme
* [python-tabulate to convert pandas DataFrames to Readme tables](https://pypi.org/project/tabulate/)
