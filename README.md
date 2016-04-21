# USPS Post Box Scraper

A Scrapy spider that finds as many US Postal Service collection boxes that it can from the USPS website and outputs the resulting data to geojson features for easier consumption.

### Data

You can browse the data that was scraped in April 2016 by going to the [`data`](https://github.com/iandees/postboxes/tree/master/data) directory. The data is organized in files by state two-letter code and in files based on the first three characters of the postal code of the post box reported by the USPS.

The properties of each GeoJSON feature include the opening hours, name, address, and identifier as reported by the US Postal Service.

### Running the Scraper

This is a standard [Scrapy](https://scrapy.readthedocs.org/en/latest/) spider. More detailed installation instructions can be found on Scrapy's page, but in general:

```
git clone git@github.com:iandees/postboxes.git
cd postboxes
virtualenv venv
venv/bin/activate
pip install -r requirements.txt
scrapy crawl collection_box
```

Once you've run the scraper, you'll have a bunch of files with a single GeoJSON feature per line. Run `geojsonify.py` to clean then up and add the rest of the GeoJSON structure around those lines to make them a FeatureCollection browseable on GitHub.

```
python geojsonify.py
```
