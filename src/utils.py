import os
import re
import json
import copy

import pytz
from datetime import datetime

from src.flags import FLAGS


def get_packages(gs_client):
    print("Getting packages...")

    # Find a spreadsheet by key and open the content sheet
    book = gs_client.vfxpy_book
    worksheet = book.worksheet("content")

    packages = _get_projects_from_spreadsheet(worksheet)
    return packages


def _get_projects_from_spreadsheet(worksheet):

    # Extract all of the values
    items = worksheet.get_all_records()

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
    print("Removing cruft...")
    packages = [package for package in packages
                if package.get("name") not in FLAGS.keys()]
    return packages


def save_to_file(s3_client, packages):
    now = datetime.now(pytz.utc)
    key = "results.json"

    if os.environ.get("IS_LAMBDA_FUNCTION") == "1":
        tmp_path = "/tmp/{0}".format(key)
    else:
        tmp_path = "./{0}".format(key)

    with open(tmp_path, "w") as f:
        f.write(json.dumps({
            "data": packages,
            "last_update": now.strftime("%A, %d %B %Y, %X %Z"),
        }))

    extra_args = copy.deepcopy(s3_client.metadata)
    extra_args["ContentType"] = "application/json"
    extra_args["ACL"] = "public-read"

    print("Uploading results to S3...")
    s3_client.upload_file(tmp_path, key, extra_args)


def compare_and_notify(s3_client, gs_client):
    print("Comparing data...")

    # Find a spreadsheet by key and open the first sheet
    community_book = gs_client.community_book
    if not community_book:
        now = datetime.now(pytz.utc)
        s3_client.warn("Could not access community maintained spreadsheet on: {}".format(
            now.strftime("%A, %d %B %Y, %X %Z")))
        return

    community_worksheet = community_book.get_worksheet(0)

    # Extract all of the values
    records = community_worksheet.get_all_records()

    # Construct comparable data
    new_record_data = construct_record_data(records)

    # Get last recorded data from S3
    record_list = s3_client.list_files("records/")

    if record_list:
        newest = record_list[0]["Key"]
        oldest = record_list[-1]["Key"]

        obj = s3_client.get_object(newest)
        content = obj["Body"].read().decode("utf-8")
        content_dict = json.loads(content)

        old_record_data = content_dict.get("data")

        # delete one record if 5 already exist on S3
        if len(record_list) >= 5:
            s3_client.delete_object("records/{}".format(oldest))
    else:
        old_record_data = dict()

    # Compare data
    changes = list()
    for k, new in new_record_data.items():
        old = old_record_data.get(k)
        if not old:
            changes.append({
                "product": k,
                "key": "ALL",
                "old_value": "NO_DATA",
                "new_value": "FULL_SET",
            })
        else:
            for key, value in new.items():
                old_value = old.get(key)
                if value != old_value:
                    changes.append({
                        "product": k,
                        "key": key,
                        "old_value": old_value,
                        "new_value": value,
                    })

    if not changes:
        print("No changes detected!")
    else:
        # Send email
        s3_client.notify(changes, gs_client.community_key)

        # Write the record to S3
        now = datetime.now(pytz.utc)
        timestamp = now.strftime("%y%m%d_%H%M%S")
        filename = "{}.json".format(timestamp)
        key = "records/{}".format(filename)

        if os.environ.get("IS_LAMBDA_FUNCTION") == "1":
            tmp_path = "/tmp/{0}".format(filename)
        else:
            tmp_path = "./{0}".format(filename)

        with open(tmp_path, "w") as f:
            f.write(json.dumps({
                "data": new_record_data,
                "read_on": now.strftime("%A, %d %B %Y, %X %Z"),
            }))

        extra_args = copy.deepcopy(s3_client.metadata)
        extra_args["ContentType"] = "application/json"

        print("Uploading record to S3...")
        s3_client.upload_file(tmp_path, key, extra_args)


def construct_record_data(records):
    records_dict = dict()

    for item in records:
        id_ = re.sub("[^0-9a-zA-Z]+", "_", item.get("Product").lower())
        records_dict[id_] = item

    return records_dict
