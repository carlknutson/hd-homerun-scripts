import math
import os
import requests
import sys

url = os.environ["HDHR_LOCAL_URL"]

def get_recordings():
    all_recorded_file_info = requests.get(f'http://{url}/recorded_files.json').json()

    unique_recordings = set()

    for recording in all_recorded_file_info:
        unique_recordings.add(recording['Title'])

    for recording_name in unique_recordings:
        print('"' + recording_name + '"')

def delete_recording(title):
    all_recorded_file_info = requests.get(f'http://{url}/recorded_files.json').json()

    deleted_count = 0

    for recording in all_recorded_file_info:
        if recording['Title'] == title:
            episodes = requests.get(recording['EpisodesURL']).json()
    
            for episode in episodes:

                try:
                    # https://info.hdhomerun.com/info/dvr_api:deleting_recordings
                    response = requests.post(url=episode['CmdURL'], params={'cmd':'delete', 'rerecord':'1'})
                    response.raise_for_status()
                except Exception:
                    print(f'Deleted {deleted_count} recording(s) of {title} before error.')
                    raise
                deleted_count += 1
    
    print(f'Deleted {deleted_count} recording(s) of {title}.')

def get_storage_details():
    info = get_capacity_info()

    print(f'Storage is {info["percentage_used"]}% used')
    print(f'Free storage remaining: {info["free_space"]}')

def get_capacity_info():
    dvr_info = requests.get(f'http://{url}/discover.json').json()

    total_space = dvr_info['TotalSpace']
    free_space = dvr_info['FreeSpace']

    used_space = total_space - free_space

    return {
        'free_space': convert_size(free_space),
        'percentage_used': round(used_space / total_space * 100, 2)
    }

# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor (math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def main():
    try:
        action = sys.argv[1]
    except IndexError:
        print('An action parameter, must be provided.')
        return

    if action == 'get_recordings':
        get_recordings()
    elif action == 'delete_recording':
        try:
            delete_recording(sys.argv[2])
        except IndexError:
            print(f'Action: {action}, requires a recording name input.')
    elif action == 'get_storage_details':
        get_storage_details()
    elif action == 'get_capacity_info':
        print(get_capacity_info())
    else:
        print(f'Action: {action}, is not implemented.')

if __name__ == "__main__":
    main()