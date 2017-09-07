# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, re
from .items import TaobaoGoodsDetailItem, TaobaoGoodsListItem, TaoBaoSearchPageItem

class TaobaospiderPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, TaoBaoSearchPageItem):
            self._process_search_item(item)
        elif isinstance(item, TaobaoGoodsListItem):
            self._process_list_item(item)
        else:
            self._process_detail_item(item)
        return item

    def _process_search_item(self, item):
        item['page_number'] = item['page_number'].replace('\n', '').replace(' ', '').rstrip('，')
        self.db.search.insert(dict(item))

    def _process_list_item(self, item):
        pattern = re.compile('\d+')
        item['image_url'] = 'https:' + item['image_url'][0]
        item['title'] = ''.join(item['title']).replace('\n', '').replace(' ', '')
        item['url'] = 'https:' + item['url'][0]
        item['goods_id'] = item['goods_id'][0]
        item['price'] = item['price'][0]
        item['location'] = item['location'][0]
        match = pattern.search(item['payment_number'][0])
        item['payment_number'] = match.group() if match else item['payment_number']
        self.db.goodslist.insert(dict(item))

    def _process_detail_item(self, item):
        self.db.goodsdetail.insert(dict(item))
