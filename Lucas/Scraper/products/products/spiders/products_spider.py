from products.items import ProductsItem
from scrapy import Spider, Request
import re
import pandas as pd


class Products(Spider):
    name = 'products_spider'
    allowed_urls = ['https://www.artfinder.com/#/']
    start_urls = ['https://www.artfinder.com/#/']

    def parse(self, response):
        # get a list of all slugs
        df = pd.read_csv("../artists.csv", usecols=['slug']).drop_duplicates()
        slugs = df['slug'].to_list()

        list_urls = [f'https://www.artfinder.com/{slug}#/' for slug in slugs]

        # go for each artist page
        for url in list_urls:
            yield Request(url=url, callback=self.parse_page)

    def parse_artist_page(self, response):
        # get the max pages of work

    def parse_product_page(self, response):
        item = ProductsItem()
        item['title'] = response.xpath(
            '//h1[@class="h2 af-underline-links"]/text()').extract()[0].strip()
        item['type'] = response.xpath(
            '//h2[@class="p af-underline-links margin margin-s"]/a/text()').extract_first()
        item['price'] = response.xpath(
            '//span[@class="main-price js-price"]/text()').extract_first()

        bulletPoints_raw = response.xpath(
            '//ul[@class="af-underline-links"]/li/span').extract()
        bulletPoints = list(map(lambda x: re.sub(
            r'\<[^<>]*\>', '', x).strip(), bulletPoints))
        item['bulletPoints'] = bulletPoints

        # item['shipping'] = SELENIUM

        item['description'] = response.xpath(
            '//div[@id="product-description"]/p/text()').extract_first()
        item['materialsUsed'] = response.xpath(
            '//div[@id="product-description"]/p/text()').extract()[1].split(",")
        item['tags'] = response.xpath(
            '//p[@class="af-line-height-l"]/a/text()').extract()

        item['featuredByEditors'] = response.xpath('//div[@class="show-for-large-up margin margin-m margin-top"]/p/a/text()').extract(
        ) if response.xpath('//div[@class="show-for-large-up margin margin-m margin-top"]/p/a/text()').extract() != [] else "---"

        # item['numberOfPictures'] = ??????

        yield item
