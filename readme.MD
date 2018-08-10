# Scrape Amazon Review Pages

Amazon has a system in place to keep you from scraping their pages. What this Python app does is scrape a page from a headless Chrome browser instance using the [Selenium WebDriver](http://www.seleniumhq.org/download/) for Chrome.

This allows you to feed a list of Amazon ASINs in as a .csv (no header) and
scrape the number of reviews received and the number of stars as well.

I have recently added the ability to retrieve review text and the number of stars for that rating.

#### Usage
Just pass the path to your csv of ASINs (no header) as a command line argument as such
```
py amzreviewscrape.py -asins="C:\PATH\TO\ASINS\FILE.CSV"
```



#### Dependencies:
Requires [Python version 3.6.3](https://www.python.org/downloads/release/python-363/) or [greater](https://www.python.org/downloads/)

This uses Beautiful Soup and the Selenium Web Driver for Google Chrome
which can be found [here](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver),
which you will need to install separately and point to in amzreviewscrape.py unless you install to
either `usr/local/bin/chromedriver for OSx/Linux` or `C:\chromedriver\chromedriver\` for Windows

```
# Relevant Code Sample from amzreviewscrape.py for chromedriver directory
# check for current os
if os.name == 'posix':
    # osx
    driver_path = '/usr/local/bin/chromedriver'
elif os.name == 'nt':
    # win32
    driver_path = 'C:\chromedriver\chromedriver'
else:
    print('Unknown operating system!!!')
    exit()
```

#### OS Note
This works on Windows and MacOSx, however take note of the path to the
selenium web driver in the `driver_path` variable.

#### The CSV Output currently looks like:

![output][screenshot]

[screenshot]: https://github.com/aflansburg/amzreviewsscrape/blob/master/scrape-output.png "CSV Output Screen Shot"

