import scrapy
from scrapy.spiders import Spider
from scrapy.loader import ItemLoader
from ..items import TaoBaoSearchPageItem, TaobaoGoodsListItem, TaobaoGoodsDetailItem

class TaoBaoSpider(Spider):
    name = 'taobao.com'
    allowed_domains = [
        'taobao.com',
        'tmall.com'
    ]
    start_urls = [
        'https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20170907&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E8%A3%A4%E5%AD%90%E7%94%B7&suggest=0_2&_input_charset=utf-8&wq=%E8%A3%A4%E5%AD%90&suggest_query=%E8%A3%A4%E5%AD%90&source=suggest&sort=sale-desc'
    ]

    def parse(self, response):
        url_number = response.xpath(
            '//*[@id="mainsrp-itemlist"]/div/div/div[1]/div[1]/div[1]/div/div[1]/a/@trace-num').extract_first()
        page_number = response.xpath('//*[@id="mainsrp-pager"]/div/div/div/div[1]/text()').extract_first()
        searchPageItem = TaoBaoSearchPageItem(url_number=url_number, page_number=page_number)
        yield searchPageItem
        goods_list = response.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
        for goods in goods_list:
            item_loader = ItemLoader(item=TaobaoGoodsListItem(), selector=goods)
            item_loader.add_xpath('goods_id', './div[1]/div/div[1]/a/@trace-nid')
            item_loader.add_xpath('wangwang', './div[2]/div[4]/div[2]/span/a/@href')
            item_loader.add_xpath('location', './div[2]/div[3]/div[2]/text()')
            item_loader.add_xpath('payment_number', './div[2]/div[1]/div[2]/text()')
            item_loader.add_xpath('title', './div[2]/div[2]/a/text()[1]')
            item_loader.add_xpath('title', './div[2]/div[2]/a/span[1]/text()')
            item_loader.add_xpath('title', './div[2]/div[2]/a/text()[2]')
            item_loader.add_xpath('title', './div[2]/div[2]/a/span[2]/text()')
            item_loader.add_xpath('title', './div[2]/div[2]/a/text()[3]')
            item_loader.add_xpath('url', './div[1]/div/div[1]/a/@href')
            item_loader.add_xpath('price', './div[2]/div[1]/div[1]/strong/text()')
            item_loader.add_xpath('image_url', './div[1]//div[@class="pic"]/a/img/@data-src')
            goodsListItem = item_loader.load_item()
            yield goodsListItem
            detail_url = goodsListItem['url']
            if 'tmall.com' in detail_url:
                request = scrapy.Request(url=detail_url, callback=self.parse_tmall_item)
            else:
                print(detail_url)
                request = scrapy.Request(url=detail_url, callback=self.parse_taobao_item)
            request.meta['goods_id'] = goodsListItem['goods_id']
            yield request

    def parse_tmall_item(self, response):
        item_loader = ItemLoader(item=TaobaoGoodsDetailItem(), response=response)
        item_loader.add_value('goods_id', response.meta['goods_id'])
        item_loader.add_xpath('store_name', '//*[@id="side-shop-info"]/div/h3/div/a/text()')
        item_loader.add_xpath('original_price', '//*[@id="J_StrPriceModBox"]/dd/span/text()')
        item_loader.add_xpath('actual_price', '//*[@id="J_PromoPrice"]/dd/div/span/text()')
        item_loader.add_xpath('sales_volume', '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/ul/li[1]/div/span[2]/text()')
        item_loader.add_xpath('postage', '//*[@id="J_PostageToggleCont"]/p/span/text()')
        item_loader.add_xpath('attribute', '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dt/text()')
        item_loader.add_xpath('attribute', '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[1]/dd/ul/li/a/span/text()')
        item_loader.add_xpath('attribute', '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[2]/dt/text()')
        item_loader.add_xpath('attribute', '//*[@id="J_DetailMeta"]/div[1]/div[1]/div/div[4]/div/div/dl[2]/dd/ul/li/a/span/text()')
        item_loader.add_xpath('details', '//*[@id="J_AttrUL"]/li/text()')
        item_loader.add_xpath('score', '//*[@id="shop-info"]/div[2]/div[1]/div[2]/span/text()')
        item_loader.add_xpath('score', '//*[@id="shop-info"]/div[2]/div[2]/div[2]/span/text()')
        item_loader.add_xpath('score', '//*[@id="shop-info"]/div[2]/div[3]/div[2]/span/text()')
        goodsDetailItem = item_loader.load_item()
        yield goodsDetailItem

    def parse_taobao_item(self, response):
        item_loader = ItemLoader(item=TaobaoGoodsDetailItem(), response=response)
        item_loader.add_value('goods_id', response.meta['goods_id'])
        item_loader.add_xpath('store_name', '//*[@id="J_ShopInfo"]/div/div[1]/div[1]/dl/dd/strong/a/text()')
        item_loader.add_xpath('original_price', '//*[@id="J_StrPrice"]/em[2]/text()')
        item_loader.add_xpath('actual_price', '//*[@id="J_PromoPriceNum"]/text()')
        item_loader.add_xpath('sales_volume', '//*[@id="J_Counter"]/div/div[2]/a/@title')
        item_loader.add_xpath('postage', '//*[@id="J_WlServiceTitle"]/text()')
        item_loader.add_xpath('attribute', '')
        item_loader.add_xpath('details', '//*[@id="attributes"]/ul/li/text()')
        item_loader.add_xpath('score', '//*[@id="J_ShopInfo"]/div/div[2]/div/dl[1]/dd/a/text()')
        item_loader.add_xpath('score', '//*[@id="J_ShopInfo"]/div/div[2]/div/dl[2]/dd/a/text()')
        item_loader.add_xpath('score', '//*[@id="J_ShopInfo"]/div/div[2]/div/dl[3]/dd/a/text()')
        goodsDetailItem = item_loader.load_item()
        yield goodsDetailItem