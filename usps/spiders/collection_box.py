# -*- coding: utf-8 -*-
import scrapy
from usps.items import UspsCollectionBoxItem


class CollectionBoxSpider(scrapy.Spider):
    name = "collection_box"
    allowed_domains = ["tools.usps.com"]
    start_urls = [l.strip() for l in open('zipcodes.txt')]

    def parse(self, response):
        for item in response.xpath('//tr[@class="result"]'):
            lat = float(item.xpath('*/div[@class="flag"]/@lat')[0].extract())
            lon = float(item.xpath('*/div[@class="flag"]/@lon')[0].extract())
            name = item.xpath('td/div/a/span/text()')[0].extract()

            collection_times = []
            for hr in item.xpath('td[@class="hours"]/table/tbody/tr/td/ul/li'):
                days = hr.xpath('span[@class="days"]/text()')[0].extract()
                hour = hr.xpath('span[@class="hours"]/text()')[0].extract()

                collection_times.append(dict(days=days, time=hour))

            address_info = item.xpath('*/div[@class="address"]')[0]
            # sometimes the city is blank for whatever reason
            city_info = address_info.xpath('span[@class="cityLn"]/text()')
            address = {
                "street": address_info.xpath('span[@class="addressLn"]/text()')[0].extract(),
                "city": city_info[0].extract() if city_info else None,
                "state": address_info.xpath('span[@class="stateLn"]/text()')[0].extract(),
                "postcode": address_info.xpath('span[@class="zip-code"]/text()')[0].extract(),
            }
            location_id = address_info.xpath('span[@id="locationID"]/text()')[0].extract()

            yield UspsCollectionBoxItem(
                location_id=location_id,
                name=name,
                address=address,
                collection_times=collection_times,
                lat=lat,
                lon=lon,
            )

