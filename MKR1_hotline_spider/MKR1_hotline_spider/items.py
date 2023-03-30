import scrapy

class BathItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
class BathShop(scrapy.Item):
    title = scrapy.Field()
    shop_link = scrapy.Field()
