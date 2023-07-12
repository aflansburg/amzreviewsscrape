#NOTICE!
This project has been archived. The ever changing structure of Amazon reviews and the newer mechansisms in place to prevent web scraping are formidable.

# Scrape Amazon Review Pages

Amazon has a system in place to keep you from scraping their pages. What this Python app does is scrape a page from a headless Chrome browser instance using the [Selenium WebDriver](http://www.seleniumhq.org/download/) for Chrome.

This allows you to feed a list of Amazon ASINs in as a .csv (no header) and
scrape the number of reviews received and the number of stars as well.

Each page of reviews will be scraped, so if you provide a large number of ASINs and/or ASINs with a large number of reviews, it could take some time.

Fields that will be retrieved are: `'asin', 'product_title', 'rating', 'review_title', 'variation', 'review_text', 'review-links'`

#### Fair Warning

Web scraping is not an exact science at times, so if a web page's structure changes, or even if something as simple as a class is renamed or a `data-hook` type attribute removed, this code will break. This repo could use some foolproofing and more thought, but for now it works - and we're definitely happy to have any contributions.

#### Debugging Tip

If you're running/testing and having errors, your chromedriver process is likely still running so make sure to Force quit or kill the process in your OS task/process manager.

#### Setup with pipenv

Install all dependencies from the `pipfile`

```
pipenv install
```

#### Usage

Just pass the path to your csv of ASINs (no header) as a command line argument as such

```
# Windows
py amzreviewscrape.py --asins="C:\PATH\TO\ASINS\FILE.CSV" --driverpath="C:\PATH\TO\CHROMEDRIVER"

# Mac OSx/Linux
py amzreviewscrape.py --asins="/path/to/asins/csv" --driverpath="/path/to/chromedriver"
```

To pass additional options to chromedriver such as:

```
--disable-dev-shm-usage
--no-sandbox
```

You can pass the options with `--options` and separated by commas:

```
py amzreviewscrape.py --asins="/path/to/asins/csv" --driverpath="/path/to/chromedriver" --options="disable-dev-shm-usage,no-sandbox"
```

#### Dependencies:

Requires >= [Python version 3.6.3](https://www.python.org/downloads/release/python-363/)

This requires the Selenium Web Driver for Google Chrome which can be found [here](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver).

You will need to install separately and provide to amzreviewscrape.py via the `--driverpath` argument or install to
either `usr/local/bin/chromedriver` for OSx/Linux or `C:\chromedriver\chromedriver\` for Windows to have it sourced automatically.

#### The CSV Output currently looks like:

![output][screenshot]

[screenshot]: https://github.com/aflansburg/amzreviewsscrape/blob/master/scrape-output.png 'CSV Output Screen Shot'
