from bs4 import BeautifulSoup as BS
from selenium import webdriver
import csv

def readAsinCSV(fn):
    asinList = []
    with open(fn, newline='') as csvfile:
        asinReader = csv.reader(csvfile, delimiter=',')
        for row in asinReader:
            asinList.append(row[0])
    return asinList

def readReviews(driver , file):

    BASE_URL = 'https://www.amazon.com/product-reviews/'

    browser = webdriver.Chrome(executable_path=driver)
    asins = readAsinCSV(file)
    products = []

    if len(asins) > 0:
        for asin in asins:
            url = BASE_URL + asin
            browser.get(url)
            html = browser.page_source

            soup = BS(html, 'html.parser')
            # grab the title
            if soup.find('a', {'data-hook': 'product-link'}):
                title = soup.find('a', {'data-hook': 'product-link'})
                if (title.text):
                    title = str(title.text)
                else:
                    title = 'No title found'
            else:
                title = 'No title found'


            # grab the element containing the total number of reviews
            totalReviews = soup.find('span', {'data-hook': 'total-review-count'})
            if totalReviews:
                totalReviews = int(totalReviews.text)
            else:
                print('no reviews - FAIL')

            if totalReviews != 0:
                averageRating = soup.find('span', {'data-hook': 'rating-out-of-text'})
                averageRating = str(averageRating.text)
                # grab the element containing the number of 5 star reviews and parse out everything
                # except for the percentage and then convert it to a float
                fiveStarsP = soup.find('a', {'a-size-small a-link-normal 5star histogram-review-count'})
                if fiveStarsP:
                    fiveStarsP = str(fiveStarsP.text)
                    fiveStarsP = fiveStarsP.replace('%', '')
                    fiveStarsP = float(float(fiveStarsP) / 100)
                    fiveStars = totalReviews * fiveStarsP
                    fiveStars = int(round(fiveStars, 0))
                else:
                    fiveStarsP = 0
                    fiveStars = 0

                fourStarsP = soup.find('a', {'a-size-small a-link-normal 4star histogram-review-count'})
                if (fourStarsP):
                    fourStarsP = str(fourStarsP.text)
                    fourStarsP = fourStarsP.replace('%', '')
                    fourStarsP = float(float(fourStarsP) / 100)
                    fourStars = totalReviews * fourStarsP
                    fourStars = int(round(fourStars, 0))
                else:
                    fourStarsP = 0
                    fourStars = 0

                threeStarsP = soup.find('a', {'a-size-small a-link-normal 3star histogram-review-count'})
                if (threeStarsP):
                    threeStarsP = str(threeStarsP.text)
                    threeStarsP = threeStarsP.replace('%', '')
                    threeStarsP = float(float(threeStarsP) / 100)
                    threeStars = totalReviews * threeStarsP
                    threeStars = int(round(threeStars, 0))
                else:
                    threeStarsP = 0
                    threeStars = 0

                twoStarsP = soup.find('a', {'a-size-small a-link-normal 2star histogram-review-count'})
                if (twoStarsP):
                    twoStarsP = str(twoStarsP.text)
                    twoStarsP = twoStarsP.replace('%', '')
                    twoStarsP = float(float(twoStarsP) / 100)
                    twoStars = totalReviews * twoStarsP
                    twoStars = int(round(twoStars, 0))
                else:
                    twoStarsP = 0
                    twoStars = 0

                oneStarP = soup.find('a', {'a-size-small a-link-normal 1star histogram-review-count'})
                if oneStarP:
                    oneStarP = str(oneStarP.text)
                    oneStarP = oneStarP.replace('%', '')
                    oneStarP = float(float(oneStarP) / 100)
                    oneStar = totalReviews * oneStarP
                    oneStar = int(round(oneStar, 0))
                else:
                    oneStarP = 0
                    oneStar = 0

                productDict = { 'ASIN': asin, 'title': title, 'totalReviews': totalReviews, 'averageStars': averageRating,
                               'oneStarReviews': oneStar, 'twoStarReviews': twoStars, 'threeStarReviews': threeStars,
                               'fourStarReviews': fourStars, 'fiveStarReviews': fiveStars }
                products.append(productDict)
                # print(f'\n{title}\n')
                # print(f'Total reviews: {totalReviews}')
                # print(f'Average rating: {averageRating}\n')
                # print(f'Total number of 1 star reviews: {oneStar} ({int(oneStarP*100)}%)')
                # print(f'Total number of 2 star reviews: {twoStars} ({int(twoStarsP*100)}%)')
                # print(f'Total number of 3 star reviews: {threeStars} ({int(threeStarsP*100)}%)')
                # print(f'Total number of 4 star reviews: {fourStars} ({int(fourStarsP*100)}%)')
                # print(f'Total number of 5 star reviews: {fiveStars} ({int(fiveStarsP*100)}%)')
            else:
                print(f'\n{asin}: {title}')
                print(f'No reviews or ratings!\n')
        browser.close()
        # should return an object with all info here (or write out to csv)
        return products



