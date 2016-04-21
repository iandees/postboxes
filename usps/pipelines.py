# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import json
import os
import errno

class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['location_id'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['location_id'])
            return item

class GeoJSONOutput(object):
    def mkdir_p(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def process_item(self, item, spider):
        prefix = "../data/%s" % item['address']['state'].lower()
        filename = "%s/%sxx.geojson" % (prefix, item['address']['postcode'][:3])
        self.mkdir_p(prefix)

        with open(filename, 'a') as f:
            geojson_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [item['lon'], item['lat']],
                },
                "properties": {
                    "id": item['location_id'],
                    "name": item['name'],
                    "address": item['address'],
                    "collection_times": item['collection_times'],
                }
            }
            line = json.dumps(geojson_feature) + ",\n"
            f.write(line)
        return item
