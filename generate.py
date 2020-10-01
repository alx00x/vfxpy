import os

from src.svg_wheel import generate_svg_wheel
from src.utils import get_packages, remove_irrelevant_packages, save_to_file, compare_and_notify
from src.clients import s3Client, gsClient


S3_BUCKET = os.environ["S3_BUCKET"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]
RECIPIENT_EMAIL = os.environ["RECIPIENT_EMAIL"]

VFXPY_SPREADSHEET_KEY = os.environ["VFXPY_SPREADSHEET_KEY"]
COMMUNITY_SPREADSHEET_KEY = os.environ["COMMUNITY_SPREADSHEET_KEY"]


def main(*args):

    s3_client = s3Client(S3_BUCKET, SENDER_EMAIL, RECIPIENT_EMAIL)
    gs_client = gsClient(VFXPY_SPREADSHEET_KEY, COMMUNITY_SPREADSHEET_KEY)

    packages = remove_irrelevant_packages(get_packages(gs_client))
    save_to_file(s3_client, packages)
    generate_svg_wheel(s3_client, packages)
    compare_and_notify(s3_client, gs_client)
    print("Exiting...")

if __name__ == '__main__':
    main()
