# Around The World Classifier

This is a Flask webserver application. It incorporates Jupyter notebook operation and web page visualization of a deep learning - image classification topic. Via Jupyter notebooks the deep learning events and data exctration (image classification, GPS data, datetime) are processed, evaluated and documented. Image uploads, data analysis and classification results are organized and shown via web pages. Data analysis visualization is supported by Plotly plots, tables and image bags.


## What is the goal of this notebook
This notebook, has four purposes:
1. It extracts image datetimes of images (if available)
2. It extracts image GPS data (if available)
3. It provides object classification via yolo3v and ImageNet.
4. It creates an Classifcation-Meta-Data Report based on the extracted data as a Pandas DataFrame. This will be the main output for the web app.

As an example: this could be intersting if you traveled for a long time, collected thousands of images and now you want to filter out an image subset. Or maybe you want to create a funny story of your travel based on showing only images to the audience with certain objects on it (For example: "Show me only images of my **Around The World Travel** with bottles on it") 

## How is the Data collected?
- Datetimes and GPS data are extracted from the image meta data using the pillow library.
- The photo classification is realized in two different approaches:
    1. by using a yolov3 object detection algorithm. Here, I am using yolov3 pretrained weights. Deep Learning Inference with own images enables a detection of up to 80 different classes within one image. A boundary box with a class description is provided
    2. by using a convolutional neural network (CNN) based pretrained model from Torchvision via Transfer Learning. As a standard VGG16 is chosen. However, you can replace VGG16 by any other torchvision model. VGG16 is using the whole ImageNet classification system, The total number of classes is 1000. The file **data/imagenet_classes.txt** provides a dictionary of all one 1000 classes.

## How is the output of this notebook organized
- The main output is a Pandas DataFrame stored as a csv file '***images.csv***'. This DataFrame will be used by a web app called ***Around The World Classifier***. The DataFrame contains classification and meta data information of your whole image set. The web app uses this information to show the user correponding images based on his search criteria.
- In adition, the classification-Meta-Data report will be exported as an html table with thumbnail images (***filter_report.html***)
- Images detected by Yolo are stored with object boundary in a separate folder called **images_yolo**.
- Images with one or more persons detected by Yolo are addionally stored in a folder called ***images_personal***. This subset will be the base for future projects CNN based classifier projects for personal detection (see below)

- A as well as stored in an html table (**your_image_folder_name.html**).

## What will be done in the future?
In the future will be implemented:
- a GPS filter via the haversine method. This will allow you to filter images based on adjustable radial distances referred to a provided GPS location (longitude and latitude).
- a third  CNN based classifier with a layer combination of three times 'Conv-ReLU-MaxPool'. This approach should be deeply enough for sufficient feature extraction and for an appropriate image size/feature reduction. The goal of this CNN is to filter peronalized images, e.g. to identify images of yourself. However, for this classification step you have to provide a dataset of at least 500 personolized images. This CNN will be not pretrained.


## Aim of the web app
The web app provides a user inteface to enable a user an interaction with the Classification-Meta-Data Report and the image database. A user can filter out images based on his filter criteria. Filter criteria are:
    - certain time ranges
    - and/or single or multiple class objects like ('show me only images with beaches and/or persons and/or birds and/or ...').
    - geolocated ranges via radial distance from a GPS point


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
