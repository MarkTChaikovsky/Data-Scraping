import scrapy
import json
import requests
from MKR1_hotline_spider.items import BathItem,BathShop


def post_item_to_mockend(item):
    url = 'https://mockend.com/Andrashko/scraping2023/Items'
    headers = {'Content-type': 'application/json'}
    data = json.dumps(dict(item))
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)


def post_shop_to_mockend(shop):
    url = 'https://mockend.com/Andrashko/scraping2023/Shops'
    headers = {'Content-type': 'application/json'}
    data = json.dumps(dict(shop))
    response = requests.post(url, headers=headers, data=data)
    print(response.status_code)


class HotlineSpider(scrapy.Spider):
    name = 'hotline_spider'
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/santekhnika/vanny/']

    def parse(self, response):

        products = response.css('div.list-body__content').css('.list-item')

        for product in products:
            title = product.css('a.list-item__title::text').get()
            link = product.css('a.list-item__title::attr(href)').get()
            price = product.css('span.price__value::text').get()

            item = BathItem(
                title=title,
                link=link,
                price=price
            )
            yield item
            post_item_to_mockend(item)

            yield BathItem(
                title = title,
                link = link,
                price = price
            )
            yield scrapy.Request(
                url = 'https://hotline.ua/'+link,
                callback = self.parse_shop
            )

    def parse_shop(self, response):
        shops = response.css('div.list').css('.list__item')
        for shop in shops:
            title = shop.css('a.shop__title::text').get()
            shop_link = shop.css('a.shop__title::attr(href)').get()

            shop_item = BathShop(
                title=title,
                shop_link=shop_link
            )
            post_shop_to_mockend(shop_item)

            yield shop_item

            yield BathShop(
                title = title,
                shop_link = shop_link
            )

        next_page = response.css('a.pagination-next::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
