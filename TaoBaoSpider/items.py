# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import Join, MapCompose


class TaoBaoSearchPageItem(scrapy.Item):
    url_number = scrapy.Field()#链接总数
    page_number = scrapy.Field()#总页数


class TaobaoGoodsListItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    goods_id = scrapy.Field()#商品ID
    wangwang = scrapy.Field()#掌柜旺旺
    location = scrapy.Field()#发货地
    payment_number = scrapy.Field()#付款量
    title = scrapy.Field()#宝贝的标题
    url = scrapy.Field()#宝贝的链接地址
    price = scrapy.Field()#宝贝交易价格
    image_url = scrapy.Field()#宝贝的主图地址

class TaobaoGoodsDetailItem(scrapy.Item):
    goods_id = scrapy.Field()  # 商品ID
    store_name = scrapy.Field()#店铺名称
    original_price = scrapy.Field()#划线价格
    actual_price = scrapy.Field()#实际价格
    sales_volume = scrapy.Field()#30天销量
    postage = scrapy.Field()#邮费
    attribute = scrapy.Field()#属性栏内容
    details = scrapy.Field()#宝贝详情的内容
    score = scrapy.Field()#店铺信誉等级/分数