# imports
from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import datetime
import sys
import os
from .sort import query
import psycopg2


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']

subjects = ["Chemistry", "Algebra", "World History", "Language"]

# holds id for folders
folder_ids = {}

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
            'homepage/Autosorter/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

# Call the Drive v3 API
service = build('drive', 'v3', credentials=creds)

# If folders are already created and stored in requirements.txt,
# read them from requirements.txt and store them in ids.
# If not, create folders and put ids in ids.\

def getRowsFromDatabase():
    try:
        connection = psycopg2.connect(user="ujfijzsb",
                                    password="NWC_if3eTGyHWGRon1UcrEy7iRsPGm5p",
                                    host="batyr.db.elephantsql.com",
                                    port="5432",
                                    database="ujfijzsb")
        cursor = connection.cursor()
        postgreSQL_select_Query = "select * from mobile"

        cursor.execute(postgreSQL_select_Query)
        print("Selecting rows from mobile table using cursor.fetchall")
        mobile_records = cursor.fetchall()

        print("Print each row and it's columns values")
        for row in mobile_records:
            print("Id = ", row[0], )
            print("Model = ", row[1])
            print("Price  = ", row[2], "\n")

    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from PostgreSQL", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

#!/usr/bin/python

def insert_vendor(vendor_name):
    sql = """INSERT INTO user_folderid(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    conn = None
    vendor_id = None
    try:
        # connect to the PostgreSQL database
        conn = psycopg2.connect(user="ujfijzsb",
                                    password="NWC_if3eTGyHWGRon1UcrEy7iRsPGm5p",
                                    host="batyr.db.elephantsql.com",
                                    port="5432",
                                    database="ujfijzsb")
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (vendor_name,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id

def createFolder():
    global subjects
    global folder_ids

    # Subjects (folders)
    
    # Opens requirements.txt
    f = open("homepage/Autosorter/requirements.txt", "r+")
    filesize = os.path.getsize("homepage/Autosorter/requirements.txt")
    print(filesize)
    ids = []
    if filesize == 0:
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
            f.write(id + "\n")
    else:
        # Else, read ids from requirements.txt into ids array
        ids = [id.replace("\n", "") for id in f.readlines()]

    # Fill dict folder_ids with subjects as the keys and the ids as the values
    print(ids)
    for i in range(len(subjects)):
        folder_ids[subjects[i]] = ids[i]

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
createFolder()


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
	            createShortcut(file.get('id'), folder_ids[folder_name])

	    # If no more pages, end
	    page_token = response.get('nextPageToken', None)
	    if page_token is None:
	        break
	print("Task completed! :)")