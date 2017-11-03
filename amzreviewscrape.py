from helpers import readReviews
import os
import csv

dir = os.path.dirname(__file__)
# inputFile = os.path.join(dir, 'samples\\ten_asins.csv')
# run on all listings
inputFile = os.path.join(dir, 'samples\\ALL_ASINs.csv')

# hold on to your butts
if os.name == 'posix':
    # osx
    driver_path = '/usr/local/bin/chromedriver'
elif os.name == 'nt':
    #win32
    driver_path = 'C:\chromedriver\chromedriver'
else:
    print('Unknown operating system!!!')
    exit()

data = readReviews(driver_path, inputFile)

fieldnames = []
for k,v in data[0].items():
    fieldnames.append(k)


with open('output.csv', 'w', newline='') as dataFile:
    dictWriter = csv.DictWriter(dataFile, fieldnames=fieldnames)

    dictWriter.writeheader()
    for dict in data:
        dictWriter.writerow(dict)