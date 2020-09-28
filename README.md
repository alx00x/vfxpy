VFX Python 3 Readiness
==================

Python 3 support graph for most popular Python libraries and DCC applications used in VFX production.

## How do you identify Python 3 support?

This site pulls from the data found in a google [spreadsheet](https://docs.google.com/spreadsheets/d/1mvmWPO8vdAtH_jHJd3v4GoSxBueZeOM362NSjlSEQWI), which itself is a copy of the the [original one](https://docs.google.com/spreadsheets/d/10XG92byepTD-LEeXx4mBjhGaNPtJsd_QaXlZ866wj7k) made and maintained by the community. Since the original spreadsheet is editable by preatty much anyone with an internet connection, author of this site didn't feel confortable pulling data directly form it. Additionally, it is not quite programmatically friendly, so a copy was necessary for the time being. **This may (hopefully) change in the future.**

*A notification system has been set up to notify the author about any changes that occur in the original spreadsheet.*

## Contribute

Please use issue tracker for issues, suggestions, feature requests and further enhancements.

## How does the site work?

The site works by checking a [spreadsheet](https://docs.google.com/spreadsheets/d/1mvmWPO8vdAtH_jHJd3v4GoSxBueZeOM362NSjlSEQWI) on daily bases. Script `generate.py` runs on AWS Lambda to generate the data shown on the website. 

It saves output JSON file to S3 which is used to build graph. Site itself is hosted on S3 bucket.

## Credits

This is derivative work from [py3readiness](http://chhantyal.net/py3readiness/), a site that tracks general compatibility with Python 3, which in turn is a derivative of [pythonwheels.com](https://pythonwheels.com/), a site that tracks which Python distributions ship the wheel distribution.
