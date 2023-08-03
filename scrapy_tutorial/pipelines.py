# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import ujson
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ScrapyTutorialPipeline:
    def process_item(self, item, spider):
        if "bio" in item:
            with open("authors.jsonld", "a+") as fp:
                fp.write(f"{ujson.dumps(item)}\n")
        else:
            with open("quotes.jsonld", "a+") as fp:
                fp.write(f"{ujson.dumps(item)}\n")
        return item
