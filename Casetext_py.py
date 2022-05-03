# -*- coding: utf-8 -*-
"""Casetext-py

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kSic5ICrvlgrjxjjyPwRqzI1vHfnPf0A
"""

# load packages
import requests # to create collection and upload to collection
import zipfile # to retrieve files from zip folder
import random # for randomly selecting files
import config # config.py contains authorozation token

# Initiate key variables
auth_token = config.auth_token
collection = 'https://project-apollo-api.stg.gc.casetext.com/v0/kayla-collects'
zip_file = '446c8aa0-6eba-11e5-bc7f-4851b79b387c.zip'

## Download Data

# Create function to retrieve all file names within zip file
file_name_list = [] # list to append file names to

def get_file_names():
  with zipfile.ZipFile(zip_file, 'r') as zip: 
   # Get list of files names in zip
   for name in zip.namelist(): # namelist(): zipfile function that creates list of all files in folder
     file_name_list.append(name) # append file names to list
# Call function to get all file names in folder
get_file_names()

# Create function to randomly select file names from file_name_list
random_file_list = [] # list to append random files names to

def get_random_files(x= 1000): # takes Number to randomly sample as input, 1000 is default
  for file in random.sample(file_name_list,x): # sample() fnc from "random" package
    random_file_list.append(file) # append randomly sampled file name to list

# Call function to randomly select files
get_random_files()

## Create WeSearch Collection

# Create Function tp Create a WeSearch Collection
def create_collection():
  headers = {
    'Authorization': 'Bearer ' + auth_token, # authorization token needed
    'Content-Type': 'application/json',
  }
  data = '{ "model": "lawbert" }' # lawbert is the default model
# data = '{"email":"","password":"[HIDDEN]"}'
  response = requests.post('https://project-apollo-api.stg.gc.casetext.com/v0/kayla-collects/create', headers=headers)
# Call Function to Create a WeSearch Collection
create_collection()
    
## Upload to Collection

# Create function to retrieve text from files of interest
files = []
def get_text():
  with zipfile.ZipFile(zip_file, 'r') as zip: 
    for file in random_file_list:
      with zip.open(file) as myfile:
        files.append(myfile.read())
# Call function to retrieve text
get_text()

# Upload files to Collection
def upload_files():
  headers = {
    'Authorization': 'Bearer ' + auth_token,
    'Content-Type': 'text/plain',
    }
  for data in files:
    response = requests.post(collection, headers=headers, data= data)

# Call function to upload files
upload_files()

# Verify succesful ingestion of 1000 files into collection (len)
print("There are " + str(len(response.json()['documents'])) + " documents in the Collection")