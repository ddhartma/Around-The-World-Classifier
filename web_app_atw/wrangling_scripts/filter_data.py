import pandas as pd
import plotly.graph_objs as go

import os
import json

import ast

from PIL import Image, ImageDraw, ExifTags, ImageTk
import base64
import io
from io import StringIO, BytesIO

from IPython.display import HTML

from datetime import datetime, timedelta

# File to collect data of images to display in web app 

def load_data(path):
    """ Load pkl file with classification and meta data results
    
        INPUTS:
        ------------
            path - (string) path to classification report
        
        OUTPUTS:
        ------------
        df (pandas dataframe) dataframe containing the classification report
    """
    
    df = pd.read_pickle(path)
    try: 
        del df['Unnamed: 0']
    except:
        pass
        
    return df


def perfectEval(anonstring):
    """ Transform string elements in dataframe columns to lists via ast module
        
        INPUTS:
        ------------
            anonstring - (string) a string in the form "['elmt1', 'elmt2', 'elmt2', ...]" 
                         which should be transformed  to a list as ['elmt1', 'elmt2', 'elmt2', ...]
        
        OUTPUTS:
        ------------
            ev (list) - a list transformation of the input string
    """
    try:
        ev = ast.literal_eval(anonstring)
        return ev
    except ValueError:
        corrected = "\'" + str(anonstring) + "\'"
        ev = ast.literal_eval(corrected)
        return ev

def get_yolo_and_imagenet_lists(path):
    """ Extract Yolo lists and ImageNet classification lists from the Classification-Meta-Data report.
        Those lists are needed for web app select menus and for displaying filter results
        
        INPUTS:
        ------------
            path - (string) path to classification report
        
        OUTPUTS:
        ------------
            df - (pandas dataframe) of the classification report
            yolo_flat_list - (list) of all in df observed Yolo classes
            imageNet_flat_list - (list) of all in df observed ImageNet classes
            
    """
    
    df = load_data(path)
    # yolo classifications
    yolo_list = df['classes_yolo'].tolist()
    yolo_flat_list = [item for sublist in yolo_list for item in sublist]
    yolo_flat_list = list(set(yolo_flat_list))
    #print('yolo_flat_list', yolo_flat_list)
    
    # ImageNet classifications
    imageNet_list = df['classes_ImgNet'].tolist()
    imageNet_flat_list = [item for sublist in imageNet_list for item in sublist]
    imageNet_flat_list = list(set(imageNet_flat_list))
    #print('imageNet_flat_list', imageNet_flat_list)

    return df, yolo_flat_list, imageNet_flat_list

def create_combined_class_list(path):
    """ Create a list of combined Yolo and ImageNEt lists
        
        INPUTS:
        ------------
            path - (string) path to classification report
        
        OUTPUTS:
        ------------
            df - (pandas dataframe) of the the classification report
            combined_class_list - (list) of combined Yolo and ImageNEt lists
            yolo_flat_list - (list) of all in df observed Yolo classes
            imageNet_flat_list - (list) of all in df observed ImageNet classes
    """
    
    df, yolo_flat_list, imageNet_flat_list = get_yolo_and_imagenet_lists(path)
    
    yolo_flat_list = sorted(yolo_flat_list)
    imageNet_flat_list = sorted(imageNet_flat_list)

    combined_class_list = yolo_flat_list
    combined_class_list.extend(imageNet_flat_list)
    combined_class_list = sorted(combined_class_list)
    combined_class_list.insert(0,'Open this select menu')

    return df, combined_class_list, yolo_flat_list, imageNet_flat_list


def get_first_lat_datetime_value(df):
    """ Filter Classification Report via datetime (start and end datetime)
        
        INPUTS:
        ------------
            df - (pandas dataframe) of the the classification report
            data - (dictionary) used for filtering and output data storage
        
        OUTPUTS:
        ------------
            first_dt - (datetime) first date in in dataset
            last_dt - (datetime) last date in dataset
    """
    
    # first  datetime entry
    first_dt = df['date_time'].iloc[0].date() - timedelta(days=1)


    # last datetime entry
    last_dt = df['date_time'].iloc[-1].date() + timedelta(days=1)
    

    
    return first_dt, last_dt

 
def filter_by_datetime(df, data):
    """ Filter Classification Report via datetime (start and end datetime)
        
        INPUTS:
        ------------
            df - (pandas dataframe) of the the classification report
            data - (dictionary) used for filtering and output data storage
        
        OUTPUTS:
        ------------
            df_filter - (pandas dataframe) of the the classification report 
                        filtered by datetime start and end point
    """
    
    datetime_filter_lower = df['date_time'] >= data['start_date']
    datetime_filter_upper = df['date_time'] <=  data['end_date']

    # Select all cases where df['date_time'] >= start_datetime and df['date_time'] <= end_datetime
    df_filter = df[datetime_filter_lower & datetime_filter_upper]
    df_filter.sort_values('date_time', inplace=True, ascending=True)

    return df_filter


def filter_by_class(df, data):
    """ Filter Classsification Report based on certain class items of Yolo and ImageNet
        
        INPUTS:
        ------------
            df - (pandas dataframe) of the the classification report
            data - (dictionary) used for filtering and output data storage
        
        
        OUTPUTS:
        ------------
            df_filter - (pandas dataframe) of the the classification report 
                        filtered by class items of Yolo and ImageNet
    """
    
    selected_list = [data['selected_1'], 
                     data['selected_2'], 
                     data['selected_3'], 
                     data['selected_4'], 
                     data['selected_5'], 
                     data['selected_6'], 
                     data['selected_7'], 
                     data['selected_8']]
    
    
    
    if set(selected_list) == {'Open this select menu'}:
        """
        Mode 1: All Selectboxes are set to 'Open this select menu' --> No Class Filtering
        """
        return df
    
    
    else:
        """
        Mode 2: Apply class filter
        """
        df['imgnet_choice'] = df['classes_ImgNet'].apply(lambda x: any([k in str(x) for k in selected_list]))
        df['yolo_choice'] = df['classes_yolo'].apply(lambda x: any([k in str(x) for k in selected_list]))
        
       
        df_filter = df[(df['imgnet_choice'] == True) | (df['yolo_choice'] == True)]
    
    return df_filter


def create_image_infosets(df_filter, data):
    """ 1. Get info of images (image_path, gps, datetime, classification) and prepare it as info sets for web app
        2. Updata data['image_set'] based on fildering
        
        INPUTS:
        ------------
            df_filter - (pandas dataframe) of the the classification report 
                        filtered by datetime AND class items of Yolo and ImageNet
        
        OUTPUTS:
        ------------
            df_filter - (pandas dataframe) of the the classification report 
                        GPS info corrected for Google Maps, must be string of tuple for Google Maps 
            image_set - (list) paths to the actual set of images
            date_time - (list) of datetimes for actual images
            GPS - (list) of GPS coordinates  for actual images
            classes_yolo - (list) of lists od Yolo classes  for actual images
            classes_ImgNet - (list) of lists od ImageNet classes  for actual images
            markers_and_infos - (list) of lists with info of the actual image set 
                                (latitude, longitudes, image set, datetimes, GPS as tuple, yolo and Imagenet classes)
            
    """
    df_filter.loc[df_filter.GPS == '(None, None)', "GPS"] = "('None', 'None')"

    df_filter = df_filter.sort_values('file',ascending=True)

    image_set = [os.path.split(path)[1] for path in df_filter['file'].tolist()]
    
    data['image_set'] = image_set

    date_time = df_filter['date_time'].tolist()
    GPS = eval(str(df_filter['GPS'].tolist()))
    classes_yolo = df_filter['classes_yolo'].tolist()
    classes_ImgNet = df_filter['classes_ImgNet'].tolist()
    
    lats = [x[0] for x in df_filter['GPS'].tolist()]
    longs = [x[1] for x in df_filter['GPS'].tolist()]
    markers_and_infos = [lats,
                        longs,
                        image_set,
                        [str(dt) for dt in date_time],
                        GPS,
                        classes_yolo,
                        classes_ImgNet
                        ]

    #for kundex, elmt in enumerate(markers_and_infos[4]):
    #    markers_and_infos[4][kundex] = list(ast.literal_eval(elmt))
    #for kundex, elmt in enumerate(markers_and_infos[5]):
    #    markers_and_infos[5][kundex] = ast.literal_eval(elmt)
    #for kundex, elmt in enumerate(markers_and_infos[6]):
    #    markers_and_infos[6][kundex] = ast.literal_eval(elmt)

    data['markers_and_infos'] = markers_and_infos

    return df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos



def set_path_for_image(image_path, base_dir, target_folder):
    """ Correct the path of a stored image by concating the filename to the actual media path ( base_dir + target_folder). 
        The base_dir is the dirpath to the classification report (provided via the web app later on)
        
        INPUTS:
        ------------
            image_path - (string) path to the image provided in the classifiication report
            base_dir - (string) dir_path to the classifcation report (e.g. /Volume/.../my_images) 
            target_folder - (string) two possibilities: 1. target_folder = 'images' --> location of the original images
                            2. target_folder = 'images_yolo' --> folder of images generated by Yolo classification
        
        OUTPUTS:
        ------------
            new_path_image - (string) corrected path to the actual image
            
    """
    try:
        path_to_file, filename = os.path.split(image_path)
    
       
        new_path_image = os.path.join(base_dir, target_folder, filename)
        
    
        return new_path_image
    except:
        return None
    
def check_file_path(row):
    """ Check if Yolo image exists. return True if Yes, False if not.
        This True and False definition is needed to create successfully thumbnail images.
        This should be done ONLY if the Yolo Image exists. Otherwise an error would occur.
        
        INPUTS:
        ------------
            row - ( pandas Series) actual chosen row of the classification report DataFrame
            
        
        OUTPUTS:
        ------------
            True/False - (bool) if Yolo image in that row exist, False if not 
             
    """
    try:
        return os.path.isfile(row)
    except:
        return False

def get_thumbnail(path):
    """ Create a thumbnail image for the actual chosen image
        
        INPUTS:
        ------------
            path - (string) the CORRECTED path to the actual image
        
        OUTPUTS:
        ------------
            i (Image) a thumbnail image for the actual image
    """
    i = Image.open(path)
    i.thumbnail((300, 300), Image.LANCZOS)
    return i

def get_image_asraw_Base64(im):
    """ Convert image back to a readable html tag for the browser
        
        INPUTS:
        ------------
            im - (Image) an Image object 
        
        OUTPUTS:
        ------------
            html_img (string) an html tag for browser displaying
    """
    buffer = io.BytesIO()
    im.save(buffer, format='PNG')
    buffer.seek(0)

    data_uri = base64.b64encode(buffer.read()).decode('ascii')

    #html = '<html><head></head><body>'
    html_img = '<img src="data:image/png;base64,{0}">'.format(data_uri)
    #html += '</body></html>'

    return html_img


def df_as_html(df, base_dir):
    """ Transform the DataFrame with images to HTML object
        
        INPUTS:
        ------------
            df - (pandas dataframe) of the the classification report 
                 (eventiully filtered by datetime AND class items of Yolo and ImageNet)
            
        
        OUTPUTS:
        ------------
            No return 
            filter_result.html - (file) an html file containing the filter output with thumbnail images
    """
    pd.set_option('display.max_colwidth', -1)

    df['image'] = df.apply(lambda row: get_thumbnail(set_path_for_image(row['path_to_file'], base_dir, 'images')), axis = 1)
    df['exists'] = df.apply(lambda row: check_file_path(set_path_for_image(row['img_path_yolo'], base_dir, 'images_yolo')), axis = 1)

    df['image_yolo'] = df.apply(lambda row: get_thumbnail(set_path_for_image(row['img_path_yolo'], base_dir, 'images_yolo')) if row['exists'] == True else None, axis = 1)

    try:
        df.drop('exists', inplace =True, axis=1)
    except:
        pass


    # Convert DataFrame to HTML, displaying PIL.Image objects embedded in dataframe
    html = df.to_html(formatters={'image': get_image_asraw_Base64, 'image_yolo': get_image_asraw_Base64}, escape=False)

    #with open(image_folder + '.html', 'w') as f:
    with open('filter_result.html', 'w') as f:
        f.write(html)





def get_filtered_data(df_filter, data):
    """ Main function in order to 
        1. filter the classifcation report based on classes and datetimes 
        2. create image infosets for the web app
        
        INPUTS:
        ------------
            df_filter (pandas dataframe) the NON filtered (just loaded dataframe) of the the classification report file
            data - (dictionary) used for filtering and output data storage
            
        OUTPUTS:
        ------------
            df_filter - (pandas dataframe) updated (filtered) dataframe of the the classification report 
            data - (dictionary) updated data dictionary (key 'image_set' is updated)
            image_set - (list) paths to the actual set of images
            date_time - (list) of datetimes for actual images
            GPS - (list) of GPS coordinates  for actual images
            classes_yolo - (list) of lists od Yolo classes  for actual images
            classes_ImgNet - (list) of lists od ImageNet classes  for actual images 
            markers_and_infos - (list) of lists with info of the actual image set 
                                (latitude, longitudes, image set, datetimes, GPS as tuple, yolo and Imagenet classes)  
    """
    
    
    # check datetime filter, if checked filter by datetime range
    if data['check_date'] == True:
        print('-------------------------')
        print('   DATE FILTER CHECKED')
        print('-------------------------')
        df_filter = filter_by_datetime(df_filter, data)

    else:
        print('-------------------------')
        print(' DATE FILTER NOT CHECKED')
        print('-------------------------')
        
        

    # check check_classification filter, if checked filter by chosen ImageNet and Yolo classes
    if data['check_classification'] == True:
        print('-------------------------')
        print('  CLASS FILTER CHECKED')
        print('-------------------------')
        df_filter = filter_by_class(df_filter, data)


    else:
        print('-------------------------')
        print('CLASS FILTER NOT CHECKED')
        print('-------------------------')
    
    df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos = create_image_infosets(df_filter, data)


    return df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos


def load_likes(path, data):
    """ Action, when 'Load Favoirites' Button was clicked. Load likes from like_setting.json

        INPUTS:
        ------------
            path - (string) path to images.pkl
            data - (dictionary) the data dictionary with control settings from run.py
        
        OUTPUTS:
        ------------
            df_filter - (pandas dataframe) updated (filtered) dataframe of the the classification report 
            data - (dictionary) updated data dictionary (key 'image_set' is updated)
            image_set - (list) paths to the actual set of images
            date_time - (list) of datetimes for actual images
            GPS - (list) of GPS coordinates  for actual images
            classes_yolo - (list) of lists od Yolo classes  for actual images
            classes_ImgNet - (list) of lists od ImageNet classes  for actual images 
            markers_and_infos - (list) of lists with info of the actual image set 
                                (latitude, longitudes, image set, datetimes, GPS as tuple, yolo and Imagenet classes)  

    """
    df = load_data(path)
    with open('like_setting.json') as f:
        like_setting = json.load(f) 
    df_filter = df[df['path_to_file'].apply(lambda x: os.path.split(x)[1] in list(like_setting.keys()))]
    df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos = create_image_infosets(df_filter, data)
    return df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos

def save_likes(data):
    """ Action, when 'Save Favourites' Button was clicked. Save like setting in like_setting.json

        INPUTS:
        ------------
            data - (dictionary) the data dictionary with control settings from run.py

        OUTPUTS:
        ------------
            save actual like settings in like_setting.json

    """
    with open('like_setting.json') as f:
        like_setting = json.load(f)

    for key, element in data['likes'].items():
        if element == True:
            path, file_name = os.path.split(key)
            like_setting[file_name] = path
        if element == False:
            try:
                del like_setting[file_name]
            except:
                pass
        print(like_setting)

    with open('like_setting.json', 'w') as f:
        json.dump(like_setting, f)
            
