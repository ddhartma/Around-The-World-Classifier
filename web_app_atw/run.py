from wrangling_scripts.filter_data import create_combined_class_list, get_filtered_data, df_as_html, save_likes, load_likes
import json

from flask import Flask
from flask import render_template, request, jsonify, redirect, url_for
from flask import send_file, send_from_directory

import os

cwd = os.getcwd()


class Data():
	# Initialize data controls
	data = {'check_classification': True,
			'check_date': True,
			'check_map': True,
			'selected_1': 'Open this select menu',
			'selected_2': 'Open this select menu', 
			'selected_3': 'Open this select menu',
			'selected_4': 'Open this select menu',
			'selected_5': 'Open this select menu',
			'selected_6': 'Open this select menu',
			'selected_7': 'Open this select menu',
			'selected_8': 'Open this select menu',
			'start_date': "2014-04-05",
			'end_date': "2014-04-07",
			'current_location_lat': 0,
			'current_location_lon': 0,
			#'current_zoom': 5,
			#'current_radius': 500,
			}

data_tank = Data() 
data = data_tank.data

# Set path to Classification report
try:
	with open('setting.json') as f:
		setting = json.load(f) 
	
	data['class_rep_file_path'] = setting['class_rep_file_path']
	data['google_api'] = setting['google_api']
except:
	data['class_rep_file_path'] = 'path/to/class_report'
	data['google_api'] = 'YOUR_GOOGLE_API'


# Set main paths --> Base, ClassRep and Media 
BASE_DIR = os.path.split(data['class_rep_file_path'])[0]

# Check if stored path to classification path exists, if yes take it, if not set application path use test/example file 
if os.path.isfile(data['class_rep_file_path']):
    BASE_DIR = os.path.split(data['class_rep_file_path'])[0]
    CLASS_REP_DIR = data['class_rep_file_path']
else: 
    BASE_DIR =  os.path.dirname(os.path.abspath(__file__))
    CLASS_REP_DIR = os.path.join(BASE_DIR, 'images.xlsx')

MEDIA_DIR = os.path.join(BASE_DIR, 'images').replace('\\', '/')

print()
print('*********************************')
print('PATH SETTINGS')
print('BASE_DIR: ', BASE_DIR)
print('CLASS_REP_DIR: ', CLASS_REP_DIR)
print('MEDIA_DIR: ', MEDIA_DIR)
print('*********************************')
print()


# Load Classifcation Report
# Get combined_class_list (concated list of yolo_flat_list and imageNet_flat_list)
df, combined_class_list, yolo_flat_list, imageNet_flat_list = create_combined_class_list(CLASS_REP_DIR)
data['combined_class_list'] = combined_class_list

# Initialize df_filter, use only the first 20 images of the dataset
df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos  = get_filtered_data(df[:20], data)

# Start Flask app
app = Flask(__name__)

# Main url
@app.route('/')
def index():
	return render_template('index.html', 
						class_rep_file_path=data['class_rep_file_path'],
						google_api=data['google_api'],
						check_classification=data['check_classification'],
						check_date=data['check_date'],
						check_map=data['check_map'],
						selected_1=data["selected_1"],
						selected_2=data["selected_2"], 
						selected_3=data["selected_3"],
						selected_4=data["selected_4"],
						selected_5=data["selected_5"],
						selected_6=data["selected_6"],
						selected_7=data["selected_7"],
						selected_8=data["selected_8"],
						start_date=data['start_date'],
						end_date=data['end_date'],
						combined_class_list=combined_class_list,
						current_location_lat=data['current_location_lat'],
						current_location_lon=data['current_location_lon'],
						#current_zoom=data['current_zoom'],
						#current_radius=data['current_radius'],
						image_set=data['image_set'],
						markers_and_infos=data['markers_and_infos'],
						number_images=len(data['image_set']),
						)
# url after JS POST
@app.route('/return_after_js/')
def return_after_js():
	return render_template('index.html', 
						class_rep_file_path=data['class_rep_file_path'],
						google_api=data['google_api'],
						check_classification=data['check_classification'],
						check_date=data['check_date'],
						check_map=data['check_map'],
						selected_1=data["selected_1"],
						selected_2=data["selected_2"], 
						selected_3=data["selected_3"],
						selected_4=data["selected_4"],
						selected_5=data["selected_5"],
						selected_6=data["selected_6"],
						selected_7=data["selected_7"],
						selected_8=data["selected_8"],
						start_date=data['start_date'],
						end_date=data['end_date'],
						combined_class_list=combined_class_list,
						current_location_lat=data['current_location_lat'],
						current_location_lon=data['current_location_lon'],
						#current_zoom=data['current_zoom'],
						#current_radius=data['current_radius'],
						image_set=data['image_set'],
						markers_and_infos=data['markers_and_infos'],
						number_images=len(data['image_set'])
						)

# connect images in HTML with MEDIA_DIR
@app.route('/uploads/<path:filename>')
def show_file(filename):
    return send_from_directory(MEDIA_DIR, filename, as_attachment=True)

# connect images in HTML with MEDIA_DIR
@app.route('/uploads/')
def send_file(filename):
    return send_file(filename, mimetype='image/jpg')

# info print statetments after JS POST
def redirect_filter_result(df_filter):
	data_tank.df_filter = df_filter

	print()
	print('--------------------- markers_and_infos start --------------------- ')
	info_names =['lats','longs','image_set', 'date_times', 'GPS', 'classes_yolo', 'classes_ImgNet']
							
	for info_name, element in zip(info_names, data['markers_and_infos']):
		print('-------------')
		print(info_name)
		print('-------------')
		print(element)
	print('--------------------- markers_and_infos end --------------------- ')

# info print statetments after JS POST, state of checkboxes and button events
def redirect_ui_status():
	print()
	print("data['load_fav']", data['load_fav']) 
	print("data['save_fav']", data['save_fav'])   
	print("data['export_table']", data['export_table'])  
	print("data['apply_filter']", data['apply_filter'])  
	print()
	print("data['class_rep_file_path']", data['class_rep_file_path']) 
	print("data['google_api']", data['google_api'])   
	print()
	print("data['check_classification']", data['check_classification'])  
	print("data['check_date']", data['check_date'])  
	print("data['check_map']", data['check_map'])  
	print()
	

# Get results Back from Javascript SUBMIT BUTTON
@app.route("/get_post_js_submit", methods=["POST"])
def get_post_js_submit():
	if request.method == "POST":
			data = data_tank.data
			

			data_back = request.get_json()
			data_back = data_back['data']

			data.update(data_back)

			# FILTER BUTTON CLICKED --> Filter Data 
			if data['apply_filter'] == True:
				df_filter = df.copy()
				df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos  = get_filtered_data(df_filter, data)
				redirect_filter_result(df_filter)
				redirect_ui_status()
				return redirect(url_for('return_after_js'))

			# EXPORT TABLE BUTTON CLICKED --> Export filtered Table as HTML file
			if data['export_table'] == True:
				df_as_html(data_tank.df_filter, base_dir=BASE_DIR)
				redirect_ui_status()
			
			# LOAD FAVOURITES BUTTON CLICKED --> Load Favourite Selection
			if data['load_fav'] == True:
				df_filter, data, image_set, date_time, GPS, classes_yolo, classes_ImgNet, markers_and_infos = load_likes(CLASS_REP_DIR, data)
				redirect_filter_result(df_filter)
				redirect_ui_status()
				return redirect(url_for('return_after_js'))

			# SAVE FAVOURITES BUTTON CLICKED --> Save actual Favourite Selection
			if data['save_fav'] == True:
				
				print('Likes')
				print(data['likes']) 
				save_likes(data)
				redirect_ui_status()

			# SAVE PATH AND API BUTTON CLICKED --> Save actual chosen path to classification report and actual provided Google Maps API
			if data['save_path_api'] == True:
				
				print('Save path and API')
				print(data['save_path_api']) 
				print(data['class_rep_file_path'])
				print(data['google_api'])
				setting = {}
				setting['class_rep_file_path'] = data['class_rep_file_path']
				setting['google_api'] = data['google_api']

				with open('setting.json', 'w') as f:
					json.dump(setting, f)

				redirect_ui_status()

		
		
def main():
	""" Start the Web App
	"""
	app.run(host='0.0.0.0', port=3001, debug=True)


if __name__ == '__main__':
    main()
                           