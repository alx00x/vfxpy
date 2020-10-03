import boto3
from botocore.exceptions import ClientError

import gspread

from src.template import changes_table, warning_body


class s3Client(object):
    def __init__(self, bucket, sender, recipient):
        self.client = boto3.client("s3")
        self.ses_client = boto3.client("ses")
        self.bucket = bucket
        self.metadata = {
            "CacheControl": "max-age=21600, public",    # 6 hours
        }

        self.sender = sender
        self.recipient = recipient

    def list_files(self, prefix):
        files = list()
        response = self.client.list_objects_v2(Bucket=self.bucket, Prefix=prefix, StartAfter=prefix)
        for content in response.get("Contents", []):
            files.append({"Key": content.get("Key"), "LastModified": content.get("LastModified")})
        files.sort(key=lambda item: item["LastModified"], reverse=True)
        return files

    def upload_file(self, file, key, extra_args):
        self.client.upload_file(file, self.bucket, key, ExtraArgs=extra_args)

    def get_object(self, key):
        return self.client.get_object(Bucket=self.bucket, Key=key)

    def delete_object(self, key):
        return self.client.delete_object(Bucket=self.bucket, Key=key)

    def notify(self, changes, community_key, vfxpy_key):
        subject = "VFXPY: there are changes for you to check! "

        # construct email from changes
        body_html = """
        <html>
        <head></head>
        <body>
            <h1>VFX Python 3 Readiness</h1>
            <p>Changes have occurred in the <a href="https://docs.google.com/spreadsheets/d/{community_key}">community spreadsheet</a>!</p>
            <p>Please update <a href="https://docs.google.com/spreadsheets/d/{vfxpy_key}">vfxpy spreadsheet</a> accordingly:</p>
        """.format(community_key=community_key, vfxpy_key=vfxpy_key)

        for idx, each in enumerate(changes):
            body_html += "<h4>Change ID: {num}</h4>".format(num=idx)
            body_html += changes_table.format(
                product=each["product"],
                key=each["key"],
                old_value=each["old_value"],
                new_value=each["new_value"],
                )

        body_html += "</body></html>"

        body_text = ("VFX Python 3 Readiness\r\n"
                     "Changes have occurred in the community spreadsheet!\r\n"
                     "https://docs.google.com/spreadsheets/d/{sid}".format(sid=sid)
                     )

        self.send_email(subject, body_html, body_text)

    def warn(self, message):
        subject = "VFXPY: warning"
        body_html = warning_body.format(message)
        self.send_email(subject, body_html, message)

    def send_email(self, subject, body_html, body_text):
        charset = "UTF-8"
        try:
            response = self.ses_client.send_email(
                Destination={"ToAddresses": [self.recipient]},
                Message={
                    "Subject": {
                        "Charset": charset,
                        "Data": subject,
                    },
                    "Body": {
                        "Html": {
                            "Charset": charset,
                            "Data": body_html,
                        },
                        "Text": {
                            "Charset": charset,
                            "Data": body_text,
                        },
                    },
                },
                Source=self.sender,
            )
        # Display an error if something goes wrong.
        except ClientError as err:
            print(err.response["Error"]["Message"])
        else:
            print("Email sent! Message ID:")
            print(response["MessageId"])


class gsClient(object):
    def __init__(self, vfxpy_key, community_key):
        self.client = gspread.service_account(filename="client_secret.json")
        self.vfxpy_key = vfxpy_key
        self.community_key = community_key

        self._vfxpy_book = None
        self._community_book = None

        self.initialize()

    def initialize(self):

        # Get vfxpy maintained spreadsheet (we cannot let this one fail)
        print("Getting vfxpy book...")
        self._vfxpy_book = self.client.open_by_key(self.vfxpy_key)

        # Try to get community maintained spreadsheet
        print("Getting community book...")
        try:
            self._community_book = self.client.open_by_key(self.community_key)
        except Exception as err:
            # Print to log
            print(err)

    @property
    def vfxpy_book(self):
        return self._vfxpy_book

    @property
    def community_book(self):
        return self._community_book
