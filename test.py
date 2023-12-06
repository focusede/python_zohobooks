import json
import requests
import csv

# Zoho Books API credentials
client_id = 'your_client_id from zoho dev console'
client_secret = 'your_client_secret from zoho dev console'
redirect_uri = 'http://www.zoho.com/books' # us books URL
organization_id = 'your_org_id from your zoho account'
token_file = 'data/token.txt' # storage for token
refresh_token_file = 'data/refresh_token.txt' # storage for refresh token
access_token = '' # init token

# Zoho Books API endpoints - us URLs
auth_url = 'https://accounts.zoho.com/oauth/v2/auth'
token_url = 'https://accounts.zoho.com/oauth/v2/token'
api_url = 'https://books.zoho.com/api/v3/' 

def get_refresh_token():
    try:
        with open(refresh_token_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_refresh_token(refresh_token):
    with open(refresh_token_file, 'w') as file:
        file.write(refresh_token)

def get_access_token():
    try:
        with open(token_file, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def save_access_token(access_token):
    with open(token_file, 'w') as file:
        file.write(access_token)

def get_new_token():
    refresh_token = get_refresh_token()
    # Get access token using the authorization code
    token_params = {
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'refresh_token'
    }
    token_response = requests.post(token_url, data=token_params)
    global access_token
    access_token = token_response.json().get('access_token')
    save_access_token(access_token)

def get_timesheets_from_api(project_id):
    page = 1
    timesheet_entries = []
    while True:
        headers = {
           'Authorization': f'Zoho-oauthtoken {access_token}'
        }
        response = requests.get(api_url + f'projects/timeentries?organization_id={organization_id}&page={page}&project_id={project_id}', headers = headers)
        if response.status_code == 200:
            page_context = response.json().get('page_context')
            page_timesheet_entries = response.json().get('time_entries')
            timesheet_entries.extend(page_timesheet_entries)
            if page_context['has_more_page'] == False:
                break
            else:
                page=page+1
        elif response.status_code==401:
            get_new_token()
        else:
            print(f"Error getting timesheet data: {response.json()['message']}")
            return
    return timesheet_entries

def get_projects_from_api():
    page = 1
    print("Getting Projects from API...")
    while True:
        headers = {
           'Authorization': f'Zoho-oauthtoken {access_token}'
        }
        timesheet_projects = []
        response = requests.get(api_url + f'projects?organization_id={organization_id}&filter_by=Status.Active&sort_column=project_name&page={page}', headers=headers)
        if response.status_code == 200:
            page_context = response.json().get('page_context')
            page_timesheet_projects = response.json().get('projects')
            timesheet_projects.extend(page_timesheet_projects)
            if page_context['has_more_page'] == False:
                break
            else:
                page=page+1
        elif response.status_code==401:
            get_new_token()
        else:
            break
    # save 
    with open("data/projects.json", "w") as outfile:
        json.dump(timesheet_projects, outfile)
    return timesheet_projects

def export_csv(export_filename, export_obj):
    with open(export_filename, 'w', newline='', encoding='utf-8') as data_file:
        # create the csv writer object
        csv_writer = csv.writer(data_file, dialect='excel', quoting=csv.QUOTE_NONNUMERIC)
        count = 0
        for row in export_obj:
            if count == 0:
                # Writing headers of CSV file
                header = row.keys()
                csv_writer.writerow(header)
                count += 1
        
            # Writing data of CSV file
            csv_writer.writerow(row.values())
        data_file.close()

if __name__ == "__main__":
    access_token = get_access_token()
    projects = get_projects_from_api()
    # get timesheets for first project found [0] - replace with what project_id you are looking for
    ts = get_timesheets_from_api(project_id=projects[0]["project_id"])
    
    # export projects
    export_csv('export_projects.csv', projects)
    # export timesheets 
    export_csv('export_ts.csv', ts)



