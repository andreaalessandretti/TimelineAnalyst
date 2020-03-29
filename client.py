from zipfile import ZipFile
import os.path
from os import path
import requests

if path.exists('temp'):
    print('The folder temp already exists.')
else:
    #https://takeout.google.com/settings/takeout/custom/location_history
    filename = '/Users/andrea/Downloads/takeout-20200328T141106Z-001.zip'
    print("Unzipping file ... ", filename , end = '')

    with ZipFile(filename, 'r') as zipObj:
       zipObj.extractall('temp')

    print("done")




# api-endpoint
URL = "http://127.0.0.1:5000"


# Get
r = requests.get(url = URL+'/empdb/employee')

# extracting data in json format
data = r.json()

print('All employee')
print(data)


# Get

id = 101
r = requests.get(url = URL+'/empdb/employee/'+str(id))

# extracting data in json format
data = r.json()

print('Get employee',str(id))
print(data)



#POST
print('POST #########')
# data to be sent to api

id = 101
data = {'id':'1', 'name':'And33rea', 'title':'tes33t'}

r = requests.post(url = URL+'/empdb/employee', json = data)
#r = requests.post(url = URL+'/empdb/employee', data = data)

data = r.json()

print(data)




r = requests.get(url = URL+'/empdb/employee')

# extracting data in json format
data = r.json()

print('All employee')
print(data)

'''
#POST

# data to be sent to api
data = {'api_dev_key':API_KEY,
        'api_option':'paste',
        'api_paste_code':source_code,
        'api_paste_format':'python'}

# sending post request and saving response as response object
r = requests.post(url = API_ENDPOINT, data = data)

# extracting response text
pastebin_url = r.text
print("The pastebin URL is:%s"%pastebin_url)


#Get
# location given here
location = "delhi technological university"

# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}

# sending get request and saving the response as response object
r = requests.get(url = URL, params = PARAMS)

# extracting data in json format
data = r.json()
'''


'''
from getpass import getpass
>>> requests.get('https://api.github.com/user', auth=('username', getpass()))
<Response [200]>
'''
