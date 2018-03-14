# Scrape Amazon Review Pages

Amazon has a system in place to keep you from scraping their pages. What this Python app does is open individual browser windows and scrapes
the content on the page displayed using the [Selenium WebDriver](http://www.seleniumhq.org/download/) for Chrome.
After each scrape, the opened Chrome window is closed.

This allows you to feed a list of Amazon ASINs in as a .csv (no header) and
scrape the number of reviews received and the number of stars as well.

I have recently added the ability to retrieve review text and the number of stars for that rating.

#### Usage
Just set the path to your csv of ASINs (no header) in `amzreviewscrape.py` - variable `inputFile`.

To run:
```
py amzreviewscrape.py
```

#### Dependencies:
This uses Beautiful Soup and the Selenium Web Driver for Google Chrome
which can be found [here](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver),
which you will need to install separately and point

#### OS Note
This works on Windows and MacOSx, however take note of the path to the
selenium web driver in the `driver_path` variable.

#### The CSV Output currently looks like:

![output][screenshot]

[screenshot]: https://github.com/aflansburg/amzreviewsscrape/blob/master/scrape-output.png "CSV Output Screen Shot"

