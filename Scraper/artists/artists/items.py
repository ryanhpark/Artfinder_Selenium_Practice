import scrapy


class ArtistsItem(scrapy.Item):
    artFinderId = scrapy.Field()
    artistName = scrapy.Field()
    country = scrapy.Field()
    products_count = scrapy.Field()
    follows = scrapy.Field()
    profession = scrapy.Field()
    is_represented_by_gallery = scrapy.Field()
    is_artist = scrapy.Field()
    accepts_commissions = scrapy.Field()
    artist_rating = scrapy.Field()
    seller_rating = scrapy.Field()
    is_artist_of_the_day_today = scrapy.Field()
