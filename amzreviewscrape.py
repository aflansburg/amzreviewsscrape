from helpers import read_reviews
from helpers import is_valid_file
import argparse
import os
import csv
import io

argparser = argparse.ArgumentParser()
argparser.add_argument("--asins", dest="filename", required=True, help="Enter the path to your ASIN file.",
                       type=lambda x: is_valid_file(argparser, x))
argparser.add_argument("--driverpath", dest="driver_path", required=False, help="Enter the path to your chromedriver file.",
                       type=lambda x: is_valid_file(argparser, x))
args = argparser.parse_args()

inputFile = args.filename
driver_path = args.driver_path
print(inputFile)

# check for current os
if driver_path is None:
    if os.name == 'posix':
        # osx
        driver_path = '/usr/local/bin/chromedriver'
    elif os.name == 'nt':
        # win32
        driver_path = 'C:\chromedriver\chromedriver'
    else:
        print('Unknown operating system!!!')
        exit()

data = read_reviews(driver_path, inputFile)
# *** Commenting out variations for now, as they may not work as expected ***
# field_names = ['asin', 'product_title', 'rating', 'review_title', 'variation', 'review_text', 'review-links']
field_names = ['asin', 'product_title', 'rating', 'review_title', 'review_text', 'review-links']

expanded_reviews = []

for product_reviews in data:
    _asin = product_reviews['asin']
    _title = product_reviews['title']
    _data = product_reviews['data']

    for _d in _data:
        expanded_reviews.append([_asin, _title, _d[0], _d[1], _d[2], _d[3]])

with io.open('./output/output.csv', 'w', encoding="utf-8", newline='') as dataFile:
    writer = csv.writer(dataFile, delimiter=',')

    writer.writerow(field_names)
    for e in expanded_reviews:
        writer.writerow(e)

    print(f'Output written to "./output/output.csv"')




