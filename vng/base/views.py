from rest_framework.decorators import api_view
from rest_framework.response import Response
from .scrap_functions import rdw_scrapper
from flask import Flask, request, jsonify
from flask import request, abort
from functools import wraps
from base64 import encodebytes
from joblib import dump, load
import pandas as pd
from PIL import Image
from . import read_exifdata
import numpy as np
import ast
import io
import os
from PIL.ExifTags import TAGS
from .scrap_functions import license_number_with_company_name
from .models import Company, LicensePlate, TargetImage
# Create your views here.
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm', 'tif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def get_response_image(image_path):
    pil_img = Image.fromarray(np.uint8(image_path)).convert('RGB') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('utf-8') # encode as base64
    return encoded_img
def limit_content_length(max_length):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cl = request.content_length
            if cl is not None and cl > max_length:
                abort(413)
            return f(*args, **kwargs)
        return wrapper
    return decorator
# Companies and map irregularities API
@api_view(['GET'])
def vngp1_predict_pre_extracted(request, place_type):
    if (len(place_type) == 0):
        return Response({'error': 'Data is not correct. Please make a search again'})
    output_dir = ''
    data_directory = f'{os.getcwd()}/base/10-08-22'
    companies_details_csv = f'{data_directory}/674_records_final_result_merged_with_updated_bovag_merged_reviews_and_irregularities.csv'#place_api_car_companies_indicators.csv'

    companies_df = pd.read_csv(companies_details_csv)

    companies_df["lat_lng"] = [[geometry['location']['lat'], geometry['location']['lng']] for geometry in
                        [ast.literal_eval(i) for i in companies_df["geometry"]]]
    
    if place_type != 'all':
        companies_df = companies_df[companies_df['types'].str.contains(place_type)]
    companies_indicators_dict = companies_df.fillna(0).to_dict('r')

    response_dict = {'status': 'new',
                        'compnaies_indicators_dict': companies_indicators_dict,
                        }
    return Response(response_dict)

@api_view(['POST'])
def vngp1_predict_license_plate(request):
    file = request.data.get('file')
    print(file)
    if file == "":
        return Response({'error': 'No file'})
    image_bytes = file.read()
    with open("image.jpg", "wb") as img:
        img.write(image_bytes)
        
    license_plate_company_data = license_number_with_company_name.get_image_upload_license_company_res(image_bytes)
    # read metadata
    coordinates = read_exifdata.image_coordinates("image.jpg")
    lat = coordinates[0]
    lng = coordinates[1]
    rdw_scrapped_response = []
    for license_number in license_plate_company_data['license_number']:
        rdw_scrapped_response.append({license_number: rdw_scrapper.rdw_scrapper(license_number)})
    # storing into database
    company = Company()
    company.place_api_company_name = license_plate_company_data['place_api_company_name']
    company.bovag_matched_name = license_plate_company_data['bovag_matched_name']
    company.poitive_reviews = license_plate_company_data['poitive_reviews']
    company.negative_reviews = license_plate_company_data['negative_reviews']
    company.rating = license_plate_company_data['rating']
    company.duplicate_location = license_plate_company_data['duplicate_location']
    company.kvk_tradename = license_plate_company_data['kvk_tradename']
    company.irregularities = license_plate_company_data['irregularities']
    company.duplicates_found = license_plate_company_data['duplicates_found']
    company.Bovag_registered = license_plate_company_data['Bovag_registered']
    company.KVK_found = license_plate_company_data['KVK_found']
    company.company_ratings = license_plate_company_data['company_ratings']
    company.latitude = lat
    company.longitude = lng
    company.save()
    targetImage = TargetImage(company=company)
    targetImage.image = file
    targetImage.save()
    os.remove("image.jpg")
    
    for license_number in license_plate_company_data['license_number']:
        licensePlate = LicensePlate(company=company, target_image=targetImage)
        licensePlate.license_number = license_number
        licensePlate.save()
    
    
    return Response({"license_plate_company_data": license_plate_company_data, "license_numbers_data": rdw_scrapped_response})
# We are using RDW function inside the license-plate API. 
# So No need to make seperate RDW API 


# @api_view(['GET'])
# def rdw(request, license):
#     data = rdw_scrapper.rdw_scrapper(license)
#     return Response(data)

