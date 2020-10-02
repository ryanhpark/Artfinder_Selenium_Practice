import scrapy


class (scrapy.Item):
    title = scrapy.Field()
    type = scrapy.Field()
    price = scrapy.Field()
    bulletPoints = scrapy.Field()
    shipping = scrapy.Field()
    description = scrapy.Field()
    materialsUsed = scrapy.Field()
    tags = scrapy.Field()
    featuredByEditors = scrapy.Field()
    numberOfPictures = scrapy.Field()
    buyAndSave = scrapy.Field()
