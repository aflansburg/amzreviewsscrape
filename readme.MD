# amzreviewsscrape

This allows you to feed a list of Amazon ASINs in as a .csv (no header) and
scrape the number of reviews received and the number of stars as well.
I hope to add the ability to scrape the actual review text as well, it
should be trivial, but welcome any PRs.

*** Important Note: If you have 1000 ASINs, this will open 1000 Chrome windows - separate app instances - (although it will close them after the scrape is done).

#### Usage
Just set the path to your csv of ASINs (no header) in `amzreviewscrape.py` - variable `inputFile`
I created a directory called `samples`

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

#### Output currently looks like:

![output][screenshot]

[screenshot]: https://github.com/aflansburg/amzreviewsscrape/blob/master/scrape-output.png "Output Screen Shot"

