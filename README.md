# Around The World Classifier

This is a Flask webserver application. It incorporates Jupyter notebook operation and web page visualization of a deep learning - image classification topic. Via Jupyter notebooks the deep learning events and data exctration (image classification, GPS data, datetime) are processed, evaluated and documented. Image uploads, data analysis and classification results are organized and shown via web pages. Data analysis visualization is supported by Plotly plots, tables and image bags.

## What is the goal of this project
Suppose, you collected thousands of images during a long-term travel and now you want to filter out an image subset based on datetime and/or object classification and/or GPS data. For example could create a funny story about your travel based on showing only images to the audience with certain objects on it (For example: "You want to show only images where one can find a beach a sunset or even tiny things like water bottles from June till July 2014"). For those filtering you cou could use a web app. This is the purpose of this project. 

## The web app
The web app provides a user inteface to enable a user an interaction with his image database. A user can filter out images based on his filter criteria. Filter criteria are:
    - certain time ranges
    - and/or single or multiple class objects like ('show me only images with beaches and/or persons and/or birds and/or ...').
    - geolocated ranges via radial distance from a GPS point

## In order to prepare the web app...
3 Jupyter Notebooks are necessary for the important Data Engineering/Science part

### 1_ETL_aorund_the_world_classifier.ipynb

This notebook is an ETL (Exract-Transform-Load) step, which is needed for an optimized Flask web app workflow. Its goals are: 
- It reads in images of an image dataset that you provided 
- It extracts meta data information out of each image  
- It transforms the data so that it can be used for image classification and for the web_app workflow.
- It corrects the rotation of images and by using image exif data 
- It deletes damaged images 
- It sorts images based on datetime
- it renames images to simplify image access for the web_app 
- It stores the corrected images in a new folder called ***./images***
- It creates and stores an Image Meta Data Report as a pickle file

### 2_ML_around_the_worl_classifier.ipynb
The purposes of this notebook are:
- It provides object classification via yolo3v and ImageNet.
- It creates an Classifcation-Meta-Data Report based on the extracted data as a Pandas DataFrame. The first part of this report was done in the ETL notebook before. This report will be the main output for the web app.

## How is the Data collected?
- Datetimes and GPS data are extracted from the image meta data using the pillow library in the ETL notebook (1_ETL_around_the_world_clssifier.ipynb)
- The photo classification is done in two different approaches:
    1. by using a yolov3 object detection algorithm. Here, I am using yolov3 pretrained weights. Deep Learning Inference with own images enables a detection of up to 80 different classes within one image. A boundary box with a class description is provided
    2. by using a convolutional neural network (CNN) based on a pretrained model from Torchvision via Transfer Learning. As a standard VGG16 is chosen. However, you can replace VGG16 by any other torchvision model. VGG16 is using the whole ImageNet classification system, The total number of classes is 1000. The file **data/imagenet_classes.txt** provides a dictionary of all one 1000 classes.

## How is the output of the notebooks organized
- The **output of 1_ETL_around_the_world_classifier.ipynb** is a newly created folder called ***./images***. This folder contains all your readable images, with corrected orientation (auto corrected using exif data), sorted and renamed by datetime. This folder is the source for the following image classification step and for the web app. In addition, this notebook exports the first part of the Classification-Meta-Data-Report as ***images.pkl*** with filepath, Datetime and GPS information. 
- The ***output of 2_ML_around_the_world_classifier.ipynb*** is an update of ***images.pkl*** with image classification results. In adition, the classification-Meta-Data report will be exported as an html table with thumbnail images (***filter_report.html***). Images detected by Yolo are stored with object boundary in a separate folder called **images_yolo**. Images with one or more persons detected by Yolo are addionally stored in a folder called ***images_personal***. This subset will be the base for future projects CNN based classifier projects for personal detection (see below) 
- The notebook ***3_Filter_around_the_world_classifier.ipynb*** contains filtering code for the web. This notebook contains filter tests for th web app file ***/wrangling_scripts/filter.data.py***. There is no direct output from this file which is needed for the web app.

## What is still missing and will be implemented in the future?
In the future will be implemented (***help is welcome here***):
- a GPS filter via the haversine method. This will allow you to filter images based on adjustable radial distances referred to a provided GPS location (longitude and latitude).
- a third  CNN based classifier with a layer combination of three times 'Conv-ReLU-MaxPool'. This approach should be deeply enough for sufficient feature extraction and for an appropriate image size/feature reduction. The goal of this CNN is to filter peronalized images, e.g. to identify images of yourself. However, for this classification step you have to provide a significant dataset of personolized images.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites: Installation of Python via Anaconda and Command Line Interaface
- Install [Anaconda](https://www.anaconda.com/distribution/). Install Python 3.7 - 64 Bit
- You need a Command Line Interface (CLI). If you are a Window user install [git](https://git-scm.com/)). Under Mac OS use the pre-installed Terminal.
- Upgrade Anaconda via
```
$ conda upgrade conda
$ conda upgrade --all
```

- Optional: In case of trouble add Anaconda to your system path. Write in your CLI
```
$ export PATH="/path/to/anaconda/bin:$PATH"
```
The project installation is divided into two parts: Part A describes the cloning of the project and the installation of the project environment. Part B describes Yolo weight settings for Transfer Learning, and the implementation of specific Django webserver settings.

### Project installation Part A
- Open Git Bash (Terminal, respectively)
- Change Directory to your project older, e.g. `cd my_github_projects`
- Clone the Github Project inside this folder with Git Bash (Terminal) vias:
```
$ git clone https://github.com/ddhartma/Around-The-World-Image-Classifier.git
```

- Change Directory
```
$ cd Around-The-World-Image-Classifier
```

- Create a new Python environment via the provided yml file. Inside Git Bash (Terminal) write:
```
$ conda env create -f env_windows.yml (under Windows)
$ conda env create -f env_macOS.yml (under Mac OS)
```

- Check the environment installation via
```
$ conda env list
```

- Activate the installed MTP_LSTM environment via
```
$ conda activate atw_macOS (Mac OS)
$ conda activate atw_windows
```

### Project installation Part B
- Download the [yolov3 weights](https://s3-us-west-1.amazonaws.com/udacity-aind/dog-project/dogImages.zip). Place this file in the repo-folder, at location `path/to/Around-The-World-Image-Classifier/atw_classifier/templates/data/config`.  This file contains the pretrained wheights for a yolov3 image detection with 80 classes. More details can be found [here](https://towardsdatascience.com/object-detection-and-tracking-in-pytorch-b3cf1a696a98).

- Get your [GMPAS API](https://developers.google.com/maps/documentation?hl=de)

- Put in this API in .../Around-The-World-Image-Classifier/atw_classifier/templates/layout.html in line 13 under src="ENTER YOUR GMAPS API HERE">

- Change directory to Django webserver
```
$ cd atw_classifier
```
- Apply migrations to Django webserver
```
$ python manage.py migrate
```
- Create an Admin
```
$ python manage.py createsuperuser
```
- Store your images under
```
$ .../Around-The-World-Image-Classifier/images
```

- Upload images. Click on 'UPLOAD IMAGES' in the Navigation Bar
<img src='readme_images/readme_image1.png' width=100% />


- Then click on 'UPLOAD PHOTOS'. Choose images you want to classify. For automatic rotation correction click on 'ROTATE ALL'.
<img src='readme_images/readme_image2.png' width=100% />


- Click on 'CLASSIFICATION' and click on the button 'start the Jupyter Notebook 'around_the_world_classifier.ipynb'
<img src='readme_images/readme_image3.png' width=100% />


- Run the notebook for automatic classification. If you stored your images at a diddferent place then ''.../Around-The-World-Image-Classifier/images', provide the spoecific image path under 'PART A2 PATH SETTING'.
<img src='readme_images/readme_image4.png' width=100% />


Enjoy!


## (Optionally) Accelerating the Training Process (personified image classification)

If your code is taking too long to run, you will need to either reduce the complexity of your chosen CNN architecture or switch to running your code on a GPU.  If you'd like to use a GPU, you can spin up an instance of your own:

#### Amazon Web Services

You can use Amazon Web Services to launch an [EC2 GPU instance](https://aws.amazon.com/de/ec2/). However, this service is not for free.

## Acknowledgments
* Please check out great Udacity Nanodegree programs, e.g. [Deep Learning](https://www.udacity.com/course/deep-learning-nanodegree--nd101)
