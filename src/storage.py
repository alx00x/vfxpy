import boto3

s3_client = boto3.client("s3")

bucket = "vfxpy.com"

metadata = {
    "CacheControl": "max-age=21600, public",    # 6 hours
    "ACL": "public-read",                       # make public
}
