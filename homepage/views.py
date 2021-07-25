from __future__ import print_function
import pickle
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from numpy import genfromtxt
import numpy as np
import os
from io import StringIO
from django.core.files.storage import FileSystemStorage
import inspect
import matplotlib.pyplot as plt
import json
from IPython.display import display
from pygooglenews import GoogleNews
import datetime as dt
import pandas as pd
import selenium as sel
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import requests
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig, AutoModelForSeq2SeqLM, AutoTokenizer, pipeline, AutoTokenizer, AutoModel
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import *
from django.contrib.auth.decorators import *
import psycopg2
# imports

import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import sys
import os
from .Autosorter.sort import query
import psycopg2

# Create your views here.


global fileString
prob = None

def article(request):
    return render(request, 'homepage/article.html')

def home(request):
    if(request.method == "POST" and request.FILES['file']):
        global fileString
        theFile = request.FILES["file"]
        fs = FileSystemStorage()
        filename = fs.save(theFile.name, theFile)
        uploaded_file_url = fs.url(filename)
        fileString = str(uploaded_file_url)
        return HttpResponseRedirect('upload')
    return render(request, 'homepage/index/home.html',)





def aboutUsPage(request):
    return render(request, 'homepage/aboutus.html')


def autoSorterPage(request):
    return render(request, 'homepage/autosorter.html')


def autoSortermain(request):
    createFolder(request)
    driveApiSorter()
    context = {

    }
    return render(request, 'homepage/autosorter.html', context)


def getEmailOfUser(request):
    try:
        return request.user.email
    except AttributeError:
        print('Please Login to our Hackedt to get access to autosorter')


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

subjects = ["Chemistry", "Algebra", "World History", "Language"]

# holds id for folders
ids_for_folder = {}

# initializes creds to None
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Call the Drive v3 API
service = build('drive', 'v3', credentials=creds)

# If folders are already created and stored in requirements.txt,
# read them from requirements.txt and store them in ids.
# If not, create folders and put ids in ids.


def createFolder(request):
    global subjects
    global ids_for_folder

    # Subjects (folders)

    # Opens requirements.txt
    # print(filesize)
    ids = []
    if getValues(request) == False:
        # If requirements.txt is empty, make folders and get id
        for subject in subjects:
            file_metadata = {
                'name': subject,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            file = service.files().create(body=file_metadata,
                                          fields='id').execute()
            id = file.get('id')
            ids.append(id)
        folder_ids = ",".join(ids)
        uploadValues(request, folder_ids)

    elif getValues(request):
        folder_ids = getValues()
        folder_ids = folder_ids.split(',')

    # Fill dict folder_ids with subjects as the keys and the ids as the values
    print(folder_ids)
    for i in range(len(subjects)):
        ids_for_folder[subjects[i]] = folder_ids[i]

# Create shortcut to file from folder


def createShortcut(file_id, folder_id):
    file = service.files().get(fileId=file_id, fields='id, parents, name').execute()
    shortcut_metadata = {
        'Name': file.get('name'),
        'mimeType': 'application/vnd.google-apps.shortcut',
        'shortcutDetails': {
            'targetId': file_id
        }
    }
    shortcut = service.files().create(body=shortcut_metadata,
                                      fields='id,shortcutDetails').execute()
    service.files().update(fileId=shortcut.get('id'),
                           addParents=folder_id,
                           fields='id, parents',).execute()

# Creates folders if not already created
# If folders are already created, get IDs from requirements.txt


# Loops over all files

def driveApiSorter():
    page_token = None
    while True:
        response = service.files().list(q="mimeType='application/vnd.google-apps.document'" or "mimeType='application/vnd.google-apps.drawing'" or "mimeType='application/vnd.google-apps.form'" or "mimeType='application/vnd.google-apps.presentation'" or "mimeType='application/vnd.google-apps.spreadsheet'",
                                        spaces='drive',
                                        fields='nextPageToken, files(id, name)',
                                        pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            datecreated_split_temp = service.files().get(fileId=file.get(
                'id'), fields="createdTime").execute()['createdTime'].split('-')
            yearvariable = datecreated_split_temp[0]

            datetime_obj = datetime.datetime.now()

            # Checks if file has been created/last modified within the last year
            if (int(datetime_obj.year)-1) <= (int(yearvariable)):
                # Uses sort function to get the subject for the file based on file name
                folder_name = query(file.get('name'), subjects)
                # Print the file name and the folder name
                print(f"{file.get('name')} - {folder_name}")
                # Create shortcut to file in folder
                createShortcut(file.get('id'), ids_for_folder[folder_name])
        
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break        
        

   
    # If no more pages, end

    print("Task completed! :)")
    if os.path.exists('token.json'): 
        os.remove('token.json')


def getRowsFromDatabase(postgreSQL_select_Query):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="NWC_if3eTGyHWGRon1UcrEy7iRsPGm5p",
                                      host="localhost",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from mobile table using cursor.fetchall")
        user_id = cursor.fetchall()
        return user_id

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

#!/usr/bin/python


def sql_request(sql):
    vendor_id = None
    conn = None

    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(user="postgres",
                                password="NWC_if3eTGyHWGRon1UcrEy7iRsPGm5p",
                                host="localhost",
                                port="5432",
                                database="postgres")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        #vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print('ERROR')
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return vendor_id


def uploadValues(request, foldersid):
    user_id = getRowsFromDatabase(
        f"SELECT user_id FROM account_emailaddress WHERE email='{getEmailOfUser(request)}';")[0][0]
    sql_request(
        f"INSERT INTO user_folderid(user_id,folder_id) VALUES ({user_id}, '{foldersid}');")


def getValues(request):
    try:
        user_id = getRowsFromDatabase(
            f"SELECT user_id FROM account_emailaddress WHERE email={getEmailOfUser(request)}';")[0][0]
        check = getRowsFromDatabase(f"SELECT folder_id FROM user_folderid WHERE user_id={user_id};")[
            0][0]  # check if this is true/false

        return check
    except Exception as error:
        return False
