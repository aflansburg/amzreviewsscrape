from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import math
import re
import pprint
import os.path
import sys

pp = pprint.PrettyPrinter(indent=4)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")

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


def read_reviews(driver, file, chromedriver_options):
    if len(chromedriver_options):
        [chrome_options.add_argument(f"--{c}") for c in chromedriver_options]
    base_url = 'https://www.amazon.com/product-reviews/'

    print(f"\nUsing Chromedriver with Options: #{chrome_options.arguments}\n")
    browser = webdriver.Chrome(chrome_options=chrome_options,executable_path=driver)
    asins = read_asin_csv(file)
    products = []

    if len(asins) > 0:
        print(f"\nWorking with {str(len(asins))} ASINS:\n----------------------------")
        for asin in asins:
            review_dict = {asin: {"ratings": [], "review-titles": [], "reviews": [], "review-links": [], }}

            # get reviews page count
            url = base_url + asin
            browser.get(url)
            source = browser.page_source

            soup = BS(source, 'html.parser')

            ratings_reviews_text = soup.find('div', {'data-hook': 'cr-filter-info-review-rating-count'}).span.contents
            ratings_reviews_text = ratings_reviews_text[0].split('|')
            ratings_count = int(re.sub(r'[^\d]', '', ratings_reviews_text[0]))
            reviews_count = int(re.sub(r'[^\d]', '', ratings_reviews_text[1]))
            page_count = int(math.ceil(reviews_count/10))

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
                print(f'\nStarting parsing for ASIN {asin}\nPage count: {str(page_count)}:\n')
                for i in range(page_count):
                    page = i + 1
                    page = str(page)
                    sys.stdout.write(f"\rParsing page {page} of {page_count}")
                    sys.stdout.flush()
                    browser.get(url + f'/ref=cm_cr_getr_d_paging_btm_{page}?pageNumber={page}')
                    html = browser.page_source
                    paged_soup = BS(html, 'html5lib')
                    stars = paged_soup.find_all('i', {'data-hook': ['review-star-rating', 'cmps-review-star-rating']})
                    stars = [s for s in stars if 'stars' in s.span.text]
                    for star in stars:
                        if 'stars' in star.text:
                            regex = "(\d.\d)"
                            p = re.compile(regex)
                            match = p.search(star.text)
                            review_dict[asin]['ratings'].append(match.group(0))
                    review_titles_soup = paged_soup.findAll(re.compile(r'(i|a)'),{'data-hook': 'review-title'})

                    review_titles = []
                    links = []
                    for review_title in review_titles_soup:
                        if 'data-hook' not in review_title.previous_sibling.previous_sibling.attrs.keys() or review_title.previous_sibling.previous_sibling.attrs['data-hook'] != 'review-star-rating-view-point':
                            review_titles.append(review_title)
                            if review_title.name == 'a':
                                links.append(f"https://www.amazon.com{review_title.attrs['href']}")
                            else:
                                links.append('')
                    # links = [f"https://www.amazon.com{l['href']}" for l in links]
                    for ll in links:
                        review_dict[asin]['review-links'].append(ll)
                    for rt in review_titles:
                        sp = rt.findChild('span')
                        if len(rt.findChild('span')):
                            review_dict[asin]['review-titles'].append(re.sub(r'\n', '', rt.span.text))
                        else:
                            review_dict[asin]['review-titles'].append(re.sub(r'\n', '', rt))
                    review_text = paged_soup.find_all('span', {'data-hook': 'review-body'})

                    review_text = [rev.span.text.replace('\U0001f44d', '').replace('\U0001f4a9', '') if rev.span else '' for rev in review_text]
                    for review in review_text:
                        review_dict[asin]['reviews'].append(re.sub(r'\n', '', review))
            data_tuples = []
            for rr in range(len(review_dict[asin]['reviews'])-1):
                try:
                    data_tuples.append((review_dict[asin]['ratings'][rr], review_dict[asin]['review-titles'][rr],
                                        review_dict[asin]['reviews'][rr],
                                        review_dict[asin]['review-links'][rr]))
                except IndexError:
                    print('There was an index out of range error - this typically means the review HTML has changed somehow.')
            products.append({"asin": asin, "title": product_title, "data": data_tuples})
            print(f"\n\nReviews for ASIN {asin} parsed & written to CSV\n----------------------------")
        browser.close()
        # should return an object with all info here (or write out to csv)
        return products

