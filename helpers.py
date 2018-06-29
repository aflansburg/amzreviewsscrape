from bs4 import BeautifulSoup as BS
from selenium import webdriver
import csv
import math
import re
import pprint
import os.path

pp = pprint.PrettyPrinter(indent=4)


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg  # return the file path


def read_asin_csv(fn):
    asin_list = []
    with open(fn, newline='') as csvfile:
        asin_reader = csv.reader(csvfile, delimiter=',')
        for row in asin_reader:
            asin_list.append(row[0])
    return asin_list


def read_reviews(driver, file):

    base_url = 'https://www.amazon.com/product-reviews/'

    browser = webdriver.Chrome(executable_path=driver)
    asins = read_asin_csv(file)
    products = []

    if len(asins) > 0:
        for asin in asins:
            review_dict = {asin: {"ratings": [], "review-titles": [], "reviews": [], "review-links": []}}

            # get reviews page count
            url = base_url + asin
            browser.get(url)
            source = browser.page_source

            soup = BS(source, 'html.parser')
            # soup = soup.encode("utf-8")

            total_reviews = soup.find('span', {'data-hook': 'total-review-count'})
            total_reviews = int(total_reviews.text.replace(",",""))
            page_count = int(math.ceil(total_reviews/10))

            # grab the title
            if soup.find('a', {'data-hook': 'product-link'}):
                product_title = soup.find('a', {'data-hook': 'product-link'})
                if product_title.text:
                    product_title = str(product_title.text)
                else:
                    product_title = 'No title found'
            else:
                product_title = 'No title found'

            if page_count > 0:
                print(f'Page count: {str(page_count)}')
                for i in range(page_count):
                    page = i + 1
                    page = str(page)
                    print(f'Fetching page {page}')
                    browser.get(url + f'/ref=cm_cr_getr_d_paging_btm_{page}?pageNumber={page}')
                    html = browser.page_source
                    paged_soup = BS(html, 'html.parser')
                    stars = paged_soup.find_all('div', {'data-hook': 'review'})
                    stars = [s for s in stars if 'stars' in s.text]
                    for star in stars:
                        if 'stars' in star.text:
                            regex = "(\d.\d)"
                            p = re.compile(regex)
                            match = p.search(star.text)
                            review_dict[asin]['ratings'].append(match.group(0))
                    review_titles = paged_soup.find_all('a',
                          {'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'})
                    review_titles = [r.text for r in review_titles]
                    links = paged_soup.find_all('a',
                          {'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'}, href=True)
                    links = ["https://www.amazon.com%s" % l['href'] for l in links]
                    for ll in links:
                        review_dict[asin]['review-links'].append(ll)
                    for rt in review_titles:
                        review_dict[asin]['review-titles'].append(rt)
                    review_text = paged_soup.find_all('span', {'data-hook': 'review-body'})
                    review_text = [rev.text.replace('\U0001f44d', '').replace('\U0001f4a9', '') for rev in review_text]
                    for review in review_text:
                        review_dict[asin]['reviews'].append(review)
            data_tuples = []
            for rr in range(len(review_dict[asin]['reviews'])):
                data_tuples.append((review_dict[asin]['ratings'][rr], review_dict[asin]['review-titles'][rr],
                                    review_dict[asin]['reviews'][rr], review_dict[asin]['review-links'][rr]))
            products.append({"asin": asin, "title": product_title, "data": data_tuples})

        browser.close()
        # should return an object with all info here (or write out to csv)
        return products

