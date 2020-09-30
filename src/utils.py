import re
import json
import copy
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from src.storage import bucket, metadata, s3_client
from src.flags import FLAGS

BASE_URL = 'https://pypi.org/pypi'


def get_json_url(package_name):
    return BASE_URL + '/' + package_name + '/json'


def get_packages():
    print('Getting packages...')
    packages = _get_projects_from_spreadsheet()
    print('- Done.')
    return packages


def _get_projects_from_spreadsheet():
    # use credentials to create a client to interact with the Google Drive API
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    spr = client.open("Python 3 VFX packages (vfxpy.com)")
    sheet = spr.worksheet("content")

    # Extract all of the values
    items = sheet.get_all_records()

    # Remap values
    data = list()
    for item in items:
        item_data = dict()
        item_data["id"] = re.sub("[^0-9a-zA-Z]+", "_", item.get("Product").lower())
        item_data["vendor"] = item.get("Vendor")
        item_data["name"] = item.get("Product")
        item_data["type"] = item.get("Type")

        item_data["title"] = item.get("Description")
        item_data["body"] = item.get("Notes")
        item_data["package_version"] = item.get("Package Version")
        item_data["python_version"] = item.get("Python 3 Version")
        item_data["website"] = item.get("Web Site").strip()
        item_data["source"] = item.get("Source").strip()

        item_data["py3support"] = True if (item.get("Status") == "yes") else False
        item_data["css_class"] = "success" if item_data["py3support"] else "default"
        item_data["icon"] = "\u2713" if item_data["py3support"] else ""

        item_data["label"] = item.get("Label")
        item_data["label_css_class"] = "success" if (item_data["label"] == "Preview") else "warning"

        data.append(item_data)

    return data


def remove_irrelevant_packages(packages):
    print('Removing cruft...')
    packages = [package for package in packages
                if package.get('name') not in FLAGS.keys()]
    print('- Done.')
    return packages


def save_to_file(packages):
    now = datetime.datetime.now()
    key = 'results.json'
    tmp_path = './{0}'.format(key)
    with open(tmp_path, 'w') as f:
        f.write(json.dumps({
            'data': packages,
            'last_update': now.strftime('%A, %d %B %Y, %X %Z'),
        }))

    # extra_args = copy.deepcopy(metadata)
    # extra_args["ContentType"] = "application/json"

    # try:
    #     s3_client.upload_file(tmp_path, bucket, key, ExtraArgs=extra_args)
    # except Exception as e:
    #     print(e)
